from flask import Flask, render_template, request, jsonify
import joblib
import json
import os
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the trained model
model = joblib.load(os.path.join('model', 'RandomForest.joblib'))

# Load crop descriptions from JSON
with open(os.path.join('model', 'crop_descriptions.json'), 'r') as f:
    crop_descriptions = json.load(f)

# Initialize the scaler (use the same one that was used during training)
scaler = StandardScaler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input parameters from the form
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # Prepare the input data
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        # Scale the input data if necessary (use the same scaler as in training)
        input_data_scaled = scaler.fit_transform(input_data)

        # Predict the probabilities for each crop (if using classification model)
        probabilities = model.predict_proba(input_data_scaled)[0]  # Get probabilities for each class

        # Get the indices of the top 5 crops with the highest probabilities
        top_5_indices = np.argsort(probabilities)[-5:][::-1]  # Sort and pick the top 5 indices

        # Fetch crop names based on top 5 indices
        crop_names = model.classes_[top_5_indices]  # Get crop names corresponding to top 5 indices

        # Prepare the crop data (name, description, and image)
        crops_info = []
        for crop_name in crop_names:
            crop_info = {}

            # Retrieve description from the crop_descriptions.json file
            crop_info['name'] = crop_name
            crop_info['description'] = crop_descriptions.get(crop_name, "No description available.")

            # Retrieve image path (use original crop name here, no .lower())
            image_filename = f'images/{crop_name}.png'  # Correct file path based on crop name
            crop_info['image'] = image_filename  # This will point to the correct image file

            crops_info.append(crop_info)

        return render_template('index.html', crops=crops_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
