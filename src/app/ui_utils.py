import streamlit as st

def inject_custom_css():
    """Injects high-end professional styling into the Streamlit app."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Apply fonts */
        html, body, [class*="css"], .stMarkdown, p, span, label, input, select, textarea {
            font-family: 'Outfit', sans-serif !important;
        }

        /* Hide default Streamlit Deploy button */
        .stAppDeployButton {
            display: none !important;
        }

        /* Customize main container */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #1e293b;
        }
        section[data-testid="stSidebar"] .sidebar-content {
            background-color: #0f172a !important;
        }

        /* Custom Cards */
        .med-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            margin-bottom: 1.25rem;
            color: #f8fafc;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .med-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
        .med-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #00f2fe, #4facfe);
        }
        
        /* Threat-level Glowing Borders */
        .med-card.tumor-detected::before {
            background: linear-gradient(90deg, #ef4444, #f87171);
        }
        .med-card.no-tumor::before {
            background: linear-gradient(90deg, #10b981, #34d399);
        }

        /* Card Text */
        .med-card h4 {
            margin-top: 0 !important;
            color: #38bdf8 !important;
            font-weight: 600 !important;
            font-size: 1.15rem !important;
            margin-bottom: 0.75rem !important;
        }

        /* Metric Cards */
        .kpi-container {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        .kpi-card {
            flex: 1;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 1.25rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        }
        .kpi-card:hover {
            border-color: #00adb5;
            box-shadow: 0 0 10px rgba(0, 173, 181, 0.2);
        }
        .kpi-val {
            font-size: 2rem;
            font-weight: 700;
            color: #00adb5;
            margin-bottom: 0.25rem;
        }
        .kpi-lbl {
            font-size: 0.75rem;
            font-weight: 500;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.07em;
        }

        /* Form styling */
        div[data-testid="stForm"] {
            border: 1px solid #334155 !important;
            background-color: #1e293b !important;
            border-radius: 12px !important;
            padding: 2rem !important;
        }

        /* Buttons Styling */
        div.stButton > button {
            background: linear-gradient(90deg, #00adb5, #007bb5) !important;
            color: #ffffff !important;
            border: none !important;
            padding: 0.6rem 2rem !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 6px rgba(0, 173, 181, 0.2) !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }
        div.stButton > button:hover {
            box-shadow: 0 6px 15px rgba(0, 173, 181, 0.4) !important;
            transform: translateY(-2px) !important;
            color: #ffffff !important;
        }
        div.stButton > button:active {
            transform: translateY(0px) !important;
        }

        /* Report List Grid */
        .report-grid-card {
            background-color: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .report-grid-info {
            display: flex;
            flex-direction: column;
        }
        .report-patient-name {
            font-weight: 600;
            color: #f1f5f9;
            font-size: 1.05rem;
        }
        .report-date {
            font-size: 0.8rem;
            color: #64748b;
            margin-top: 0.15rem;
        }
        
        /* Dropzone visual placeholder */
        .upload-card {
            border: 2px dashed #475569;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            background-color: #0f172a;
            color: #94a3b8;
            margin-bottom: 1.5rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

def render_header(title, subtitle=None):
    """Renders a beautiful medical portal header."""
    subtitle_html = f"<div style='color: #94a3b8; font-size: 1.1rem; margin-top: 0.25rem;'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        f"""
        <div style="margin-bottom: 2rem; border-bottom: 2px solid #1e293b; padding-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 2.25rem;">🧠</span>
                <span style="font-size: 2rem; font-weight: 700; background: linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {title}
                </span>
            </div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_kpi(value, label):
    """Returns the HTML for a single KPI metric card."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-val">{value}</div>
        <div class="kpi-lbl">{label}</div>
    </div>
    """

def render_card(title, html_content, border_class=""):
    """Renders a styled card wrapper."""
    st.markdown(
        f"""
        <div class="med-card {border_class}">
            <h4>{title}</h4>
            <div>{html_content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
