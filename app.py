import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the files
model = joblib.load('disease_model.pkl')
symptoms = joblib.load('symptoms_list.pkl')

st.set_page_config(page_title="Disease Predictor", page_icon="🩺")
st.title("🩺 HealthLink")
st.write("HealthLink AI is a machine-learning powered diagnostic tool designed to bridge the gap between symptooms and professional care. By analyzing user-reported data through a Random Forest algorithm, the app provides instant health insights and connects users directly to the correct medical specialists.")
st.write("This webapp is a science fair project by 10th Grade Students (Chisom and Mesooma Obi).")
st.write("Select symptoms to see what the AI thinks.")

# symptoms multiselect
options = st.multiselect("Select symptoms:", list(symptoms_list))

# Results
if st.button("Run Diagnosis"):
    input_data = np.zeros(len(symptoms_list))
    for s in options:
        index = list(symptoms_list).index(s)
        input_data[index] = 1
    
    prediction = model.predict(input_data.reshape(1, -1))

# Results 2
    result = prediction[0]
    
    st.success(f"### Predicted Condition: {result}")
    
# Book appointments  button
    form_url = f"https://docs.google.com/forms/d/e/YOUR_ID/viewform?entry.123={result}"
    st.link_button("📋 Book Appointment", form_url)

# "Doctor's view"
if st.sidebar.checkbox("Specialist Login (Admin Only)"):
    password = st.sidebar.text_input("Enter Code", type="password")
    if password == "4421": # Password
        st.sidebar.success("Access Granted")
        st.sidebar.link_button("View Patient Queue", "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=drivesdk")
