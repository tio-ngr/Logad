import sklearn
import numpy as np
import pandas as pd
import re
import string
from flask import Flask, render_template, request, jsonify
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import pickle

app = Flask(__name__)
global tfidf_vectorizer

# Load the pre-trained MLP model and TF-IDF Vectorizer
model_path = 'model/mlp_model.pkl'
vectorizer_path = 'model/vectorizer.pkl'

mlp_model = pickle.load(open(model_path, 'rb'))
tfidf_vectorizer = pickle.load(open(vectorizer_path, 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_kata = request.form['text_input']
        predicted_language, confidence_score = deteksi_bahasa(input_kata)
        return render_template('index.html', prediction=predicted_language, probability=confidence_score)

def deteksi_bahasa(input_kata):
    predicted_language = mlp_model.predict([input_kata])
    class_probabilities = mlp_model.predict_proba([input_kata])
    confidence_score = max(class_probabilities[0])
    return predicted_language[0], confidence_score

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)