import streamlit as st


def render_metrics(
    messages,
    participants,
    start_date,
    end_date,
):

    formatted_start = start_date.strftime("%d %b %Y")
    formatted_end = end_date.strftime("%d %b %Y")

    c1, c2, c3 = st.columns([1, 1, 2])

    with c1:
        st.subheader("Messages")
        st.write(str(len(messages)))

    with c2:
        st.subheader("Participants")
        st.write(str(len(participants)))

    with c3:
        st.subheader("Date Range")
        st.write(f"{formatted_start} → {formatted_end}")