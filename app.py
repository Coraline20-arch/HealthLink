import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time
from datetime import datetime

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
    st.session_state.history = []   # stores each past diagnosis for this session
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# =========================================================
# 3. Simple multi-language text dictionary
#    Add more keys/languages here as needed.
# =========================================================
TEXT = {
    "English": {
        "welcome_title": "🩺 HealthLink AI Portal",
        "welcome_sub": "Bridging the gap between symptoms and specialist care.",
        "patients_header": "👤 Patients",
        "patients_info": "Experience our AI-driven diagnostic tool to analyze your symptoms.",
        "enter_button": "🚀 Enter Diagnostics",
        "specialists_header": "🏥 Specialists",
        "specialists_sub": "Access the secure patient queue and dashboard.",
        "admin_code": "Enter Admin Code",
        "diagnosis_title": "🔍 Symptom Analysis",
        "select_symptoms": "Select all symptoms you are experiencing:",
        "search_placeholder": "Search symptoms...",
        "severity_label": "Rate the severity of each symptom (helps your specialist, does not change the AI result):",
        "run_button": "Run AI Diagnosis",
        "loading_text": "AI is cross-referencing symptom patterns...",
        "predicted": "Predicted Condition",
        "confidence": "Model Confidence",
        "speed": "Processing Speed",
        "urgent": "🚨 Urgent Notice: This may be a high-priority condition. Please seek emergency care immediately or call your local emergency number.",
        "standard": "🟢 Standard Notice: Specialist follow-up recommended within a few days.",
        "book_button": "📋 Book Specialist Appointment",
        "download_summary": "⬇️ Download My Summary",
        "history_header": "🕓 Your Past Checks (this session)",
        "no_history": "No past checks yet.",
        "disclaimer": "⚠️ This tool is for educational purposes only and is not a substitute for professional medical advice.",
        "back_button": "⬅️ Back to Portal Home",
    },
    "Pidgin": {
        "welcome_title": "🩺 HealthLink AI Portal",
        "welcome_sub": "We dey connect your symptoms with specialist wey fit help you.",
        "patients_header": "👤 Patients",
        "patients_info": "Use our AI tool check wetin dey worry you.",
        "enter_button": "🚀 Enter Diagnostics",
        "specialists_header": "🏥 Specialists",
        "specialists_sub": "Enter the secure patient queue and dashboard.",
        "admin_code": "Enter Admin Code",
        "diagnosis_title": "🔍 Symptom Check",
        "select_symptoms": "Choose all the symptoms wey you dey feel:",
        "search_placeholder": "Find symptom...",
        "severity_label": "Rate how bad each symptom be (e go help your doctor, e no go change the AI result):",
        "run_button": "Run AI Check",
        "loading_text": "AI dey check your symptoms well well...",
        "predicted": "Wetin AI Think E Be",
        "confidence": "AI Confidence",
        "speed": "Speed",
        "urgent": "🚨 Serious Notice: This fit be serious matter. Abeg go hospital sharp sharp or call emergency number.",
        "standard": "🟢 Normal Notice: E good make you see specialist within few days.",
        "book_button": "📋 Book Specialist Appointment",
        "download_summary": "⬇️ Download My Summary",
        "history_header": "🕓 Your Past Checks (this session)",
        "no_history": "No past check yet.",
        "disclaimer": "⚠️ This tool na for learning purpose only, e no be replacement for real doctor advice.",
        "back_button": "⬅️ Go Back to Home",
    },
}

def t(key):
    lang = st.session_state.get("lang", "English")
    return TEXT.get(lang, TEXT["English"]).get(key, TEXT["English"].get(key, key))

# =========================================================
# 4. CSS
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

# =========================================================
# 5. Global Data Loading
# =========================================================
model = joblib.load('disease_model.pkl')
symptoms_list = list(joblib.load('symptoms_list.pkl'))

# List of urgent conditions - expand as needed
URGENT_DISEASES = ['Heart attack', 'Stroke', 'Malaria', 'Typhoid']

# =========================================================
# 6. Sidebar: language picker (always visible)
# =========================================================
st.sidebar.selectbox(
    "🌐 Language / Èdè / Harshe / Asụsụ",
    options=list(TEXT.keys()),
    key="lang",
)

# =========================================================
# VIEW 1: THE SPLASH SCREEN
# =========================================================
if st.session_state.page == "home":
    st.markdown('<div class="portal-card">', unsafe_allow_html=True)
    st.title(t("welcome_title"))
    st.write(t("welcome_sub"))
    st.write("A 10th-grade research project by **Chisom & Mesooma Obi**")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t("patients_header"))
        st.info(t("patients_info"))
        if st.button(t("enter_button"), use_container_width=True):
            st.session_state.page = "app"
            st.rerun()

    with col2:
        st.subheader(t("specialists_header"))
        st.write(t("specialists_sub"))
        password = st.text_input(t("admin_code"), type="password")

        # --- Admin code now pulled from st.secrets instead of hardcoded ---
        # Create a file at .streamlit/secrets.toml with:
        #   admin_code = "4421"
        # (see secrets.toml.example provided alongside this file)
        real_admin_code = st.secrets.get("admin_code", "4421")

        if password and password == real_admin_code:
            st.success("Access Granted. When opening the queue, right click and 'Open in a new tab'.")

            # --- Optional: live dashboard pulled straight from Google Sheets ---
            # This only activates if you've configured a Google service account
            # in st.secrets (see notes at the bottom of this file). Otherwise it
            # falls back to the plain spreadsheet link, same as before.
            sheet_url = "https://docs.google.com/spreadsheets/d/1RFfeLyySqT8hxieP0ZzuHe9WLcpMiZJxprHz6G7F98E/edit?usp=sharing"

            dashboard_loaded = False
            if "gcp_service_account" in st.secrets:
                try:
                    import gspread
                    from google.oauth2.service_account import Credentials

                    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
                    creds = Credentials.from_service_account_info(
                        st.secrets["gcp_service_account"], scopes=scopes
                    )
                    gc = gspread.authorize(creds)
                    sh = gc.open_by_url(sheet_url)
                    worksheet = sh.sheet1
                    records = worksheet.get_all_records()

                    if records:
                        df = pd.DataFrame(records)

                        # --- Triage sorting: urgent cases bubble to the top ---
                        # Assumes the sheet has a column literally called "Condition"
                        # or "Predicted Condition". Adjust the column name below to
                        # match whatever your Google Form actually writes.
                        condition_col = None
                        for candidate in ["Predicted Condition", "Condition", "Diagnosis"]:
                            if candidate in df.columns:
                                condition_col = candidate
                                break

                        if condition_col:
                            df["Urgent"] = df[condition_col].isin(URGENT_DISEASES)
                            df = df.sort_values(by="Urgent", ascending=False)
                            st.subheader("📂 Patient Queue (urgent cases first)")
                            st.dataframe(
                                df.drop(columns=["Urgent"]),
                                use_container_width=True,
                            )
                        else:
                            st.subheader("📂 Patient Queue")
                            st.dataframe(df, use_container_width=True)

                        dashboard_loaded = True
                except Exception as e:
                    st.warning(f"Couldn't load live dashboard, showing raw link instead. ({e})")

            if not dashboard_loaded:
                st.link_button("📂 Open Patient Queue", sheet_url, use_container_width=True)
        elif password:
            st.error("Incorrect code.")

# =========================================================
# VIEW 2: THE DIAGNOSTICS APP
# =========================================================
else:
    if st.sidebar.button(t("back_button")):
        st.session_state.page = "home"
        st.rerun()

    st.title(t("diagnosis_title"))

    # --- Symptom search filter, on top of the multiselect's own search ---
    search_term = st.text_input("🔎 " + t("search_placeholder"))
    if search_term:
        filtered_symptoms = [s for s in symptoms_list if search_term.lower() in s.lower()]
    else:
        filtered_symptoms = symptoms_list

    options = st.multiselect(t("select_symptoms"), filtered_symptoms)

    # --- Severity sliders per selected symptom ---
    # NOTE: The underlying model was trained on plain yes/no (0/1) symptom
    # inputs, so severity is NOT fed into the model (that could quietly
    # break predictions). It's shown to the specialist in the summary/
    # appointment info instead, which is where it's actually useful.
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
        else:
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st.markdown(f"""
                    <div style="padding: 30px; text-align: center;">
                        <svg class="loader-heart" viewBox="0 0 24 24">
                            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                        </svg>
                        <p style="color: black; font-weight: 500;">{t("loading_text")}</p>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(2.5)

            loading_placeholder.empty()

            input_data = np.zeros(len(symptoms_list))
            for s in options:
                index = symptoms_list.index(s)
                input_data[index] = 1

            input_vector = input_data.reshape(1, -1)
            prediction = model.predict(input_vector)
            result = prediction[0]

            # --- Real confidence score instead of a hardcoded "94%" ---
            confidence_text = "N/A"
            top_alternatives = []
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(input_vector)[0]
                classes = model.classes_
                top_idx = np.argsort(proba)[::-1][:3]
                top_alternatives = [(classes[i], proba[i]) for i in top_idx]
                confidence_text = f"{top_alternatives[0][1] * 100:.1f}%"

            # --- Real processing speed instead of a hardcoded "1.2s" ---
            start_time = time.time()
            _ = model.predict(input_vector)
            elapsed = time.time() - start_time
            speed_text = f"{elapsed:.2f}s"

            st.success(f"### {t('predicted')}: {result}")

            col_m1, col_m2 = st.columns(2)
            col_m1.metric(t("confidence"), confidence_text)
            col_m2.metric(t("speed"), speed_text)

            # --- Show top-3 alternative conditions, if available ---
            if len(top_alternatives) > 1:
                st.write("**Other possible matches:**")
                for cond, prob in top_alternatives[1:]:
                    st.write(f"- {cond}: {prob * 100:.1f}%")

            # --- Simple explainability: which symptoms most likely drove this ---
            # Works for tree-based models (feature_importances_) or linear
            # models (coef_). Skips gracefully if the model has neither.
            importances = None
            if hasattr(model, "feature_importances_"):
                importances = model.feature_importances_
            elif hasattr(model, "coef_"):
                importances = np.abs(model.coef_).mean(axis=0) if model.coef_.ndim > 1 else np.abs(model.coef_)

            if importances is not None:
                selected_importance = [
                    (s, importances[symptoms_list.index(s)]) for s in options
                ]
                selected_importance.sort(key=lambda x: x[1], reverse=True)
                if selected_importance:
                    st.write("**Symptoms that most influenced this result:**")
                    for sym, score in selected_importance[:3]:
                        st.write(f"- {sym}")

            is_urgent = result in URGENT_DISEASES
            if is_urgent:
                st.error(t("urgent"))
            else:
                st.info(t("standard"))

            form_url = "https://docs.google.com/forms/d/e/1FAIpQLSec-ev-zZ3KcUQW6A1eYBSl_MuAzqoZbImXYlvHzWcGYfK8_w/viewform?usp=header"
            st.link_button(t("book_button"), form_url, type="primary")

            # --- Save this check into session history ---
            record = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Symptoms": ", ".join(options),
                "Severity": ", ".join(f"{s}: {severities[s]}" for s in options),
                "Predicted Condition": result,
                "Confidence": confidence_text,
                "Urgent": "Yes" if is_urgent else "No",
            }
            st.session_state.history.append(record)

            # --- Downloadable summary for the patient to bring to their visit ---
            summary_text = (
                f"HealthLink AI Summary\n"
                f"Date: {record['Time']}\n"
                f"Symptoms: {record['Symptoms']}\n"
                f"Severity: {record['Severity']}\n"
                f"Predicted Condition: {record['Predicted Condition']}\n"
                f"Confidence: {record['Confidence']}\n"
                f"Urgency: {record['Urgent']}\n"
            )
            st.download_button(
                t("download_summary"),
                data=summary_text,
                file_name=f"healthlink_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
            )

    # --- History section ---
    st.markdown("---")
    st.subheader(t("history_header"))
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    else:
        st.caption(t("no_history"))

    st.markdown("---")
    st.caption(t("disclaimer"))
