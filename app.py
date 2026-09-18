import streamlit as st
from src.app.ui_utils import inject_custom_css, render_header, render_kpi, render_card

# Configure Streamlit page layout
st.set_page_config(page_title="Doctor Portal | Brain MRI AI", layout="wide")

# Inject custom modern styling
inject_custom_css()

# Render portal header
render_header(
    title="AI Brain MRI Diagnosis System",
    subtitle="Doctor Portal Dashboard & Clinical Decision Support"
)

# Display Portal Quick Status KPIs
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        render_kpi(value="4 Classes", label="Tumor Classifier (CNN)"),
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        render_kpi(value="U-Net Active", label="Tumor Segmentation"),
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        render_kpi(value="GAN Augmented", label="Augmentation Status"),
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("###  Clinical Diagnostic Workflow")
st.info(" Navigate through the steps in the sidebar to perform diagnosis and review results.")

# Create grid cards for workflow description
col_left, col_right = st.columns(2)

with col_left:
    render_card(
        title="1. Patient Registration",
        html_content="""
        <p style="color: #cbd5e1; margin-bottom: 0;">
            Register patient metadata, age, gender, and clinical symptoms. 
            Saved credentials persist in the session state to populate subsequent diagnostic findings and official reports.
        </p>
        """
    )
    
    render_card(
        title="2. MRI Diagnosis & AI Analysis",
        html_content="""
        <p style="color: #cbd5e1; margin-bottom: 0;">
            Upload clinical T2/T1 MRI scans. The CNN model classifies the scan type while the U-Net 
            generates precise boundaries of identified tumor masses, overlaid in real-time.
        </p>
        """
    )

with col_right:
    render_card(
        title="3. Report Generation",
        html_content="""
        <p style="color: #cbd5e1; margin-bottom: 0;">
            Compile clinical findings, CNN confidence percentages, and visual U-Net overlay masks. 
            Instantly export a print-ready, professional PDF report conforming to hospital standards.
        </p>
        """
    )
    
    render_card(
        title="4. Historical Archives",
        html_content="""
        <p style="color: #cbd5e1; margin-bottom: 0;">
            Review previously generated patient reports. Searchable dashboard keeps track of history 
            and allows downloading archived PDFs without rerun.
        </p>
        """
    )
