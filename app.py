import streamlit as st
import joblib
import numpy as np
import pandas as pd

# 1. Page Configuration (MUST be at the top)
st.set_page_config(page_title="HealthLink AI", page_icon="🩺")

# 2. Load the files
model = joblib.load('disease_model.pkl')
symptoms_list = joblib.load('symptoms_list.pkl')

# 3. App Header
st.title("🩺 HealthLink")
st.write("HealthLink AI is a machine-learning powered diagnostic tool designed to bridge the gap between symptoms and professional care. By analyzing user-reported data through a Random Forest algorithm, the app provides instant health insights and connects users directly to the correct medical specialists.")
st.write("This webapp is a science fair project by 10th Grade Students (Chisom and Mesooma Obi).")
st.write("Select symptoms to see what the AI thinks.")

# 4. Symptom Selection
options = st.multiselect("What are your symptoms?", list(symptoms_list))

# 5. Diagnosis Logic (Everything must stay inside this 'if' block)
if st.button("Run Diagnosis"):
    # Loading Screen
    with st.spinner("Clarity in every heartbeat.."):
        # Put a tiny sleep timer here so the user can actually see the message
        import time
        time.sleep(1.5) 
        
        # All your existing code goes inside this block:
        input_data = np.zeros(len(symptoms_list))
        for s in options:
            index = list(symptoms_list).index(s)
            input_data[index] = 1
        
        prediction = model.predict(input_data.reshape(1, -1))
        result = prediction[0]

    # The spinner disappears here, and the result pops up!
    st.success(f"### Predicted Condition: {result}")
    
    # Traige
    urgent_diseases = ['Heart attack', 'Stroke', 'Malaria', 'Typhoid']
    if result in urgent_diseases:
        st.error("🚨 **High Priority:** Please seek immediate medical attention.")
    else:
        st.info("🟢 **Standard Priority:** Follow up with a specialist via the form below.")
    
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSec-ev-zZ3KcUQW6A1eYBSl_MuAzqoZbImXYlvHzWcGYfK8_w/viewform?usp=header"
    st.link_button("📋 Book Appointment for this Result", form_url)

st.sidebar.error("🆘 **EMERGENCY?**")
if st.sidebar.button("Find Nearest Hospital"):
    # This opens Google Maps to search for hospitals near the user
    st.sidebar.link_button("📍 Open Hospital Map", "https://www.google.com/maps/search/hospital+near+me")

# "Doctor's view"
if st.sidebar.checkbox("Specialist Login (Admin Only)"):
    password = st.sidebar.text_input("Enter Code", type="password")
    if password == "4421": # Your Code
        st.sidebar.success("Access Granted  'When opening, please right-click and click on Open Link in a New Tab'.")
        
        # Use st.link_button instead of st.button
        st.sidebar.link_button(
            "📂 View Patient Queue", 
            "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=sharing"
        )
