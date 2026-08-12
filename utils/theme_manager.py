import streamlit as st
from pathlib import Path

THEMES = {
    "Dark Glassmorphic": {
        "bg": "linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%)",
        "text": "#F8FAFC",
        "sidebar_bg": "rgba(15, 23, 42, 0.95)",
        "sidebar_border": "rgba(255, 255, 255, 0.08)",
        "card_bg": "rgba(30, 41, 59, 0.7)",
        "card_border": "rgba(255, 255, 255, 0.1)",
        "card_hover_box_shadow": "0 12px 40px 0 rgba(99, 102, 241, 0.2)",
        "gradient_text": "linear-gradient(90deg, #818CF8 0%, #C084FC 50%, #38BDF8 100%)",
        "stat_bg": "rgba(15, 23, 42, 0.6)",
        "stat_border": "#6366F1",
        "btn_bg": "linear-gradient(90deg, #6366F1 0%, #4F46E5 100%)",
        "btn_hover": "linear-gradient(90deg, #4F46E5 0%, #4338CA 100%)",
        "btn_text": "#FFFFFF",
        "input_bg": "rgba(15, 23, 42, 0.7)",
        "input_text": "#F8FAFC"
    },
    "Light Mode": {
        "bg": "linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 50%, #F8FAFC 100%)",
        "text": "#0F172A",
        "sidebar_bg": "#FFFFFF",
        "sidebar_border": "rgba(0, 0, 0, 0.1)",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "card_border": "rgba(203, 213, 225, 0.8)",
        "card_hover_box_shadow": "0 12px 40px 0 rgba(37, 99, 235, 0.15)",
        "gradient_text": "linear-gradient(90deg, #2563EB 0%, #7C3AED 50%, #0D9488 100%)",
        "stat_bg": "#F8FAFC",
        "stat_border": "#2563EB",
        "btn_bg": "linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%)",
        "btn_hover": "linear-gradient(90deg, #1D4ED8 0%, #1E40AF 100%)",
        "btn_text": "#FFFFFF",
        "input_bg": "#FFFFFF",
        "input_text": "#0F172A"
    },
    "Cyberpunk Neon": {
        "bg": "linear-gradient(135deg, #09090B 0%, #180828 50%, #030712 100%)",
        "text": "#F472B6",
        "sidebar_bg": "rgba(12, 10, 25, 0.95)",
        "sidebar_border": "rgba(236, 72, 153, 0.2)",
        "card_bg": "rgba(24, 15, 45, 0.8)",
        "card_border": "rgba(236, 72, 153, 0.4)",
        "card_hover_box_shadow": "0 12px 40px 0 rgba(236, 72, 153, 0.3)",
        "gradient_text": "linear-gradient(90deg, #F43F5E 0%, #A855F7 50%, #06B6D4 100%)",
        "stat_bg": "rgba(20, 10, 35, 0.7)",
        "stat_border": "#EC4899",
        "btn_bg": "linear-gradient(90deg, #EC4899 0%, #8B5CF6 100%)",
        "btn_hover": "linear-gradient(90deg, #DB2777 0%, #7C3AED 100%)",
        "btn_text": "#FFFFFF",
        "input_bg": "rgba(20, 10, 35, 0.8)",
        "input_text": "#F472B6"
    },
    "Emerald Forest": {
        "bg": "linear-gradient(135deg, #062C24 0%, #022C22 50%, #064E3B 100%)",
        "text": "#ECFDF5",
        "sidebar_bg": "rgba(4, 44, 34, 0.95)",
        "sidebar_border": "rgba(52, 211, 153, 0.15)",
        "card_bg": "rgba(6, 78, 59, 0.5)",
        "card_border": "rgba(52, 211, 153, 0.25)",
        "card_hover_box_shadow": "0 12px 40px 0 rgba(16, 185, 129, 0.2)",
        "gradient_text": "linear-gradient(90deg, #34D399 0%, #10B981 50%, #6EE7B7 100%)",
        "stat_bg": "rgba(2, 44, 34, 0.7)",
        "stat_border": "#10B981",
        "btn_bg": "linear-gradient(90deg, #10B981 0%, #059669 100%)",
        "btn_hover": "linear-gradient(90deg, #059669 0%, #047857 100%)",
        "btn_text": "#FFFFFF",
        "input_bg": "rgba(4, 44, 34, 0.8)",
        "input_text": "#ECFDF5"
    },
    "Midnight OLED": {
        "bg": "#000000",
        "text": "#F1F5F9",
        "sidebar_bg": "#0D0D0D",
        "sidebar_border": "rgba(255, 255, 255, 0.15)",
        "card_bg": "rgba(20, 20, 20, 0.95)",
        "card_border": "rgba(255, 255, 255, 0.2)",
        "card_hover_box_shadow": "0 12px 40px 0 rgba(59, 130, 246, 0.25)",
        "gradient_text": "linear-gradient(90deg, #60A5FA 0%, #3B82F6 50%, #93C5FD 100%)",
        "stat_bg": "#121212",
        "stat_border": "#3B82F6",
        "btn_bg": "linear-gradient(90deg, #3B82F6 0%, #2563EB 100%)",
        "btn_hover": "linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%)",
        "btn_text": "#FFFFFF",
        "input_bg": "#171717",
        "input_text": "#F1F5F9"
    }
}

def apply_theme(theme_name="Dark Glassmorphic"):
    """Inject dynamic CSS into Streamlit based on theme choice."""
    if theme_name not in THEMES:
        theme_name = "Dark Glassmorphic"
    
    t = THEMES[theme_name]
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, .stApp, p, h1, h2, h3, h4, h5, h6, input, button, select, textarea, .stMarkdown {{
        font-family: 'Inter', sans-serif !important;
    }}

    .stApp {{
        background: {t['bg']} !important;
        color: {t['text']} !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {t['sidebar_bg']} !important;
        border-right: 1px solid {t['sidebar_border']} !important;
    }}

    .glass-card {{
        background: {t['card_bg']} !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {t['card_border']} !important;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .glass-card:hover {{
        transform: translateY(-2px);
        box-shadow: {t['card_hover_box_shadow']} !important;
    }}

    .gradient-text {{
        background: {t['gradient_text']} !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 800;
    }}

    .stat-box {{
        background: {t['stat_bg']} !important;
        border-left: 4px solid {t['stat_border']} !important;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }}

    .stButton > button {{
        background: {t['btn_bg']} !important;
        color: {t['btn_text']} !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }}

    .stButton > button:hover {{
        background: {t['btn_hover']} !important;
        transform: translateY(-1px);
    }}

    /* Inputs styling for light / dark modes */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
        background-color: {t['input_bg']} !important;
        color: {t['input_text']} !important;
    }}

    /* Expander Layout & Icon Overlap Fix */
    details[data-testid="stExpander"] {{
        border: 1px solid {t['card_border']} !important;
        border-radius: 12px !important;
        background: {t['card_bg']} !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }}

    details[data-testid="stExpander"] summary {{
        display: flex !important;
        align-items: center !important;
        padding: 12px 16px !important;
        gap: 12px !important;
    }}

    details[data-testid="stExpander"] summary > div,
    details[data-testid="stExpander"] summary p,
    details[data-testid="stExpander"] summary span {{
        margin-left: 6px !important;
        padding-left: 6px !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
