AgroVision: Plant Disease Detection System 🌿

AgroVision is a full-stack web application designed to help farmers detect potato plant diseases (Early Blight and Late Blight) using Deep Learning.

The system uses a Convolutional Neural Network (CNN) to analyze leaf images and provides instant diagnosis along with recommended treatments. It specifically addresses the "Closed-Set" problem by incorporating a Background Class to filter out non-plant images.

🚀 Features

Real-time Prediction: Instant analysis of leaf images.

High Accuracy: ~92% accuracy on the test set.

Robustness: Intelligently rejects random/irrelevant images (Noise Filtering).

Treatment Recommendations: Provides agronomist-approved solutions for detected diseases.

User-Friendly Interface: Clean React.js frontend with drag-and-drop functionality.

🛠️ Tech Stack

Frontend: React.js, Tailwind CSS, Lucide React

Backend: Python Flask

Deep Learning: TensorFlow (Keras), NumPy, Pillow

Dataset: PlantVillage (Potato Subset)

📂 Project Structure

/AgroVision
├── .venv/                 # Python Virtual Environment
├── MiniDataset/           # Training Data (Potato Classes + Background)
├── frontend/              # React Frontend Application
│   ├── public/
│   ├── src/
│   └── package.json
├── uploads/               # Temp storage for uploaded images
├── app.py                 # Flask Backend API
├── potato_doctor.py       # CNN Training Script
├── potato_model.h5        # Trained AI Model
├── class_names.json       # Mapping of Class Indices to Names
└── README.md              # Project Documentation


⚙️ Installation & Setup Guide

Follow these steps to run the project locally.

1. Clone the Repository

git clone [https://github.com/Hiteshkashyap04/Plant_disease_detection.git](https://github.com/Hiteshkashyap04/Plant_disease_detection.git)
cd Plant_disease_detection


2. Backend Setup (Python)

Navigate to the root directory.

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install tensorflow flask flask-cors numpy pillow


3. Frontend Setup (React)

Open a new terminal, navigate to the frontend folder, and install dependencies.

cd frontend
npm install


▶️ How to Run

You need to run the Backend and Frontend in two separate terminals.

Terminal 1: Start the Backend Server

# Make sure you are in the root folder and .venv is active
python app.py


The server will start at http://127.0.0.1:5000

Terminal 2: Start the React App

cd frontend
npm start


The app will open in your browser at http://localhost:3000

🧠 Model Training (Optional)

If you want to retrain the model with your own data:

Place your images in the MiniDataset folder.

Run the training script:

python potato_doctor.py


This will generate a new potato_model.h5 and class_names.json.

📸 Screenshots

1. Home Page

2. Disease Prediction

3. Error Handling (Non-Plant)

🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

👤 Author

Hitesh