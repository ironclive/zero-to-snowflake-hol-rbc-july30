import streamlit as st

st.set_page_config(
    page_title="Zero to Snowflake HOL",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo("https://upload.wikimedia.org/wikipedia/commons/f/ff/Snowflake_Logo.svg")

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #F0F4F8;
    }
    [data-testid="stSidebarNavLink"] span {
        color: #1B2A4A !important;
        font-size: 0.95rem;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background-color: #E2E8F0 !important;
        border-radius: 6px;
    }
    .big-title {
        font-family: 'Source Sans Pro', sans-serif !important;
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        color: #1B2A4A !important;
        margin-bottom: 0 !important;
        margin-top: 0.5rem !important;
        line-height: 1.1 !important;
        padding: 0 !important;
    }
    .subtitle {
        font-size: 1.15rem !important;
        color: #5A6B7B !important;
        margin-top: 0.5rem !important;
        margin-bottom: 2.5rem !important;
        font-weight: 400 !important;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #5A6B7B;
        margin-bottom: 0.1rem;
        font-weight: 400;
    }
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #1B2A4A !important;
        line-height: 1.2 !important;
    }
    .coco-section {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 10px;
        padding: 0.5rem 0.5rem 0 0.5rem;
        margin: 1rem 0;
    }
    [data-testid="stExpander"] {
        background-color: #EFF6FF;
        border: 1px solid #BEE3F8;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/home.py", title="Home", icon=":material/home:"),
    st.Page("pages/getting_started.py", title="Getting Started", icon=":material/rocket_launch:"),
    st.Page("pages/agenda.py", title="Agenda", icon=":material/calendar_today:"),
    st.Page("pages/snowflake_ui_tour.py", title="1. Snowflake UI Tour", icon=":material/computer:"),
    st.Page("pages/querying_and_analytics.py", title="2. Querying and Analytics", icon=":material/query_stats:"),
    st.Page("pages/results_cache_and_cloning.py", title="3. Results Cache and Cloning", icon=":material/bolt:"),
    st.Page("pages/time_travel.py", title="4. Time Travel & UNDROP", icon=":material/history:"),
    st.Page("pages/dynamic_tables.py", title="5. Dynamic Tables", icon=":material/dynamic_feed:"),
    st.Page("pages/marketplace_data.py", title="6. Marketplace Data", icon=":material/storefront:"),
    st.Page("pages/governance.py", title="7. Governance", icon=":material/shield:"),
    st.Page("pages/streamlit_in_snowflake.py", title="8. Streamlit in Snowflake", icon=":material/dashboard:"),
])

pg.run()
