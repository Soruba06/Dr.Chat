import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

# Load model and tokenizer
model = tf.keras.models.load_model('symptoms_model.h5')
tokenizer = joblib.load('tokenizer.pkl')
le = joblib.load('label_encoder.pkl')

# Load and prepare data
with open('symptoms_data.json') as file:
    data = json.load(file)

# Create a dictionary mapping symptoms to tags
symptom_to_tag = {}
for entry in data:
    symptoms = entry['symptoms']
    tag = entry['tag']
    for symptom in symptoms:
        if symptom not in symptom_to_tag:
            symptom_to_tag[symptom] = set()
        symptom_to_tag[symptom].add(tag)

# Function to analyze symptoms
def analyze_symptoms(symptoms_list):
    symptoms_str = ' '.join(symptoms_list)
    symptoms_seq = tokenizer.texts_to_sequences([symptoms_str])
    symptoms_pad = pad_sequences(symptoms_seq, padding='post', maxlen=model.input_shape[1])

    # Predict and calculate probability
    prediction = model.predict(symptoms_pad)
    predicted_prob = np.max(prediction)
    predicted_tag = le.inverse_transform([np.argmax(prediction)])[0]

    # Adjust threshold as per requirement
    threshold = 0.90
    if predicted_prob > threshold:
        return predicted_tag, predicted_prob
    else:
        return 'Seek medical help', predicted_prob

# Function to check if symptoms match known situations
def check_symptoms_match(symptoms_list):
    matched_tags = set()
    for symptom in symptoms_list:
        if symptom in symptom_to_tag:
            matched_tags.update(symptom_to_tag[symptom])

    return matched_tags

# Function to handle follow-up questions
def handle_follow_up(question, previous_symptoms):
    # Provide responses based on previous symptoms
    # This is a simplified example; you might want to improve this based on context
    if 'antiseptic' in question.lower():
        return "An antiseptic solution is used to clean wounds and prevent infection. Examples include hydrogen peroxide or iodine."
    # Add more follow-up questions as needed
    return "Sorry, I don't have information on that."

# Example usage
if __name__ == "__main__":
    # Sample input
    user_symptoms = ["fever", "headache"]
    tag, prob = analyze_symptoms(user_symptoms)
    print(f"Diagnosis: {tag}, Probability: {prob}")

    # Handling follow-up
    follow_up_question = "What is an antiseptic solution?"
    response = handle_follow_up(follow_up_question, user_symptoms)
    print(f"Follow-up Response: {response}")

