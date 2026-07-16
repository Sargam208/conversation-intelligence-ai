import streamlit as st


def feature_card(title, desc):

    st.markdown(
        f"""
        <div style="
            background:rgba(255,255,255,.05);
            border:1px solid rgba(255,255,255,.10);
            border-radius:20px;
            padding:28px;
            height:185px;
            box-shadow:0 10px 25px rgba(0,0,0,.20);
        ">

        <div style="
            font-size:30px;
            font-weight:700;
            margin-bottom:16px;
        ">
        {title}
        </div>

        <div style="
            font-size:17px;
            line-height:1.7;
            opacity:.82;
        ">
        {desc}
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def render_landing():

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align:center;">

        <div style="
            font-size:68px;
            font-weight:900;
            color:#0F172A;
            letter-spacing:-2px;
            margin-bottom:20px;
        ">

        Conversation Intelligence AI

        </div>

        <div style="
            font-size:24px;
            color:#475569;
            max-width:900px;
            margin:auto;
            line-height:1.8;
            font-weight:500;
        ">

        Transform WhatsApp conversations into
        AI-powered summaries, action items,
        decisions, analytics and semantic search.

        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")
    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        feature_card(
            "Executive Summary",
            "Generate concise AI summaries of lengthy conversations.",
        )

    with c2:
        feature_card(
            "Smart Q&A",
            "Ask natural language questions using Retrieval-Augmented Generation.",
        )

    with c3:
        feature_card(
            "Analytics",
            "Visualize participant activity, trends and engagement.",
        )

    st.write("")

    c4, c5, c6 = st.columns(3)

    with c4:
        feature_card(
            "Action Items",
            "Automatically identify tasks, assignees and deadlines.",
        )

    with c5:
        feature_card(
            "Key Decisions",
            "Extract important decisions with confidence scores.",
        )

    with c6:
        feature_card(
            "Date Filters",
            "Analyze the complete chat or any custom date range.",
        )

    st.write("")
    st.write("")
    st.write("")

    c1, c2, c3 = st.columns([2.5, 1.5, 2.5])

    with c2:

        if st.button(
            "Get Started →",
            use_container_width=True,
        ):

            st.session_state["started"] = True
            st.rerun()

    st.write("")
    st.write("")

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:14px;
            color:#64748B;
            opacity:.8;
        ">

        Built with
        <b>LangChain</b> •
        <b>Groq</b> •
        <b>ChromaDB</b> •
        <b>Sentence Transformers</b> •
        <b>Streamlit</b>

        </div>
        """,
        unsafe_allow_html=True,
    )