import streamlit as st
from frontend.cards import card_start, card_end


def render_decisions(result):

    with st.container():

        st.subheader("Important Decisions")

        if result.important_decisions:

            for decision in result.important_decisions:

                st.markdown(
                    f"### {decision.title}"
                )

                st.write(
                    decision.details
                )

                st.caption(
                    f"Confidence: {decision.confidence}"
                )

                st.divider()

        else:

            st.info(
                "No important decisions found."
            )
        card_end()