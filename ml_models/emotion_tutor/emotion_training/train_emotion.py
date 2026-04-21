import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# --------------------
# CONFIG
# --------------------
IMG_SIZE = 48
BATCH_SIZE = 32
EPOCHS = 30

train_dir = "emotion_tutor/dataset"
MODEL_SAVE_PATH = "emotion_tutor/models/emotion_model"

os.makedirs("emotion_tutor/models", exist_ok=True)

# --------------------
# DATA GENERATOR
# --------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    shear_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode="grayscale",
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    subset="training"
)

val_data = datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode="grayscale",
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    subset="validation"
)

# --------------------
# MODEL
# --------------------
model = models.Sequential([
    layers.Conv2D(32, (3,3), padding="same", input_shape=(48,48,1)),
    layers.BatchNormalization(),
    layers.Activation("relu"),
    layers.MaxPooling2D(2,2),
    layers.Dropout(0.25),

    layers.Conv2D(64, (3,3), padding="same"),
    layers.BatchNormalization(),
    layers.Activation("relu"),
    layers.MaxPooling2D(2,2),
    layers.Dropout(0.25),

    layers.Conv2D(128, (3,3), padding="same"),
    layers.BatchNormalization(),
    layers.Activation("relu"),
    layers.MaxPooling2D(2,2),
    layers.Dropout(0.3),

    layers.Flatten(),
    layers.Dense(256, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(train_data.num_classes, activation="softmax")
])

# --------------------
# COMPILE
# --------------------
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# --------------------
# CALLBACKS
# --------------------
cb = [
    callbacks.EarlyStopping(
        monitor="val_loss",
        patience=6,
        restore_best_weights=True
    ),
    callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
        min_lr=1e-5
    ),
    callbacks.ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        save_format="tf"
    )
]

# --------------------
# TRAIN
# --------------------
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    callbacks=cb
)

# --------------------
# SAVE FINAL MODEL
# --------------------
model.save(MODEL_SAVE_PATH)
print("✅ Emotion model saved successfully")
