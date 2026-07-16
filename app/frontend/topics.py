import streamlit as st
from frontend.cards import card_start, card_end

def render_topics(result):

    with st.container():

        st.subheader("Key Discussion Points")

        if result.key_discussion_points:

            for topic in result.key_discussion_points:

                st.markdown(
                    f"- {topic}"
                )

        else:

            st.info(
                "No discussion topics found."
            )
        card_end()