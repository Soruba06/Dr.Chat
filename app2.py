from flask import Flask, request, jsonify, send_from_directory
from main import chat, handle_follow_up
from predict_symptoms import analyze_symptoms, check_symptoms_match
from predict_image import predict_image, handle_file
import os

app = Flask(__name__)

# Serve the index_new.html file (Main content page)
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index_new.html')

# Endpoint for First Aid Steps
@app.route('/first-aid', methods=['POST'])
def get_first_aid_steps():
    data = request.json
    user_input = data.get('user_input', '')

    # Handle follow-up if needed
    if 'follow_up' in data and data['follow_up']:
        response = handle_follow_up(user_input)
    else:
        response_data = chat(user_input)
        response = response_data["response"]
        follow_ups = response_data["follow_ups"]
        return jsonify({"response": response, "follow_ups": follow_ups})

    return jsonify({"response": response})

# Endpoint for Symptom Analysis
@app.route('/analyze-symptoms', methods=['POST'])
def analyze_symptoms_route():
    data = request.json
    symptoms_list = data.get('symptoms', [])

    if len(symptoms_list) < 2:
        return jsonify({"message": "Please provide at least 2 symptoms."}), 400

    matched_tags = check_symptoms_match(symptoms_list)

    if len(matched_tags) == 1:
        tag = matched_tags.pop()
        return jsonify({"possible_situation": tag, "confidence": "N/A"})
    elif len(matched_tags) > 1:
        tag, probability = analyze_symptoms(symptoms_list)
        if probability > 0.90:
            return jsonify({"possible_situation": tag, "confidence": probability})
        else:
            return jsonify({"message": "Symptoms are not clear. Seek medical help."})
    else:
        tag, probability = analyze_symptoms(symptoms_list)
        if probability > 0.90:
            return jsonify({"possible_situation": tag, "confidence": probability})
        else:
            return jsonify({"message": "Symptoms are not clear. Seek medical help."})

# Endpoint for Image Prediction
@app.route('/predict-image', methods=['POST'])
def predict_image_route():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    try:
        # Handle file and predict the situation
        img_file = handle_file(file)
        label, steps = predict_image(img_file)
        return jsonify({"predicted_situation": label, "first_aid_steps": steps})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)  # API 2 runs on port 5001
