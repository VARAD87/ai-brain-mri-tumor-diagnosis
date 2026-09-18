import os
import streamlit as st
import torch
import numpy as np
import cv2

from src.models.cnn_baseline import CNNBaseline
from src.segmentation.unet import UNet
from src.app.ui_utils import inject_custom_css, render_header, render_card

CLASS_NAMES = ["Glioma", "Meningioma", "No Tumor", "Pituitary"]

@st.cache_resource
def load_models():
    
    cnn = CNNBaseline(num_classes=4)
    cnn.load_state_dict(torch.load("saved_models/cnn_gan_augmented.pth", map_location="cpu"))
    cnn.eval()


    unet = UNet()
    unet.load_state_dict(torch.load("saved_models/unet_segmentation.pth", map_location="cpu"))
    unet.eval()

    return cnn, unet


st.set_page_config(page_title="MRI Diagnosis | Doctor Portal", layout="wide")


inject_custom_css()


render_header(
    title="MRI Diagnosis & AI Analysis",
    subtitle="AI-assisted classification and pixel-level tumor boundary segmentation"
)


if "patient" not in st.session_state:
    st.warning(" Access Denied: Please complete Patient Registration prior to running diagnostic inference.")
    st.stop()


try:
    cnn_model, unet_model = load_models()
    models_loaded = True
except Exception as e:
    st.error(f"Error loading deep learning models: {e}")
    models_loaded = False

if models_loaded:
    p = st.session_state["patient"]
    

    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.markdown("## MRI Image Upload")
        
     
        st.markdown(
            f"""
            <div style="background-color: #0f172a; padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 1rem;">
                <span style="font-size: 0.85rem; color: #64748b; text-transform: uppercase;">Active Patient:</span>
                <span style="font-weight: 600; color: #38bdf8; margin-left: 0.5rem;">{p['name']} ({p['age']}y/o {p['gender']})</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        uploaded = st.file_uploader(
            "Select T2/T1 Brain MRI Scan Image (JPG/PNG)", 
            type=["jpg", "png", "jpeg"]
        )

        if uploaded:
            img_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
            img = cv2.imdecode(img_bytes, 1)
            
            
            st.image(img, caption="Original Uploaded MRI Scan", use_column_width=True)
        else:
            st.markdown(
                """
                <div class="upload-card">
                    <span style="font-size: 3rem; display: block; margin-bottom: 0.5rem;">📁</span>
                    Awaiting T2/T1 MRI image upload.<br/>
                    Please drag and drop or browse for a file above.
                </div>
                """,
                unsafe_allow_html=True
            )

    with col_right:
        st.markdown("## AI Classification & Segmentation")
        
        if uploaded:
            with st.spinner("Executing AI Model Inference..."):
                
                img_r = cv2.resize(img, (224, 224)) / 255.0
                tensor = torch.tensor(img_r).permute(2, 0, 1).unsqueeze(0).float()

               
                with torch.no_grad():
                    out = cnn_model(tensor)
                    probs = torch.softmax(out, dim=1)
                    conf, pred = torch.max(probs, 1)

                tumor = CLASS_NAMES[pred.item()]
                confidence = conf.item() * 100

              
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, (224, 224))
                gray_tensor = torch.tensor(gray).unsqueeze(0).unsqueeze(0).float()

               
                with torch.no_grad():
                    mask = unet_model(gray_tensor).squeeze().numpy()

            
                mask_uint = (mask * 255).astype(np.uint8)
                overlay = cv2.applyColorMap(mask_uint, cv2.COLORMAP_JET)
                
                combined = cv2.addWeighted(
                    cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), 0.7, 
                    overlay, 0.3, 0
                )
                
               
                os.makedirs("reports/figures", exist_ok=True)
                seg_path = "reports/figures/segmentation_overlay.png"
                cv2.imwrite(seg_path, combined)
                
      
                st.session_state["segmentation_image"] = seg_path
                st.session_state["diagnosis"] = {
                    "tumor": tumor,
                    "confidence": confidence
                }

           
            border_cls = "no-tumor" if tumor == "No Tumor" else "tumor-detected"
            icon = "🟢" if tumor == "No Tumor" else "🔴"
            
            card_html = f"""
            <div style="display: flex; flex-direction: column; gap: 0.5rem; color: #f8fafc;">
                <div style="font-size: 1.25rem; font-weight: 600;">
                    {icon} Diagnosis: <span style="color: {'#10b981' if tumor == 'No Tumor' else '#ef4444'}">{tumor}</span>
                </div>
                <div style="font-size: 1rem; color: #94a3b8; margin-top: 0.25rem;">
                    Confidence Score: <span style="color: #f1f5f9; font-weight: 600;">{confidence:.2f}%</span>
                </div>
                <div style="background-color: #334155; border-radius: 6px; height: 10px; width: 100%; margin-top: 0.25rem; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #00f2fe, #4facfe); width: {confidence}%; height: 100%; border-radius: 6px;"></div>
                </div>
            </div>
            """
            
            render_card(
                title="Clinical Findings",
                html_content=card_html,
                border_class=border_cls
            )

     
            st.markdown("#### Visual Localization Analysis")
            col_raw, col_seg = st.columns(2)
            
            with col_raw:
                st.image(gray, caption="Grayscale Slice (224x224)", use_column_width=True)
            with col_seg:
                st.image(combined, caption="AI Segmentation Mask Overlay", use_column_width=True)
                
            st.success(" Scan processed. You can now compile the PDF report.")

        else:
            st.info(" Awaiting MRI Scan upload on the left column to run deep learning classification and segmentation.")
