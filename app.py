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

# Create the selection box
options = st.multiselect("What are your symptoms?", list(symptoms))

if st.button("Run Diagnosis"):
    # ... your prediction code ...
    result = prediction[0]
    specialist = doctor_map.get(result, "General Physician")
    
    st.success(f"Predicted: {result}")
    st.info(f"Recommended Specialist: {specialist}")

    # The Link: This connects the AI result to your Form
    # entry.111 might be 'Disease' and entry.222 might be 'Specialist'
    form_link = f"https://forms.gle/FpaSwB9gvSEydsDq9entry.111={result}&entry.222={specialist}"
    
    st.link_button(f"Contact {specialist} regarding {result}", form_link)


# 1. Your Base Form Link (replace with yours)
base_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSec-ev-zZ3KcUQW6A1eYBSl_MuAzqoZbImXYlvHzWcGYfK8_w/viewform?usp=header"


# Add this to your sidebar for the "Doctor's view"
if st.sidebar.checkbox("Specialist Login (Admin Only)"):
    password = st.sidebar.text_input("Enter Code", type="password")
    if password == "4421": # Simple code for the fair
        st.sidebar.success("Access Granted")
        st.sidebar.link_button("View Patient Queue", "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=drivesdk")
