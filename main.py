import urlfeatures
import string
import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 

char_list = string.punctuation

# Load the model
with open('final_model.pkl', 'rb') as file:
    model = pickle.load(file)

def extract_features(url):
    url_obj = urlfeatures.FeaturesOf(url)
    features = url_obj.get_features(char_list)
    return features

st.title('Phishing URL Prediction')

url = st.text_input('Enter the URL:')

if st.button('Predict'):
    if url:
        features = extract_features(url)
        prediction = model.predict([features])[0]
        if prediction is not None:
            if prediction == 1:
                st.write('The URL is predicted to be a phishing URL.')
            else:
                st.write('The URL is predicted to be a legitimate URL.')
        else:
            st.write('Model could not be loaded. Please check the logs for more details.')
    else:
        st.write('Please enter a URL.')


# url = "us.battle.net.ok.ppweb.asia/login/en/login.html"
# url_obj = urlfeatures.FeaturesOf(url)
# features = url_obj.get_features(char_list)
# prediction = model.predict([features])
# print(prediction[0])
