import streamlit as st

from controller.analysis import analyze_conversation

from frontend.sidebar import render_sidebar
from frontend.metrics import render_metrics
from frontend.tabs import render_tabs
from frontend.assistant import render_assistant
from config import LOGO


def run_app(pipeline):

    
    st.markdown(
        """
        <h1 style="margin-bottom:0;">
        Conversation Intelligence AI
        </h1>

        <p style="
            color:#64748B;
            margin-top:-12px;
            font-size:18px;">
            Turning Conversations into Insights
        </p>
        """,
        unsafe_allow_html=True,
    )

    sidebar = render_sidebar(pipeline)

    if sidebar is None:
        st.stop()

    (
        conversation_id,
        start_date,
        end_date,
        analyze,
    ) = sidebar

    min_date, max_date = pipeline.get_date_range(
        conversation_id
    )

    if analyze:

        analyze_conversation(
            pipeline,
            conversation_id,
            start_date,
            end_date,
            min_date,
            max_date,
        )

    if "analysis_result" not in st.session_state:
        st.stop()

    result = st.session_state["analysis_result"]

    messages = st.session_state["messages"]

    participants = st.session_state["participants"]

    start_date = st.session_state["start_date"]

    end_date = st.session_state["end_date"]

    render_metrics(
        messages,
        participants,
        start_date,
        end_date,
    )

    render_tabs(
        result,
        messages,
    )

    render_assistant(
        conversation_id,
    )