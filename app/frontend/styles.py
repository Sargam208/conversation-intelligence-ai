import streamlit as st


def apply_styles():

    st.markdown(
        """
<style>

/* ===========================
   Layout
=========================== */

.block-container{

    max-width:1400px;

    padding-top:2rem;

    padding-bottom:3rem;

}

/* ===========================
   Sidebar
=========================== */

section[data-testid="stSidebar"]{

    border-right:1px solid rgba(255,255,255,.08);

}

/* ===========================
   Metrics
=========================== */

div[data-testid="metric-container"]{

    border-radius:18px;

    padding:18px;

    border:1px solid rgba(255,255,255,.08);

    background:rgba(255,255,255,.03);

    backdrop-filter:blur(10px);

}

/* ===========================
   Buttons
=========================== */

.stButton>button{

    width:100%;

    height:48px;

    border-radius:14px;

    border:none;

    font-weight:600;

}

/* ===========================
   Chat Input
=========================== */

.stChatInput{

    border-radius:16px;

}

/* ===========================
   Tabs
=========================== */

.stTabs [data-baseweb="tab-list"]{
    gap: 18px;
    border-bottom: none;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"]{

    background: rgba(255,255,255,.22);

    border: 1px solid rgba(255,255,255,.25);

    border-radius: 14px;

    padding: 12px 26px;

    font-size:18px;

    font-weight:600;

    color:#1E293B;

    transition:all .25s ease;

}

.stTabs [data-baseweb="tab"]:hover{

    background:rgba(255,255,255,.35);

    transform:translateY(-2px);

}

.stTabs [aria-selected="true"]{

    background:linear-gradient(
        90deg,
        #2563EB,
        #3B82F6
    ) !important;

    color:white !important;

    border:none !important;

    box-shadow:
        0 8px 24px rgba(37,99,235,.30);

}

.stTabs [aria-selected="true"] p{

    color:white !important;

}

.stTabs [data-baseweb="tab-highlight"]{

    display:none;

}

/* ===========================
   Glass Cards
=========================== */

.glass-card{

    background:rgba(255,255,255,.03);

    border:1px solid rgba(255,255,255,.08);

    backdrop-filter:blur(12px);

    border-radius:20px;

    padding:24px;

    margin-bottom:24px;

}

/* ===========================
   Tables
=========================== */

table{

    border-radius:14px;

    overflow:hidden;

}

/* ===========================
   Alerts
=========================== */

.stAlert{

    border-radius:14px;

}

/* ===========================
   Divider
=========================== */

hr{

    opacity:.2;

}

</style>
""",
        unsafe_allow_html=True,
    )