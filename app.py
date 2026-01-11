import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Database Files
model = joblib.load('disease_model.pkl')
symptoms_list = joblib.load('symptoms_list.pkl')

st.set_page_config(page_title="Disease Predictor", page_icon="🩺")
st.title("🩺 HealthLink")
st.write("HealthLink AI is a machine-learning powered diagnostic tool designed to bridge the gap between symptooms and professional care. By analyzing user-reported data through a Random Forest algorithm, the app provides instant health insights and connects users directly to the correct medical specialists.")
st.write("This webapp is a science fair project by 10th Grade Students (Chisom and Mesooma Obi).")
st.write("Select symptoms to see what the AI thinks.")


# Selection box
options = st.multiselect("What are your symptoms?", list(symptoms_list))

# Results after button is clicked on
if st.button("Run Diagnosis"):
    # Data prep
    input_data = np.zeros(len(symptoms_list))
    for s in options:
        index = list(symptoms_list).index(s)
        input_data[index] = 1
    
    # Testing
    prediction = model.predict(input_data.reshape(1, -1))
    
    # Training
    result = prediction[0]
    
    # Displayed Result
    st.success(f"### Predicted Condition: {result}")
    
    # Specialist link button
    form_url = f"https://docs.google.com/forms/d/e/1FAIpQLSec-ev-zZ3KcUQW6A1eYBSl_MuAzqoZbImXYlvHzWcGYfK8_w/viewform?usp=header{result.replace(' ', '+')}"
    st.link_button("📋 Book Appointment for this Result", form_url)

# Doctor's view
if st.sidebar.checkbox("Specialist Login (Admin Only)"):
    password = st.sidebar.text_input("Enter Code", type="password")
    if password == "4421": # Password
        st.sidebar.success("Access Granted")
        st.sidebar.link_button("View Patient Queue", "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=drivesdk")
