import streamlit as st

import streamlit as st
import joblib
import numpy as np

# Load the files
model = joblib.load('disease_model.pkl')
symptoms = joblib.load('symptoms_list.pkl')

st.set_page_config(page_title="Disease Predictor", page_icon="🩺")
st.title("🩺 AI Disease Prediction")
st.write("Select symptoms to see what the AI thinks.")

# Create the selection box
options = st.multiselect("What are your symptoms?", list(symptoms))

if st.button("Run Diagnosis"):
    # Prepare the data for the model
    input_data = np.zeros(len(symptoms))
    for s in options:
        # This finds where the symptom is in our list and marks it as "1" (True)
        index = np.where(symptoms == s)[0][0]
        input_data[index] = 1
    
    # Make the prediction
    prediction = model.predict([input_data])
    st.header(f"Result: {prediction[0]}")