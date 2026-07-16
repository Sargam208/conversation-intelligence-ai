import streamlit as st

from frontend.summary import render_summary
from frontend.topics import render_topics
from frontend.decisions import render_decisions
from frontend.actions import render_actions
from frontend.analytics import render_analytics


def render_tabs(
    result,
    messages,
):

    (
        summary_tab,
        topic_tab,
        decision_tab,
        action_tab,
        analytics_tab,
    ) = st.tabs(
        [
            "Summary",
            "Topics",
            "Decisions",
            "Action Items",
            "Analytics",
        ]
    )

    with summary_tab:
        render_summary(result)

    with topic_tab:
        render_topics(result)

    with decision_tab:
        render_decisions(result)

    with action_tab:
        render_actions(result)

    with analytics_tab:
        render_analytics(messages)