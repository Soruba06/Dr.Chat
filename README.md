# Soruba06-Dr.Chat-mini-project
Web based AI first aid provider 

Project Name:DR.Chat

Purpose:
To assist users in managing medical emergencies by offering accurate first aid steps, symptom analysis, 
and additional support such as nearby hospital locations.
DR.Chat acts as a virtual health assistant available 24/7.

Core Features:

First Aid Assistance:
Provides step-by-step first aid instructions based on user queries or input symptoms.
Uses a trained model (firstaid_steps.h5) to ensure accuracy and reliability.

Symptom Analysis:
Accepts user-reported symptoms and predicts potential health conditions.
Aims to guide users in taking the right actions based on the severity of their condition.
Includes a disclaimer: "THIS IS A PREDICTION ONLY" for all symptom analysis outputs.

Image Recognition:
Allows users to upload images (e.g., wounds, rashes, burns).
Identifies the condition and suggests relevant first aid steps.
Uses pre-trained deep learning models (chatbot_model.h5 or other specific image recognition models).

Location-Based Services:
Helps users locate the nearest hospitals or clinics.
Uses geographic data to provide precise and accessible information for emergencies.

User-Friendly Interaction:
Implements a conversational interface powered by an NLP model for seamless user interaction.
Understands context and intent, ensuring personalized responses.

1..idea

2.dataset:-This folder likely contains datasets used for training, validating, or testing your machine learning models.

3.model(firstaid_steps.h5):-This file is a saved Keras model, which may be trained to predict or provide first aid steps based on user input 
                            or symptoms.
                            It includes the model's architecture, weights, and training configuration.
                            
4.chatbot_model.h5:-This is another Keras model, likely trained to handle the conversational logic of your chatbot, including intent 
                    recognition or response generation.

5.symptoms_trining.h5:-This file likely contains a Keras model trained to predict health conditions or analyze symptoms provided by users.

6.config.py:-A Python configuration file, typically used to store application settings, API keys, file paths, or other variables used across 
             your project.

This files are not include in this repository. Because this files are contain large file size. so ignore it. and also model(firstaid_steps.h5),chatbot_model.h5,symptoms_trining.h5 are need to train the model and automaticaly created by that training part(sympotoms_trining.py,train_model_image.py,train_model.py). 


