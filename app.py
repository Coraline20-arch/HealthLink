import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time
import re
import base64
import os
from datetime import datetime, timedelta

# =========================================================
# 1. Page Configuration
# =========================================================
st.set_page_config(page_title="HealthLink AI", page_icon="🩺", layout="centered")

# =========================================================
# 2. Session State Initialization
# =========================================================
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'history' not in st.session_state:
    st.session_state.history = []   # stores past diagnoses
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# --- Therapeutics / Collie Session States ---
if 'collie_messages' not in st.session_state:
    st.session_state.collie_messages = [
        {"role": "assistant", "content": "Hi! I'm Collie, your Therapeutics & Wellness companion 🌿 How are you feeling today?"}
    ]
if 'warning_count' not in st.session_state:
    st.session_state.warning_count = 0
if 'ban_expires_at' not in st.session_state:
    st.session_state.ban_expires_at = None

# =========================================================
# 3. Helper Functions & Mascot Rendering
# =========================================================
def get_image_base64(file_path):
    """Converts local image files (PNG/GIF) to base64 for html display."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def render_mascot(name, image_path, fallback_emoji, width=120):
    """Renders avatar PNGs (animated or static) with a smooth fallback if file missing."""
    b64_str = get_image_base64(image_path)
    if b64_str:
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 10px;">
                <img src="data:image/png;base64,{b64_str}" width="{width}px" style="border-radius: 50%; border: 3px solid #92BCD4; padding: 4px; background: white;" alt="{name}">
                <p style="font-weight: bold; margin-top: 4px; color: black !important;">{name}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 10px;">
                <span style="font-size: 60px;">{fallback_emoji}</span>
                <p style="font-weight: bold; margin-top: 4px; color: black !important;">{name}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def show_splash_screen(mascot_name, image_path, fallback_emoji, message, bg_color="#92BCD4"):
    """Displays a full portal transition splash screen before loading a view."""
    splash_placeholder = st.empty()
    b64_str = get_image_base64(image_path)
    
    avatar_html = (
        f'<img src="data:image/png;base64,{b64_str}" width="120px" style="border-radius: 50%; background: white; padding: 5px;" class="splash-pulse">'
        if b64_str else f'<span style="font-size: 80px;" class="splash-pulse">{fallback_emoji}</span>'
    )
    
    with splash_placeholder.container():
        st.markdown(f"""
            <div style="
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background: linear-gradient(135deg, {bg_color} 0%, #ffffff 100%);
                z-index: 99999;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;">
                {avatar_html}
                <h2 style="color: black !important; margin-top: 20px;">Connecting to {mascot_name}...</h2>
                <p style="color: #333 !important; font-size: 18px;">{message}</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1.8)
    splash_placeholder.empty()

def check_flirtatious_intent(text):
    """Detects romantic or inappropriate advances."""
    patterns = [
        r"\b(love you|date me|be my girlfriend|marry me|cutie|beautiful|kiss|hot|sexy)\b",
        r"\b(you('re| are) (pretty|cute|gorgeous|attractive))\b",
        r"\b(go out with me|single\?)\b"
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

# =========================================================
# 4. Multi-language Text Dictionary
# =========================================================
TEXT = {
    "English": {
        "welcome_title": "🩺 HealthLink AI Portal",
        "welcome_sub": "Bridging the gap between symptoms and specialist care.",
        "patients_header": "👤 Patients",
        "patients_info": "Experience our AI-driven diagnostic tool to analyze your symptoms.",
        "enter_button": "🚀 Enter Diagnostics",
        "therapeutics_header": "🌿 Therapeutics",
        "therapeutics_info": "Chat with Collie for mood support, mental well-being, and lifestyle guidance.",
        "enter_therapeutics": "💬 Chat with Collie",
        "specialists_header": "🏥 Specialists",
        "specialists_sub": "Access the secure patient queue and dashboard.",
        "admin_code": "Enter Admin Code",
        "diagnosis_title": "🔍 Symptom Analysis with Ellyse",
        "select_symptoms": "Select all symptoms you are experiencing:",
        "search_placeholder": "Search symptoms...",
        "severity_label": "Rate the severity of each symptom:",
        "run_button": "Run AI Diagnosis",
        "loading_text": "AI is cross-referencing symptom patterns...",
        "predicted": "Predicted Condition",
        "confidence": "Model Confidence",
        "speed": "Processing Speed",
        "urgent": "🚨 Urgent Notice: High-priority condition detected. Seek emergency care immediately.",
        "standard": "🟢 Standard Notice: Specialist follow-up recommended within a few days.",
        "book_button": "📋 Book Specialist Appointment",
        "download_summary": "⬇️ Download My Summary",
        "history_header": "🕓 Your Past Checks (this session)",
        "no_history": "No past checks yet.",
        "disclaimer": "⚠️ Educational purposes only; not a substitute for professional medical advice.",
        "back_button": "⬅️ Back to Portal Home",
    },
    "Pidgin": {
        "welcome_title": "🩺 HealthLink AI Portal",
        "welcome_sub": "We dey connect your symptoms with specialist wey fit help you.",
        "patients_header": "👤 Patients",
        "patients_info": "Use our AI tool check wetin dey worry you.",
        "enter_button": "🚀 Enter Diagnostics",
        "therapeutics_header": "🌿 Therapeutics",
        "therapeutics_info": "Follow Collie talk for mood support and general body wellness.",
        "enter_therapeutics": "💬 Talk with Collie",
        "specialists_header": "🏥 Specialists",
        "specialists_sub": "Enter the secure patient queue and dashboard.",
        "admin_code": "Enter Admin Code",
        "diagnosis_title": "🔍 Symptom Check with Ellyse",
        "select_symptoms": "Choose all the symptoms wey you dey feel:",
        "search_placeholder": "Find symptom...",
        "severity_label": "Rate how bad each symptom be:",
        "run_button": "Run AI Check",
        "loading_text": "AI dey check your symptoms well well...",
        "predicted": "Wetin AI Think E Be",
        "confidence": "AI Confidence",
        "speed": "Speed",
        "urgent": "🚨 Serious Notice: Go hospital sharp sharp or call emergency number.",
        "standard": "🟢 Normal Notice: E good make you see specialist within few days.",
        "book_button": "📋 Book Specialist Appointment",
        "download_summary": "⬇️ Download My Summary",
        "history_header": "🕓 Your Past Checks (this session)",
        "no_history": "No past check yet.",
        "disclaimer": "⚠️ Learning purpose only, e no be replacement for real doctor advice.",
        "back_button": "⬅️ Go Back to Home",
    },
}

def t(key):
    lang = st.session_state.get("lang", "English")
    return TEXT.get(lang, TEXT["English"]).get(key, TEXT["English"].get(key, key))

# =========================================================
# 5. CSS Styling
# =========================================================
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #92BCD4 0%, #ffffff 100%);
            font-family: 'Segoe UI', sans-serif;
            color: black !important;
        }
        [data-testid="stSidebarCollapseButton"] svg, [data-testid="openSidebar"] svg {
            fill: white !important;
        }
        .stButton button p {
            color: white !important;
        }
        .stMultiSelect label p, .stMultiSelect span, .stMultiSelect div {
            color: white !important;
        }
        h1, h2, h3, p {
            color: black !important;
        }
        .portal-card {
            background: rgba(255, 255, 255, 0.35);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(12px);
            text-align: center;
            margin-bottom: 20px;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        .splash-pulse {
            animation: pulse 1.5s infinite ease-in-out;
            display: inline-block;
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

# =========================================================
# 6. Global Data Loading
# =========================================================
try:
    model = joblib.load('disease_model.pkl')
    symptoms_list = list(joblib.load('symptoms_list.pkl'))
except Exception:
    symptoms_list = ["Fever", "Cough", "Headache", "Fatigue"]
    model = None

URGENT_DISEASES = ['Heart attack', 'Stroke', 'Malaria', 'Typhoid']

# =========================================================
# 7. Sidebar Navigation
# =========================================================
st.sidebar.selectbox(
    "🌐 Language / Èdè / Harshe / Asụsụ",
    options=list(TEXT.keys()),
    key="lang",
)

# =========================================================
# VIEW 1: HOME PORTAL (3 OPTIONS)
# =========================================================
if st.session_state.page == "home":
    st.markdown('<div class="portal-card">', unsafe_allow_html=True)
    st.title(t("welcome_title"))
    st.write(t("welcome_sub"))
    st.write("A 10th-grade research project by **Chisom & Mesooma Obi**")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        render_mascot("Ellyse", "assets/ellyse.png", "🩺", width=100)
        st.subheader(t("patients_header"))
        st.caption(t("patients_info"))
        if st.button(t("enter_button"), use_container_width=True):
            show_splash_screen("Ellyse", "assets/ellyse.png", "🩺", "Preparing Clinical Diagnostic Engine...", bg_color="#92BCD4")
            st.session_state.page = "app"
            st.rerun()

    with col2:
        render_mascot("Collie", "assets/collie.png", "🌿", width=100)
        st.subheader(t("therapeutics_header"))
        st.caption(t("therapeutics_info"))
        if st.button(t("enter_therapeutics"), use_container_width=True):
            show_splash_screen("Collie", "assets/collie.png", "🌿", "Opening Your Mindful Space...", bg_color="#B8E0D2")
            st.session_state.page = "therapeutics"
            st.rerun()

    with col3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader(t("specialists_header"))
        st.caption(t("specialists_sub"))
        password = st.text_input(t("admin_code"), type="password")
        real_admin_code = st.secrets.get("admin_code", "4421")

        if password and password == real_admin_code:
            st.success("Access Granted.")
            sheet_url = "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=sharing"
            st.link_button("📂 Open Patient Queue", sheet_url, use_container_width=True)
        elif password:
            st.error("Incorrect code.")

# =========================================================
# VIEW 2: DIAGNOSTICS APP (ELLYSE)
# =========================================================
elif st.session_state.page == "app":
    if st.sidebar.button(t("back_button")):
        st.session_state.page = "home"
        st.rerun()

    col_head, col_avatar = st.columns([3, 1])
    with col_head:
        st.title(t("diagnosis_title"))
    with col_avatar:
        render_mascot("Ellyse", "assets/ellyse.png", "🩺", width=90)

    search_term = st.text_input("🔎 " + t("search_placeholder"))
    filtered_symptoms = [s for s in symptoms_list if search_term.lower() in s.lower()] if search_term else symptoms_list
    options = st.multiselect(t("select_symptoms"), filtered_symptoms)

    severities = {}
    if options:
        st.write(t("severity_label"))
        for symptom in options:
            severities[symptom] = st.select_slider(
                symptom, options=["Mild", "Moderate", "Severe"], value="Moderate",
                key=f"severity_{symptom}"
            )

    if st.button(t("run_button")):
        if not options:
            st.warning("Please select at least one symptom first.")
        elif model is None:
            st.error("Model missing in setup context.")
        else:
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st.markdown(f"""
                    <div style="padding: 20px; text-align: center;">
                        <svg class="loader-heart" viewBox="0 0 24 24">
                            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                        </svg>
                        <p style="color: black; font-weight: 500;">{t("loading_text")}</p>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(1.5)

            loading_placeholder.empty()

            input_data = np.zeros(len(symptoms_list))
            for s in options:
                input_data[symptoms_list.index(s)] = 1

            input_vector = input_data.reshape(1, -1)
            result = model.predict(input_vector)[0]

            st.success(f"### {t('predicted')}: {result}")

            is_urgent = result in URGENT_DISEASES
            if is_urgent:
                st.error(t("urgent"))
            else:
                st.info(t("standard"))

            record = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Symptoms": ", ".join(options),
                "Severity": ", ".join(f"{s}: {severities[s]}" for s in options),
                "Predicted Condition": result,
                "Urgent": "Yes" if is_urgent else "No",
            }
            st.session_state.history.append(record)

# =========================================================
# VIEW 3: THERAPEUTICS & WELLNESS (COLLIE)
# =========================================================
elif st.session_state.page == "therapeutics":
    if st.sidebar.button(t("back_button")):
        st.session_state.page = "home"
        st.rerun()

    col_head, col_avatar = st.columns([3, 1])
    with col_head:
        st.title("🌿 Therapeutics & Wellness")
        st.write("Your mental wellness and daily mood space.")
    with col_avatar:
        render_mascot("Collie", "assets/collie.png", "🌿", width=90)

    st.markdown("---")

    now = datetime.now()
    if st.session_state.ban_expires_at and now < st.session_state.ban_expires_at:
        remaining = int((st.session_state.ban_expires_at - now).total_seconds() / 60) + 1
        st.error(f"⛔ **Chat paused:** You have received 3 warnings for inappropriate advances. Collie is taking a break. Please try again in {remaining} minute(s).")
    else:
        if st.session_state.ban_expires_at and now >= st.session_state.ban_expires_at:
            st.session_state.ban_expires_at = None
            st.session_state.warning_count = 0

        for msg in st.session_state.collie_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if user_prompt := st.chat_input("Talk to Collie about your mood or wellness..."):
            st.session_state.collie_messages.append({"role": "user", "content": user_prompt})
            
            if check_flirtatious_intent(user_prompt):
                st.session_state.warning_count += 1
                
                if st.session_state.warning_count == 1:
                    reply = "⚠️ **Warning (1/3):** I'm here purely as your health and wellness companion! Let's keep our conversation focused on your health goals. 😊"
                elif st.session_state.warning_count == 2:
                    reply = "⚠️ **Warning (2/3):** Please keep interactions respectful and focused on health. Another inappropriate message will pause chat access for 10 minutes."
                else:
                    st.session_state.ban_expires_at = datetime.now() + timedelta(minutes=10)
                    reply = "⛔ **Warning (3/3):** You have exceeded the warning threshold. Chat access is temporarily paused for 10 minutes."
            else:
                prompt_lower = user_prompt.lower()
                if "anxious" in prompt_lower or "stress" in prompt_lower:
                    reply = "I hear you. Anxiety can be overwhelming. Try the 4-7-8 breathing method: Breathe in for 4 seconds, hold for 7, and exhale slowly for 8 seconds. Would you like to try journaling what's on your mind?"
                elif "sad" in prompt_lower or "depressed" in prompt_lower:
                    reply = "I'm sorry you're feeling down. Remember to treat yourself gently today. Getting some fresh air, sipping water, or listening to calming music can help."
                elif "sleep" in prompt_lower or "tired" in prompt_lower:
                    reply = "Good sleep is crucial for wellness. Try turning off bright screens 1 hour before bed and keeping your room cool."
                else:
                    reply = "Thank you for sharing that with me! Remember, tracking your mood and maintaining light physical activity are great ways to keep your energy balanced. How else can I support your wellness today?"

            st.session_state.collie_messages.append({"role": "assistant", "content": reply})
            st.rerun()
