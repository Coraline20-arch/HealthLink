import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time

# 1. Page Configuration (MUST be the very first Streamlit command)
st.set_page_config(page_title="Disease Predictor", page_icon="🩺")

# 3. Load the AI files
model = joblib.load('disease_model.pkl')
symptoms_list = joblib.load('symptoms_list.pkl')

# 4. App Header
st.title("🩺 HealthLink")
st.write("HealthLink AI is a machine-learning powered diagnostic tool designed to bridge the gap between symptoms and professional care. This is a science fair project by Chisom and Mesooma Obi.")

# 5. Symptom Selection
options = st.multiselect("What are your symptoms?", list(symptoms_list))

# 6. Diagnosis Logic
if st.button("Run Diagnosis"):
    # --- This is the Loading Screen ---
    with st.spinner("Wait... HealthLink AI is analyzing your symptoms..."):
        time.sleep(1.5)  # Makes the loading screen visible
        
        # Prepare the data
        input_data = np.zeros(len(symptoms_list))
        for s in options:
            index = list(symptoms_list).index(s)
            input_data[index] = 1
        
        # Run the model
        prediction = model.predict(input_data.reshape(1, -1))
        result = prediction[0]
    
    # Show the result after the loading screen finishes
    st.success(f"### Predicted Condition: {result}")
    
    # Triage Accessory
    urgent_diseases = ['Heart attack', 'Stroke', 'Malaria', 'Typhoid']
    if result in urgent_diseases:
        st.error("🚨 **High Priority:** Please seek immediate medical attention.")
    else:
        st.info("🟢 **Standard Priority:** Follow up with a specialist.")

    # Link to the Google Form
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSec-ev-zZ3KcUQW6A1eYBSl_MuAzqoZbImXYlvHzWcGYfK8_w/viewform?usp=header"
    st.link_button("📋 Book Appointment for this Result", form_url)

# 7. Specialist Portal (Sidebar)
st.sidebar.markdown("---")
if st.sidebar.checkbox("Specialist Login (Admin Only)"):
    password = st.sidebar.text_input("Enter Code", type="password")
    if password == "4421":
        st.sidebar.success("Access Granted")
        st.sidebar.link_button("View Patient Queue", "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=sharing")
