import streamlit as st
from frontend.cards import card_start, card_end


def render_summary(result):

    with st.container():

        st.subheader("Executive Summary")

        st.write(
            result.executive_summary
        )

        card_end()