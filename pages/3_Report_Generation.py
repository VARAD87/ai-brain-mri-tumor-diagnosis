import os
import streamlit as st
from fpdf import FPDF
from datetime import datetime
from src.app.ui_utils import inject_custom_css, render_header, render_card


st.set_page_config(page_title="Generate Report | Doctor Portal", layout="wide")


inject_custom_css()


render_header(
    title="Report Generation Center",
    subtitle="Compile clinical findings and segmentation masks into certified PDF documents"
)


if "patient" not in st.session_state or "diagnosis" not in st.session_state:
    st.warning(" Access Denied: Patient registration and MRI diagnostic analysis must be completed prior to report generation.")
    st.stop()

patient = st.session_state["patient"]
diag = st.session_state["diagnosis"]
seg_image_path = st.session_state.get("segmentation_image")


col_preview, col_action = st.columns([1.2, 0.8])

with col_preview:
    st.markdown("### 🔍 Live Report Preview Draft")
    
    preview_html = f"""
    <div style="background-color: #0f172a; padding: 1.5rem; border-radius: 8px; border: 1px solid #1e293b; color: #e2e8f0; line-height: 1.6;">
        <div style="text-align: center; border-bottom: 2px solid #334155; padding-bottom: 0.75rem; margin-bottom: 1rem;">
            <h5 style="margin: 0; color: #00adb5; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 0.05em;">AI-Powered Brain MRI Diagnostic Report</h5>
            <span style="font-size: 0.8rem; color: #64748b;">Department of Radiology | Doctor Portal System</span>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <span style="font-weight: 600; color: #38bdf8; text-transform: uppercase; font-size: 0.85rem; display: block; border-bottom: 1px solid #1e293b; padding-bottom: 0.25rem;">Patient Information</span>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 0.5rem; font-size: 0.9rem;">
                <div><strong>Name:</strong> {patient['name']}</div>
                <div><strong>Age / Gender:</strong> {patient['age']} yrs / {patient['gender']}</div>
                <div><strong>Exam Date:</strong> {datetime.now().strftime('%d %B %Y')}</div>
                <div><strong>Ref. Symptoms:</strong> <span style="font-style: italic; color: #94a3b8;">{patient['symptoms']}</span></div>
            </div>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <span style="font-weight: 600; color: #38bdf8; text-transform: uppercase; font-size: 0.85rem; display: block; border-bottom: 1px solid #1e293b; padding-bottom: 0.25rem;">Diagnostic Findings</span>
            <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #cbd5e1;">
                Quantitative computer-aided classification analysis of the uploaded MRI scan yields a predicted tissue match for 
                <strong style="color: {'#10b981' if diag['tumor'] == 'No Tumor' else '#ef4444'}">{diag['tumor']}</strong> with a model confidence of 
                <strong>{diag['confidence']:.2f}%</strong>.
            </p>
        </div>
        
        <div>
            <span style="font-weight: 600; color: #38bdf8; text-transform: uppercase; font-size: 0.85rem; display: block; border-bottom: 1px solid #1e293b; padding-bottom: 0.25rem;">Conclusion & Guidance</span>
            <p style="margin-top: 0.5rem; font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                Findings indicate localized abnormal structures matching {diag['tumor']}. Spatial segmentation maps are overlayed on the target slices to assist radiology visual review. 
                This report is for decision-support only and should be reviewed by a board-certified neuroradiologist.
            </p>
        </div>
    </div>
    """
    
    st.markdown(preview_html, unsafe_allow_html=True)
    
    
    if seg_image_path and os.path.exists(seg_image_path):
        st.markdown("")
        st.image(seg_image_path, caption="Referenced Tumor Segmentation Slice", width=250)

with col_action:
    st.markdown("### ⚙️ Output Controls")
    
    action_html = """
    <p style="color: #cbd5e1; font-size: 0.95rem;">
        Click below to compile the validated draft into a professional, printable diagnostic PDF document.
        The resulting file will be archived in the system database for historical references.
    </p>
    """
    
    # Store compilation status
    pdf_generated = False
    download_path = ""
    
    with st.container():
        render_card(
            title="Compile Certified Report",
            html_content=action_html
        )
        
        
        if st.button("📄 Generate Certified PDF"):
            with st.spinner("Compiling PDF assets and adding clinical signatures..."):
                os.makedirs("reports/history", exist_ok=True)

                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

               
                pdf.set_fill_color(240, 240, 240)
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "AI-Powered Brain MRI Diagnostic Report", ln=True, align="C")

                pdf.set_font("Arial", "", 11)
                pdf.cell(0, 8, "Department of Radiology | Doctor Portal System", ln=True, align="C")

                pdf.ln(8)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(10)

                # -------- PATIENT DETAILS --------
                pdf.set_font("Arial", "B", 13)
                pdf.cell(0, 8, "Patient Information", ln=True)

                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 8, f"Patient Name: {patient['name']}", ln=True)
                pdf.cell(0, 8, f"Age: {patient['age']} years", ln=True)
                pdf.cell(0, 8, f"Gender: {patient['gender']}", ln=True)
                pdf.cell(0, 8, f"Date: {datetime.now().strftime('%d %B %Y')}", ln=True)

                pdf.ln(8)

                # -------- FINDINGS --------
                pdf.set_font("Arial", "B", 13)
                pdf.cell(0, 8, "Diagnostic Findings", ln=True)

                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(
                    0, 8,
                    f"The uploaded brain MRI scan was analyzed using an AI-based deep learning "
                    f"system. The model predicts the presence of a {diag['tumor']} tumor with "
                    f"a confidence score of {diag['confidence']:.2f}%. "
                    f"The classification model was trained using GAN-augmented MRI data."
                )

                pdf.ln(8)

             
                if seg_image_path and os.path.exists(seg_image_path):
                    pdf.set_font("Arial", "B", 13)
                    pdf.cell(0, 8, "Tumor Segmentation Result", ln=True)
                    pdf.ln(5)

                    
                    pdf.image(seg_image_path, x=30, w=150)
                    pdf.ln(8)

         
                pdf.set_font("Arial", "B", 13)
                pdf.cell(0, 8, "Conclusion", ln=True)

                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(
                    0, 8,
                    "The AI-based analysis indicates abnormal tissue regions consistent with a "
                    "brain tumor. The segmentation highlights the suspected tumor location to "
                    "support clinical interpretation. This report is intended as a decision-"
                    "support tool and should be reviewed by a qualified medical professional."
                )

                pdf.ln(10)
                pdf.set_font("Arial", "I", 10)
                pdf.cell(0, 8, "This is a computer-generated report and does not require a signature.", ln=True)

                # -------- SAVE --------
                filename = f"{patient['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                path = f"reports/history/{filename}"
                pdf.output(path)
                
                st.session_state["last_report_path"] = path
                st.session_state["report_ready"] = True

 
    if st.session_state.get("report_ready") and "last_report_path" in st.session_state:
        saved_path = st.session_state["last_report_path"]
        if os.path.exists(saved_path):
            st.markdown("")
            st.success("✅ Medical report successfully compiled and archived!")
            
            with open(saved_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=f,
                    file_name=os.path.basename(saved_path),
                    mime="application/pdf"
                )
