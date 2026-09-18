import streamlit as st
from src.app.ui_utils import inject_custom_css, render_header, render_card

# Page configuration
st.set_page_config(page_title="Patient Registration | Doctor Portal", layout="wide")

# Inject custom styling
inject_custom_css()

# Render page header
render_header(
    title="Patient Registration",
    subtitle="Add new patient records and clinical symptoms prior to diagnosis"
)

# Two column layout: Left (Form), Right (Active Patient Details)
col_form, col_status = st.columns([1.2, 0.8])

with col_form:
    st.markdown("### 📋 Registration Form")
    
    with st.form("patient_form", clear_on_submit=False):
        name = st.text_input("Patient Full Name", placeholder="e.g., Jane Doe")
        
        col_age_gender = st.columns(2)
        with col_age_gender[0]:
            age = st.number_input("Patient Age (Years)", min_value=0, max_value=120, value=30, step=1)
        with col_age_gender[1]:
            gender = st.selectbox("Patient Gender", ["Male", "Female", "Other"])
            
        symptoms = st.text_area("Clinical Symptoms / History Notes", placeholder="Detail symptoms, duration, and clinical history...")
        
        submit = st.form_submit_button("💾 Save Patient Details")

    if submit:
        if not name.strip():
            st.error("⚠️ Patient Name cannot be blank.")
        else:
            st.session_state["patient"] = {
                "name": name,
                "age": age,
                "gender": gender,
                "symptoms": symptoms if symptoms.strip() else "None reported"
            }
            st.success("✅ Patient details registered successfully. Proceed to MRI Diagnosis page.")

with col_status:
    st.markdown("### 🎫 Active Patient Record")
    
    if "patient" in st.session_state:
        p = st.session_state["patient"]
        card_content = f"""
        <div style="line-height: 1.6; font-size: 0.95rem; color: #e2e8f0;">
            <p><strong>Name:</strong> {p['name']}</p>
            <p><strong>Age:</strong> {p['age']} years</p>
            <p><strong>Gender:</strong> {p['gender']}</p>
            <p style="border-top: 1px solid #334155; padding-top: 0.75rem; margin-top: 0.75rem;">
                <strong>Symptoms / Notes:</strong><br/>
                <span style="color: #94a3b8; font-style: italic;">{p['symptoms']}</span>
            </p>
        </div>
        """
        render_card(title="Active Patient Details", html_content=card_content, border_class="no-tumor")
    else:
        info_content = """
        <div style="line-height: 1.6; font-size: 0.95rem; color: #94a3b8; font-style: italic;">
            No patient records registered for the current diagnostic session. 
            Fill out and submit the registration form on the left.
        </div>
        """
        render_card(title="System Status: Idle", html_content=info_content)
