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

# 1. Your Base Form Link (replace with yours)
base_form_url = "https://forms.gle/FpaSwB9gvSEydsDq9"

# 2. Add the links to your data
directory_data = {
    "Specialty": ["Dermatology", "Cardiology", "Endocrinology"],
    "Clinic Name": ["Skin Health Center", "Heart Institute", "Metabolic Care"],
    # We create a link for each row that "pre-fills" the specialty in the form
    "Action": [
        f"[Book Dermatology]({base_form_url}Dermatology)",
        f"[Book Cardiology]({base_form_url}Cardiology)",
        f"[Book Endocrinology]({base_form_url}Endocrinology)"
    ]
}

st.table(directory_data)
