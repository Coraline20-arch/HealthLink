import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the files
model = joblib.load('disease_model.pkl')
symptoms = joblib.load('symptoms_list.pkl')

st.set_page_config(page_title="Disease Predictor", page_icon="🩺")
st.title("🩺 AI Disease Prediction")
st.write("Select symptoms to see what the AI thinks.")

# Create the selection box
options = st.multiselect("What are your symptoms?", list(symptoms))

if st.button("Run Diagnosis"):
    # Create a link button to your Google Form
st.link_button("📋 Fill out Appointment Request Form", "https://forms.gle/TuHiwJz634roBahN8")
    # Prepare the data for the model
    input_data = np.zeros(len(symptoms))
    for s in options:
        # This finds where the symptom is in our list and marks it as "1" (True)
        index = np.where(symptoms == s)[0][0]
        input_data[index] = 1
    
    # Make the prediction
    prediction = model.predict([input_data])
    st.header(f"Result: {prediction[0]}")

# --- SPECIALIST DIRECTORY SECTION ---
st.markdown("---") # This adds a horizontal line to separate sections
st.header("🏢 Specialist Contact Directory")
st.write("If you already have a diagnosis, find the correct department below:")

# We create a dictionary (list) of the contact info
directory_data = {
    "Specialty": ["Dermatology", "Cardiology", "Endocrinology", "Neurology", "Gastroenterology"],
    "Clinic Name": ["Skin Health Center", "Heart & Vascular Inst.", "Metabolic Care Unit", "Neuro-Science Hub", "Digestive Health Clinic"],
    "Contact Info": ["555-0101", "555-0202", "555-0303", "555-0404", "555-0505"],
    "Email": ["skin@healthlink.com", "heart@healthlink.com", "endo@healthlink.com", "neuro@healthlink.com", "gi@healthlink.com"]
}

# This displays it as a beautiful, searchable table
st.table(directory_data)
