from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import json

# Initialize the App
app = Flask(__name__)
CORS(app)  # Enables the React frontend to communicate with this backend

# Configuration
MODEL_PATH = 'potato_model.h5'
CLASSES_PATH = 'class_names.json'
UPLOAD_FOLDER = 'uploads'

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the Brains (Model & Class Names)
print("Loading Model... please wait.")
model = tf.keras.models.load_model(MODEL_PATH)

if os.path.exists(CLASSES_PATH):
    with open(CLASSES_PATH, 'r') as f:
        class_names = json.load(f)
    print(f"Model & Classes loaded: {class_names}")
else:
    print("ERROR: class_names.json not found. Did you train the model?")
    class_names = []

# Solution Database
def get_solution(disease_name):
    solutions = {
        "Potato___Early_blight": {
            "status": "infected",
            "treatment": "Prune infected leaves. Apply copper-based fungicides. Improve air circulation."
        },
        "Potato___Late_blight": {
            "status": "critical",
            "treatment": "Remove and destroy infected plants immediately. Use Mefenoxam fungicide. Do not compost."
        },
        "Potato___healthy": {
            "status": "healthy",
            "treatment": "Plant is healthy. Maintain regular watering and check for pests."
        }
    }
    return solutions.get(disease_name, {"status": "unknown", "treatment": "Consult an agronomist."})

@app.route('/', methods=['GET'])
def home():
    return "Plant Disease API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Preprocess the image (Same logic as training!)
        img = load_img(file_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # Make Prediction
        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        if confidence < 0.70:
            return jsonify({
                "disease": "Unknown Object",
                "confidence": confidence,
                "status": "error",
                "treatment": "The AI is unsure. Please ensure you uploaded a clear Potato leaf image."
            })
        predicted_class = class_names[predicted_index]
        solution_info = get_solution(predicted_class)

        # Return Result as JSON
        result = {
            "disease": predicted_class,
            "confidence": confidence,
            "status": solution_info['status'],
            "treatment": solution_info['treatment']
        }
        
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up: Remove the temp file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(port=5000, debug=True)