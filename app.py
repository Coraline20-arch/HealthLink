import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time

# 1. Page Configuration (MUST be the very first Streamlit command)
st.set_page_config(page_title="HealthLink AI", page_icon="🩺")

# 3. Load the AI files
model = joblib.load('disease_model.pkl')
symptoms_list = joblib.load('symptoms_list.pkl')

# 4. App Header
st.title("🩺 HealthLink")
st.write("HealthLink AI is a machine-learning powered diagnostic tool designed to bridge the gap between symptoms and professional care. This is a science fair project by Chisom and Mesooma Obi.")

st.subheader("How to get started:")
col1, col2, col3 = st.columns(3)
col1.metric("Step 1", "Select Symptoms")
col2.metric("Step 2", "Run AI Diagnosis")
col3.metric("Step 3", "Book Specialist")

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
   # A more urgent-looking button container
st.info("💡 **Next Step:** To confirm this result with a human doctor, use the portal below.")
st.link_button("🏥 Connect to Specialist via HealthLink Cloud", form_url, type="primary")

# 7. Specialist Portal (Sidebar)
st.sidebar.markdown("---")
if st.sidebar.checkbox("Specialist Login (Admin Only)"):
    password = st.sidebar.text_input("Enter Code", type="password")
    if password == "4421":
        st.sidebar.success("Access Granted")
        st.sidebar.link_button("View Patient Queue", "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=sharing")

st.sidebar.title("💡 Health Tips")
st.sidebar.info("""
- Drink plenty of water.
- Track how long you've felt symptoms.
- If symptoms worsen, contact a doctor immediately.
""")
st.sidebar.header("📊 Database Statistics")
st.sidebar.write(f"**Conditions Covered:** {len(model.classes_)}")
st.sidebar.write(f"**Symptom Variations:** {len(symptoms_list)}")

# Add a "Pulse" divider
st.sidebar.markdown("---")
st.sidebar.write("📈 *System Status: Active*")

st.markdown("---")
st.caption("⚠️ **Disclaimer:** HealthLink AI is a student research project for educational purposes. "
           "It is not a substitute for professional medical advice, diagnosis, or treatment.")

