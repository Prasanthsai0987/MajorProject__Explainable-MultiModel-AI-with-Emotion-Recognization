
# where this db url is testing for local development
# and in the deployment i used render postgre database url which is different from this one.
# because the local db wont work in the internet so i used render postgre database url for deployment.Youtube Link :



https://www.youtube.com/watch?v=57eIpiotkiE 



If Something Breaks

Use this order:

Database error

Check:

DATABASE_URL
/api/auth/register fails

Check:

PostgreSQL
users table
DATABASE_URL
Login fails

Check:

email
password_hash
bcrypt
PostgreSQL
/api/auth/me returns 401

Check:

JWT
Authorization header
axios interceptor
get_current_user()
SECRET_KEY
Google login fails

Check:

GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI
Google Cloud Console
Google login succeeds but doesn't enter /home

Check:

GoogleCallback.jsx
/auth/callback route
setGoogleToken()
/api/auth/me
axios Authorization header
ProtectedRoute
END

Main idea:

LOCAL DEVELOPMENT
        ↓
Local PostgreSQL + pgAdmin

PRODUCTION
        ↓
Render PostgreSQL

FASTAPI
        ↓
DATABASE_URL

AUTHENTICATION
        ↓
PostgreSQL + JWT

GOOGLE LOGIN