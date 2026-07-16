import streamlit as st
import tempfile
from pathlib import Path
from datetime import timedelta


def render_sidebar(pipeline):

    st.sidebar.header("Conversation")

    uploaded_file = st.sidebar.file_uploader(
        "Upload WhatsApp Chat (.txt)",
        type=["txt"],
    )

    if uploaded_file is None:
        return None

    if "conversation_id" not in st.session_state:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt",
        ) as tmp:

            tmp.write(uploaded_file.getvalue())
            temp_path = tmp.name

        with st.spinner("Processing Conversation..."):

            conversation_id = pipeline.ingest(
                temp_path
            )

        Path(temp_path).unlink(
            missing_ok=True
        )

        st.session_state["conversation_id"] = conversation_id

    conversation_id = st.session_state["conversation_id"]

    min_date, max_date = pipeline.get_date_range(
        conversation_id
    )

    st.sidebar.divider()

    quick_filter = st.sidebar.radio(
        "Quick Filter",
        [
            "Entire Chat",
            "Latest Day",
            "Last 7 Days",
            "Last 30 Days",
            "Custom",
        ],
    )

    if quick_filter == "Entire Chat":

        start_date = min_date
        end_date = max_date

    elif quick_filter == "Latest Day":

        start_date = max_date
        end_date = max_date

    elif quick_filter == "Last 7 Days":

        end_date = max_date
        start_date = end_date - timedelta(days=7)

    elif quick_filter == "Last 30 Days":

        end_date = max_date
        start_date = end_date - timedelta(days=30)

    else:

        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
        )

        if len(date_range) != 2:
            st.stop()

        start_date, end_date = date_range

    analyze = st.sidebar.button(
        "Analyze",
        use_container_width=True,
    )

    return (
        conversation_id,
        start_date,
        end_date,
        analyze,
    )