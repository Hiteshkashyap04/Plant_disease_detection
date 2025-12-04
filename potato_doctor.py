import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np
import os
import json

# ==========================================
# 1. CONFIGURATION
# ==========================================
DATASET_PATH = 'MiniDataset' 
MODEL_NAME = 'potato_model.h5'
CLASS_NAMES_FILE = 'class_names.json'

# Image settings
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20 # Increased to 20, but EarlyStopping will stop it sooner if needed

# ==========================================
# 2. MODEL ARCHITECTURE
# ==========================================
def create_model(num_classes):
    print(f"Building Model for {num_classes} classes...")
    model = Sequential([
        # Block 1 - The "Eyes"
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
        MaxPooling2D(2, 2),
        
        # Block 2
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        # Block 3
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        # Block 4 (Added for extra complexity since we have Background data now)
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        # Classification Head - The "Brain"
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5), # Prevents memorization
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam', 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    return model

# ==========================================
# 3. TRAINING FUNCTION
# ==========================================
def train_model():
    # 1. Check Dataset
    if not os.path.exists(DATASET_PATH):
        print("ERROR: 'MiniDataset' folder not found.")
        return

    # 2. Setup Data Augmentation
    # We add more "noise" here so the model learns to be robust
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,      # Rotate images
        width_shift_range=0.2,  # Shift left/right
        height_shift_range=0.2, # Shift up/down
        shear_range=0.2,        # Distort shape
        zoom_range=0.2,         # Zoom in
        horizontal_flip=True,   # Mirror image
        fill_mode='nearest',
        validation_split=0.2
    )

    print("\n--- LOADING DATA ---")
    train_generator = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_generator = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    # 3. Save Class Names
    class_indices = train_generator.class_indices
    class_names = list(class_indices.keys())
    
    print(f"Classes Detected: {class_names}")
    
    with open(CLASS_NAMES_FILE, 'w') as f:
        json.dump(class_names, f)
    
    # 4. Setup Callbacks (The Smart Helpers)
    # Stop training if validation accuracy doesn't improve for 5 epochs
    early_stop = EarlyStopping(
        monitor='val_loss', 
        patience=5, 
        restore_best_weights=True,
        verbose=1
    )
    
    # Save the model only when it gets better
    checkpoint = ModelCheckpoint(
        MODEL_NAME, 
        monitor='val_accuracy', 
        save_best_only=True, 
        mode='max',
        verbose=1
    )

    # 5. Build and Train
    model = create_model(len(class_names))
    
    print("\n--- STARTING TRAINING ---")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=[early_stop, checkpoint] # Add the callbacks here
    )

    print(f"\nTraining Complete! Best model saved as '{MODEL_NAME}'")
    print(f"Class names saved to '{CLASS_NAMES_FILE}'")

# ==========================================
# 4. PREDICTION TEST FUNCTION
# ==========================================
def predict_image(image_path):
    if not os.path.exists(image_path):
        print("Error: Image file not found.")
        return

    if not os.path.exists(MODEL_NAME):
        print("Error: Model not found. Train it first.")
        return
    
    # Load resources
    model = tf.keras.models.load_model(MODEL_NAME)
    with open(CLASS_NAMES_FILE, 'r') as f:
        class_names = json.load(f)

    # Process Image
    img = load_img(image_path, target_size=IMG_SIZE)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Predict
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions)
    confidence = np.max(predictions)
    disease_name = class_names[predicted_index]

    # --- CLI REPORT ---
    print("\n" + "="*30)
    print(f"   PREDICTION RESULT")
    print("="*30)
    
    if disease_name == "Background" or disease_name == "Unknown":
        print(f"⚠️  Result: NOT A PLANT")
        print(f"   Confidence: {confidence*100:.2f}%")
        print("   Action: Please upload a valid Potato leaf.")
    else:
        print(f"🌿 Plant: Potato")
        print(f"🩺 Diagnosis: {disease_name}")
        print(f"📊 Confidence: {confidence*100:.2f}%")
        
    print("="*30 + "\n")

# ==========================================
# 5. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # --- COMMANDS ---
    
    # 1. UNCOMMENT TO TRAIN (Do this after adding the Background folder)
    # train_model()

    # 2. UNCOMMENT TO TEST (Do this after training)
    # predict_image("test_potato.jpg")
    pass