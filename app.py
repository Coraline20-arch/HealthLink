import streamlit as st
import joblib
import numpy as np
import time

# 1. Page Configuration
st.set_page_config(page_title="HealthLink AI", page_icon="🩺", layout="centered")

# 2. Session State Initialization
if 'page' not in st.session_state:
    st.session_state.page = "home"

# 3. CSS for Mixed Colors & Sidebar Arrow Fix
st.markdown("""
    <style>
        /* Global Background and Base Text (Black) */
        .stApp {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            font-family: 'Segoe UI', sans-serif;
            color: black !important;
        }

        /* --- THE ARROW FIX --- */
        /* Targets the sidebar toggle arrow/chevron and makes it white */
        [data-testid="stSidebarCollapseButton"] svg {
            fill: white !important;
        }
        
        /* Targets the 'Open Sidebar' arrow when sidebar is closed */
        [data-testid="openSidebar"] svg {
            fill: white !important;
        }

        /* FORCE WHITE TEXT for Buttons */
        .stButton button p {
            color: white !important;
        }

        /* FORCE WHITE TEXT for Multiselect Label and Options */
        /* This makes 'Choose symptoms' and the selected symptoms white */
        .stMultiSelect label p, .stMultiSelect span, .stMultiSelect div {
            color: white !important;
        }
        
        /* Ensure headers and general paragraphs stay black */
        h1, h2, h3, p {
            color: black !important;
        }

        /* Design for the Portal Card */
        .portal-card {
            background: rgba(255, 255, 255, 0.25);
            padding: 40px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(12px);
            text-align: center;
            margin-bottom: 20px;
        }

        @keyframes heartBeat {
            0% { transform: scale(1); }
            15% { transform: scale(1.1); }
            30% { transform: scale(1); }
            45% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        .loader-heart {
            width: 80px; height: 80px; fill: #FF5A5F;
            animation: heartBeat 1.2s infinite;
            display: block; margin: auto;
        }
    </style>
    """, unsafe_allow_html=True)

# 4. Global Data Loading
model = joblib.load('disease_model.pkl')
symptoms_list = joblib.load('symptoms_list.pkl')

# --- VIEW 1: THE SPLASH SCREEN ---
if st.session_state.page == "home":
    st.markdown('<div class="portal-card">', unsafe_allow_html=True)
    st.title("🩺 HealthLink AI Portal")
    st.write("Bridging the gap between symptoms and specialist care.")
    st.write("A 10th-grade research project by **Chisom & Mesooma Obi**")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 Patients")
        st.info("Experience our AI-driven diagnostic tool to analyze your symptoms.")
        if st.button("🚀 Enter Diagnostics", use_container_width=True):
            st.session_state.page = "app"
            st.rerun()

    with col2:
        st.subheader("🏥 Specialists")
        st.write("Access the secure patient queue and dashboard.")
        password = st.text_input("Enter Admin Code", type="password")
        if password == "4421":
            st.success("Access Granted")
            st.link_button("📂 Open Patient Queue", "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=sharing", use_container_width=True)

# --- VIEW 2: THE DIAGNOSTICS APP ---
else:
    # Sidebar back button
    if st.sidebar.button("⬅️ Back to Portal Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🔍 Symptom Analysis")
    
    options = st.multiselect("Select all symptoms you are experiencing:", list(symptoms_list))

    if st.button("Run AI Diagnosis"):
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            st.markdown("""
                <div style="padding: 30px; text-align: center;">
                    <svg class="loader-heart" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
