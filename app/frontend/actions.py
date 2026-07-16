import streamlit as st
from frontend.cards import card_start, card_end

def render_actions(result):
    card_start()

    with st.container():

        st.subheader("Action Items")

        if result.action_items:

            table = []

            for item in result.action_items:

                table.append(
                    {
                        "Assignee": (
                            item.assignee
                            if item.assignee
                            else "Unknown"
                        ),
                        "Task": item.task,
                        "Deadline": (
                            item.deadline
                            if item.deadline
                            else "-"
                        ),
                        "Priority": item.priority,
                    }
                )

            st.table(table)

        else:

            st.info(
                "No action items found."
            )
        card_end()