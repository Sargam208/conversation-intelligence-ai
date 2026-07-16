import streamlit as st

def card_start():

    st.markdown(
        """
        <div class="glass-card">
        """,
        unsafe_allow_html=True,
    )

def card_end():

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True,
    )