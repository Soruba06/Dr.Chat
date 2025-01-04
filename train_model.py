import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder

# Load the JSON file
with open('intents.json') as file:
    data = json.load(file)

# Extracting data
training_sentences = []
training_labels = []
classes = []
responses = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])

    if intent['tag'] not in classes:
        classes.append(intent['tag'])

# Encoding the labels
lbl_encoder = LabelEncoder()
training_labels = lbl_encoder.fit_transform(training_labels)

# Tokenize and prepare text data
vocab_size = 1000
embedding_dim = 16
max_len = 20
trunc_type = 'post'
oov_tok = "<OOV>"

tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_len, truncating=trunc_type)

# Model building
model = Sequential()
model.add(tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(Dropout(0.2))
model.add(tf.keras.layers.GlobalAveragePooling1D())
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(16, activation='relu'))
model.add(Dense(len(classes), activation='softmax'))

# Model compile
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Model training
model.fit(padded_sequences, np.array(training_labels), epochs=500)

# Save the model
model.save("firstaid_steps.h5")

# Save the fitted tokenizer and label encoder
import pickle

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('label_encoder.pickle', 'wb') as enc_file:
    pickle.dump(lbl_encoder, enc_file, protocol=pickle.HIGHEST_PROTOCOL)
