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
    # Prepare the data
    input_data = np.zeros(len(symptoms_list))
    for s in options:
        index = list(symptoms_list).index(s)
        input_data[index] = 1
    
    # Run the model
    prediction = model.predict(input_data.reshape(1, -1))
    result = prediction[0]
    
    # Show the result
    st.success(f"### Predicted Condition: {result}")
    
    # Pre-filled Form Link
    # Note: Replace 'entry.123' with your actual Google Form entry ID
    form_url = f"https://docs.google.com/forms/d/e/1FAIpQLSc_EXAMPLE/viewform?usp=pp_url&entry.1205841980{result.replace(' ', '+')}"
    st.link_button("📋 Book Appointment for this Result", form_url)

# 6. Specialist Portal (Sidebar)
st.sidebar.markdown("---")
if st.sidebar.checkbox("Specialist Login (Admin Only)"):
    password = st.sidebar.text_input("Enter Code", type="password")
    if password == "4421":
        st.sidebar.success("Access Granted")
        st.sidebar.link_button("View Patient Queue", "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=drivesdk")
