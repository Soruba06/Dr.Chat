# predict_image.py
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import json
from io import BytesIO

# Load the trained model
model = tf.keras.models.load_model('model/first_aid_model.h5')

# Load the first aid steps from JSON
with open('first_aid_steps.json', 'r') as file:
    first_aid_steps = json.load(file)

def preprocess_image(img_file):
    img = image.load_img(img_file, target_size=(150, 150))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(img_file):
    img_array = preprocess_image(img_file)
    # Predict the class
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)

    # Load class labels
    class_labels = list(first_aid_steps.keys())

    # Find the first aid steps for the predicted class
    first_aid_label = class_labels[predicted_class]
    steps = first_aid_steps.get(first_aid_label, "First aid steps not found")

    return first_aid_label, steps

def handle_file(file):
    if not file:
        raise ValueError("No file provided")

    # Convert the file to an in-memory file-like object
    img_file = BytesIO(file.read())
    return img_file
