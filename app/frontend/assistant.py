import streamlit as st

from backend.agents.qa_agent import qa_agent
from frontend.cards import card_start, card_end


def render_assistant(conversation_id):
    card_start()

    st.divider()

    st.subheader(
        "Conversation Assistant"
    )

    st.caption(
        "Ask questions about the uploaded conversation."
    )

    question = st.chat_input(
        "Ask anything about this conversation..."
    )

    if not question:
        return

    with st.chat_message("user"):

        st.write(question)

    with st.spinner("Thinking..."):

        try:

            qa = qa_agent(
                conversation_id
            )

            answer = qa.ask(
                question
            )

            with st.chat_message(
                "assistant"
            ):

                st.write(answer)
    

        except Exception as e:

            st.error(
                f"Error: {e}"
            )
    card_end()
