from urllib.parse import urlencode

import requests

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.database import get_db
from app.db.models import User
from app.db.schemas import (
    LoginResponse,
    RegisterRequest,
    UserOut,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    # Check whether email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    # Create user
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create JWT
    token = create_access_token(
        {
            "sub": user.id,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2PasswordRequestForm uses "username".
    # We use the email as the username.
    user = (
        db.query(User)
        .filter(User.email == form.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Google-only accounts don't have a password
    if not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This account uses Google Sign-In.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(
        form.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT
    token = create_access_token(
        {
            "sub": user.id,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }


# ============================================================
# CURRENT USER
# ============================================================

@router.get(
    "/me",
    response_model=UserOut,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


# ============================================================
# GOOGLE LOGIN
# ============================================================

@router.get("/google")
def google_login():
    """
    Start Google OAuth login.

    Browser goes:
        Frontend
            ↓
        /api/auth/google
            ↓
        Google login page
    """

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urlencode(params)
    )

    # IMPORTANT:
    # Redirect to GOOGLE here.
    #
    # Do NOT use jwt_token here.
    # jwt_token does not exist yet.
    return RedirectResponse(
        url=google_auth_url
    )


# ============================================================
# GOOGLE CALLBACK
# ============================================================

@router.get("/google/callback")
def google_callback(
    code: str,
    db: Session = Depends(get_db),
):
    """
    Google redirects here after successful login.

    Google
       ↓
    /api/auth/google/callback?code=...
       ↓
    Get Google access token
       ↓
    Get Google user information
       ↓
    Create/find local user
       ↓
    Create our JWT
       ↓
    Redirect to React /auth/callback
    """

    # --------------------------------------------------------
    # 1. Exchange Google authorization code for tokens
    # --------------------------------------------------------

    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=15,
    )

    if token_res.status_code != 200:
        print("Google token error:", token_res.text)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get Google token.",
        )

    google_tokens = token_res.json()

    google_access_token = google_tokens.get(
        "access_token"
    )

    if not google_access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google access token missing.",
        )

    # --------------------------------------------------------
    # 2. Get Google user information
    # --------------------------------------------------------

    userinfo_res = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={
            "Authorization": f"Bearer {google_access_token}",
        },
        timeout=15,
    )

    if userinfo_res.status_code != 200:
        print(
            "Google user info error:",
            userinfo_res.text,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get Google user information.",
        )

    guser = userinfo_res.json()

    # --------------------------------------------------------
    # 3. Extract Google user information
    # --------------------------------------------------------

    google_id = guser.get("sub")
    email = guser.get("email")
    name = guser.get("name")
    avatar_url = guser.get("picture")

    if not google_id or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account information is incomplete.",
        )

    if not name:
        name = email.split("@")[0]

    # --------------------------------------------------------
    # 4. Find user by Google ID
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(User.google_id == google_id)
        .first()
    )

    # --------------------------------------------------------
    # 5. If not found, check email
    # --------------------------------------------------------

    if not user:

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        # ----------------------------------------------------
        # Existing email account
        # ----------------------------------------------------

        if user:
            user.google_id = google_id
            user.avatar_url = avatar_url

        # ----------------------------------------------------
        # Completely new Google account
        # ----------------------------------------------------

        else:
            user = User(
                name=name,
                email=email,
                google_id=google_id,
                avatar_url=avatar_url,
                password_hash=None,
            )

            db.add(user)

    # --------------------------------------------------------
    # 6. Save user
    # --------------------------------------------------------

    db.commit()
    db.refresh(user)

    # --------------------------------------------------------
    # 7. Create our application JWT
    # --------------------------------------------------------

    jwt_token = create_access_token(
        {
            "sub": user.id,
        }
    )

    # --------------------------------------------------------
    # 8. Redirect to React
    # --------------------------------------------------------

    return RedirectResponse(
        url=(
            f"{settings.FRONTEND_URL}"
            f"/auth/callback"
            f"?token={jwt_token}"
        )
    )