import streamlit as st
import joblib
import numpy as np
import time

# Initialize session state so the app remembers if we've "started" or not
if 'started' not in st.session_state:
    st.session_state.started = False

# --- 1. THE SPLASH SCREEN ---
if not st.session_state.started:
    # Mesooma's CSS for the full-screen effect
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .welcome-container {
                text-align: center;
                padding: 50px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        </style>
        <div class="welcome-container">
            <h1 style="color: #444; font-size: 3rem;">🩺 HealthLink AI</h1>
            <p style="color: #555; font-size: 1.2rem;">Advanced Symptom Analysis & Specialist Triage</p>
        </div>
    """, unsafe_allow_html=True)

    st.write(" ") # Spacing
    if st.button("🚀 Begin Medical Scan", use_container_width=True):
        # When clicked, show the heartbeat loader then switch states
        with st.spinner("Initializing Neural Networks..."):
            time.sleep(2) 
            st.session_state.started = True
            st.rerun()

# --- 2. THE MAIN APP (Only runs after 'Begin' is clicked) ---
else:
    # Put all your original App code (Title, Multiselect, Model logic) here!
    st.sidebar.button("🏠 Back to Home", on_click=lambda: st.session_state.update({"started": False}))
    
    # ... rest of your code ...

# 1. Page Configuration
st.set_page_config(page_title="HealthLink AI", page_icon="🩺")

# 2. INTEGRATING Mesooma'S CSS (Design & Animations)
st.markdown("""
    <style>
        /* Mesooma's Background & Font */
        .stApp {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            font-family: 'Segoe UI', sans-serif;
        }

        /* The Heartbeat Animation */
        @keyframes heartBeat {
            0% { transform: scale(1); }
            15% { transform: scale(1.1); }
            30% { transform: scale(1); }
            45% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        .loader-heart {
            width: 80px;
            height: 80px;
            fill: #FF5A5F;
            animation: heartBeat 1.2s infinite ease-in-out;
            display: block;
            margin: auto;
        }

        .loader-text {
            text-align: center;
            color: #444;
            font-size: 1.3rem;
            font-weight: 500;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. Load AI files
model = joblib.load('disease_model.pkl')
symptoms_list = joblib.load('symptoms_list.pkl')

# 4. App Header (Mesooma's Welcome Screen style)
st.title("🩺 HealthLink")
st.markdown("<h3 style='color: #444;'>Ready to analyze your vitals?</h3>", unsafe_allow_html=True)

# 5. Symptom Selection
options = st.multiselect("What are your symptoms?", list(symptoms_list))

# 6. Diagnosis Logic (With Mesooma's Loading Screen)
if st.button("Begin Scan"): # Renamed to match Mesooma's button
    
    # Create a placeholder for the Mesooma's loading screen
    loading_placeholder = st.empty()
    
    with loading_placeholder.container():
        # This is your Mesooma's SVG Heart + Animation
        st.markdown("""
            <div style="padding: 50px;">
                <svg class="loader-heart" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                </svg>
                <div class="loader-text">Syncing Data...</div>
            </div>
        """, unsafe_allow_html=True)
        
        # AI Processing
        time.sleep(3.5) # Matches her HTML timer
        input_data = np.zeros(len(symptoms_list))
        for s in options:
            index = list(symptoms_list).index(s)
            input_data[index] = 1
        prediction = model.predict(input_data.reshape(1, -1))
        result = prediction[0]

    # Clear the loading screen
    loading_placeholder.empty()

    # Show the "Dashboard" (Streamlit Results)
    st.balloons()
    st.markdown("<h1 style='color: #2D9CDB;'>Analysis Complete</h1>", unsafe_allow_html=True)
    st.success(f"### Predicted Condition: {result}")
    
    # Triage and Link
    urgent_diseases = ['Heart attack', 'Stroke', 'Malaria', 'Typhoid']
    if result in urgent_diseases:
        st.error("🚨 **High Priority:** Please seek immediate medical attention.")
    else:
        st.info("🟢 **Standard Priority:** Follow up with a specialist.")

    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSec-ev-zZ3KcUQW6A1eYBSl_MuAzqoZbImXYlvHzWcGYfK8_w/viewform?usp=header"
    st.link_button("🏥 Connect to Specialist via HealthLink Cloud", form_url, type="primary")

# 7. Sidebar
st.sidebar.title("💡 Health Tips")
st.sidebar.info("- Drink plenty of water.\n- Track symptoms.\n- If symptoms worsen, call a doctor.")

if st.sidebar.checkbox("Specialist Login (Admin Only)"):
    password = st.sidebar.text_input("Enter Code", type="password")
    if password == "4421":
        st.sidebar.success("Access Granted")
        st.sidebar.link_button("View Patient Queue", "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=sharing")

# Disclaimer
st.markdown("---")
st.caption("⚠️ Disclaimer: Student research project. Not for medical advice.")
