from flask import Flask, render_template, request, jsonify
import os
import speech_recognition as sr
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import warnings

app = Flask(__name__)

warnings.simplefilter("ignore")

data = pd.read_csv("Language Detection.csv")

X = data["Text"]
y = data["Language"]

le = LabelEncoder()
y = le.fit_transform(y)

data_list = []
for text in X:
    text = re.sub(r'[!@#$(),n"%^*?:;~`0-9]', ' ', text)
    text = re.sub(r'[[]]', ' ', text)
    text = text.lower()
    data_list.append(text)

cv = CountVectorizer()
X = cv.fit_transform(data_list).toarray()

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

model = MultinomialNB()
model.fit(x_train, y_train)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect_language', methods=['POST'])
def detect_language():
    if request.method == 'POST':
        if 'text' in request.form:
            text = request.form['text']
            x = cv.transform([text]).toarray()
            lang = model.predict(x)
            lang = le.inverse_transform(lang)
            return jsonify({'language': lang[0]})
        elif 'audio' in request.files:
            audio_file = request.files['audio']
            audio_file.save('temp_audio.wav')  # Save the audio file temporarily
            recognizer = sr.Recognizer()
            with sr.AudioFile('temp_audio.wav') as source:
                audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                x = cv.transform([text]).toarray()
                lang = model.predict(x)
                lang = le.inverse_transform(lang)
                os.remove('temp_audio.wav')  # Remove the temporary audio file
                return jsonify({'language': lang[0]})
            except Exception as e:
                os.remove('temp_audio.wav')  # Remove the temporary audio file
                return jsonify({'error': str(e)})
        else:
            return jsonify({'error': 'Invalid request'})


if __name__ == '__main__':
    app.run(debug=True)