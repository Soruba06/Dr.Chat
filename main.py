import json
import random
import numpy as np
import tensorflow as tf
import pickle

# Load trained model and tokenizer
model = tf.keras.models.load_model('firstaid_steps.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('label_encoder.pickle', 'rb') as enc_file:
    lbl_encoder = pickle.load(enc_file)

# Load first aid data
with open('intents.json') as file:
    data = json.load(file)


def get_response(user_input):
    max_len = 20
    result = model.predict(
        tf.keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([user_input]), maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for intent in data['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            response = format_response(response)
            follow_ups = intent.get('follow_ups', [])
            return response, follow_ups

    return "Sorry, I didn't understand that.", []


def format_response(response):
    # Assuming response is in plain text, format it as needed
    response = response.strip()
    return {"first_aid_steps": response}


def handle_follow_up(user_input):
    # Implement your follow-up handling logic here
    return "This is a follow-up response based on your input."


# This is the function that Flask will call
def chat(user_input):
    response, follow_ups = get_response(user_input)
    return {"response": response, "follow_ups": follow_ups}
