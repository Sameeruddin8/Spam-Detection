from flask import Flask, render_template, request
import pickle
import pandas 
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)

ps = PorterStemmer()

def transform_text(text):
    text = text.lower() #convert to lower case
    text = nltk.word_tokenize(text) #converting to tokens
    
    y = [] #for removing special characters
    for i in text:
        if i.isalnum():
            y.append(i)
    
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
         
    return " ".join(y)

model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict", methods = ['GET', 'POST'])
def predict():
    text = transform_text(request.form.get('sms'))
    vector = vectorizer.transform([text])
    result = model.predict(vector)
    probabilities = model.predict_proba(vector)[0]
    confidence = max(probabilities) * 100
    if result == 0:
        prediction = "Not Spam"
    else:
        prediction = "Spam"

    return render_template('index.html', predicteeeed=prediction, confidence=confidence)
if __name__ == '__main__':
    app.run(debug = True)
