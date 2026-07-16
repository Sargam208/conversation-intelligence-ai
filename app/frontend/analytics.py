import streamlit as st
import pandas as pd
from frontend.cards import card_start, card_end


def render_analytics(messages):
    card_start()

    st.subheader("Conversation Analytics")

    df = pd.DataFrame(
        [
            {
                "sender": msg.sender,
                "message": msg.message,
                "timestamp": msg.timestamp,
            }
            for msg in messages
        ]
    )

    if df.empty:

        st.info("No data available.")
        return

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Messages",
        len(df),
    )

    c2.metric(
        "Participants",
        df["sender"].nunique(),
    )

    c3.metric(
        "Most Active",
        df["sender"].value_counts().idxmax(),
    )

    st.divider()

    st.subheader("Messages per Participant")

    participant_counts = (
        df["sender"]
        .value_counts()
    )

    st.bar_chart(
        participant_counts
    )

    st.divider()

    st.subheader("Activity Timeline")

    df["date"] = pd.to_datetime(
        df["timestamp"]
    ).dt.date

    daily_messages = (
        df.groupby("date")
        .size()
    )

    st.line_chart(
        daily_messages
    )
    card_end()