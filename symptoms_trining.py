import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

# Load and prepare data
with open('symptoms_data.json') as file:
    data = json.load(file)

# Extract symptoms and tags
symptoms_list = [entry['symptoms'] for entry in data]
tags = [entry['tag'] for entry in data]

# Flatten symptoms and create a list of all symptoms and their tags
all_symptoms = []
all_tags = []

for symptom_group, tag in zip(symptoms_list, tags):
    for symptom in symptom_group:
        all_symptoms.append(symptom)
        all_tags.append(tag)

# Tokenization and padding
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_symptoms)
X_seq = tokenizer.texts_to_sequences(all_symptoms)
X_pad = pad_sequences(X_seq, padding='post')

# Encode tags
le = LabelEncoder()
y_encoded = le.fit_transform(all_tags)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_pad, y_encoded, test_size=0.2, random_state=42)

# Build and train model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64, input_length=X_pad.shape[1]),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(le.classes_), activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test))

# Save model and tokenizer
model.save('symptoms_model.h5')
with open('tokenizer.pkl', 'wb') as file:
    joblib.dump(tokenizer, file)
with open('label_encoder.pkl', 'wb') as file:
    joblib.dump(le, file)
