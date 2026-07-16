import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st

from backend.pipeline.ingestion_pipeline import IngestionPipeline

from controller.app_controller import run_app
from config import FAVICON

from frontend.styles import apply_styles
from frontend.landing import render_landing


st.markdown(
    """
    <style>
    /* Matches your image transition: Deep blue fading to bright cloud white */
    .stApp {
        background: linear-gradient(to bottom, #2E93D7 0%, #5CB3FF 35%, #B9E3FF 70%, #FFFFFF 100%);
        background-attachment: fixed;
    }

    /* Invisible header keeping the gradient uniform */
    header {
        background: transparent !important;
    }

    /* Text input containers tailored for high readability */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #102A43 !important;
        border: 1px solid #5CB3FF !important;
        border-radius: 8px;
    }

    /* Clean, modern button style to match the layout */
    .stButton>button {
        background-color: #1D70B8 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        box-shadow: 0px 4px 10px rgba(29, 112, 184, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(
    page_title="Conversation Intelligence AI",
    page_icon=str(FAVICON),
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()
if "started" not in st.session_state:

    render_landing()

    st.stop()

pipeline = IngestionPipeline()

run_app(pipeline)

