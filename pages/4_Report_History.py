import os
import streamlit as st
from datetime import datetime
from src.app.ui_utils import inject_custom_css, render_header

# Configure layout
st.set_page_config(page_title="Report History | Doctor Portal", layout="wide")

# Inject styles
inject_custom_css()

# Render header
render_header(
    title="Report History & Archives",
    subtitle="Search and retrieve computer-generated patient diagnostic PDF files"
)

folder = "reports/history"
os.makedirs(folder, exist_ok=True)

# List all PDF reports in directory
files = [f for f in os.listdir(folder) if f.endswith(".pdf")]

if files:
    # Search input for filter
    search_query = st.text_input("🔍 Search reports by Patient Name", placeholder="Type patient name to filter...").strip().lower()
    
    # Filter files
    filtered_files = []
    for f in files:
        # Expected format: Patient_Name_YYYYMMDD_HHMMSS.pdf
        name_part = f.rsplit("_", 2)[0]
        display_name = name_part.replace("_", " ")
        if not search_query or search_query in display_name.lower():
            filtered_files.append((f, display_name))
            
    st.markdown("### 🗃 Archived Reports")
    
    if filtered_files:
        # Display each report in a grid layout
        for file_name, display_name in filtered_files:
            file_path = os.path.join(folder, file_name)
            
            # Extract timestamp from filename if matches format
            try:
                # e.g., Patient_Name_20231024_153022.pdf -> 20231024_153022
                parts = file_name.replace(".pdf", "").rsplit("_", 2)
                date_str = parts[-2]
                time_str = parts[-1]
                dt = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                date_formatted = dt.strftime("%d %B %Y, %I:%M %p")
            except Exception:
                # Fallback to file creation time if filename format fails
                mtime = os.path.getmtime(file_path)
                date_formatted = datetime.fromtimestamp(mtime).strftime("%d %B %Y, %I:%M %p")

            # Layout for the file card: Left (details), Right (download action button)
            col_details, col_button = st.columns([3, 1])
            
            with col_details:
                st.markdown(
                    f"""
                    <div style="background-color: #1e293b; border-left: 4px solid #00adb5; padding: 0.85rem; border-radius: 4px; margin-bottom: 0.5rem; height: 100%;">
                        <div style="font-weight: 600; color: #f8fafc; font-size: 1rem;">{display_name}</div>
                        <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.2rem;">Generated: {date_formatted}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            with col_button:
                # Read PDF bytes to enable download button
                with open(file_path, "rb") as f:
                    pdf_bytes = f.read()
                    
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name=file_name,
                    mime="application/pdf",
                    key=f"dl_{file_name}"
                )
            st.markdown("<hr style='margin: 0.5rem 0; border-color: #1e293b;'/>", unsafe_allow_html=True)
    else:
        st.info("No archived reports match the search criteria.")
else:
    st.info("📂 No diagnostic reports are currently archived in the system history.")
