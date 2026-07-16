import streamlit as st

from backend.agents.conversation_agent import ConversationAgent


def analyze_conversation(
    pipeline,
    conversation_id,
    start_date,
    end_date,
    min_date,
    max_date,
):

    messages = pipeline.get_messages(
        conversation_id,
        start_date,
        end_date,
    )

    if not messages:

        st.warning("No messages found.")
        st.stop()

    participants = sorted(
        {
            msg.sender
            for msg in messages
        }
    )

    db = pipeline.db

    if (
        start_date == min_date
        and end_date == max_date
    ):

        cached = db.get_ai_insights(
            conversation_id
        )

    else:

        cached = None

    if cached:

        result = cached

    else:

        with st.spinner(
            "Generating AI Insights..."
        ):

            result = ConversationAgent().analyze(
                messages
            )

            if (
                start_date == min_date
                and end_date == max_date
            ):

                db.save_ai_insights(
                    conversation_id,
                    result,
                )

    st.session_state["analysis_result"] = result
    st.session_state["messages"] = messages
    st.session_state["participants"] = participants
    st.session_state["start_date"] = start_date
    st.session_state["end_date"] = end_date