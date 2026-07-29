import streamlit as st

st.markdown('<p class="big-title">Zero to Snowflake</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Hands-on Lab · July 30, 2026</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<p class="metric-label">Sections</p>', unsafe_allow_html=True)
    st.markdown('<p class="metric-value">8</p>', unsafe_allow_html=True)
with col2:
    st.markdown('<p class="metric-label">Exercises</p>', unsafe_allow_html=True)
    st.markdown('<p class="metric-value">30+</p>', unsafe_allow_html=True)
with col3:
    st.markdown('<p class="metric-label">Duration</p>', unsafe_allow_html=True)
    st.markdown('<p class="metric-value">3 hrs</p>', unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
### How this workshop works

Each section has **numbered exercises** that you run in a Snowflake SQL file:

- **Snowsight UI** — for navigating and exploring your data
- **SQL Worksheets** — for writing and running queries
- **Marketplace** — for subscribing to external data
- **Streamlit** — for building interactive apps

All exercises build on each other sequentially — work through them in order.
""")

st.markdown("---")

st.markdown("### The scenario")

st.info("""
You are a data analyst at a **Canadian retail bank**. You have access to customer, product, 
and transaction data and need to explore it, build analytics, and enrich it with external market data.

We'll work with a pre-provisioned dataset covering:

| Data type | Examples |
|-----------|----------|
| **Customers** | Demographics, segment, annual income, credit score, province |
| **Products** | Chequing, savings, credit card, mortgage, LOC, investments |
| **Transactions** | Purchases, deposits, withdrawals, transfers, payments across 5 channels |
""")

st.markdown("---")

st.markdown("### What you'll learn")

st.markdown("""
| # | Section | What you'll do |
|---|---------|---------------|
| 1 | **Snowflake UI Tour** | Navigate Snowsight, set context, explore tables |
| 2 | **Querying & Analytics** | Joins, aggregates, window functions, time-series |
| 3 | **Results Cache & Cloning** | Observe caching, create zero-copy clones |
| 4 | **Time Travel & UNDROP** | Query historical data, recover dropped objects |
| 5 | **Dynamic Tables** | Build declarative auto-refreshing pipelines |
| 6 | **Marketplace Data** | Subscribe to free data, join with banking tables |
| 7 | **Governance** | Column masking, row access policies |
| 8 | **Streamlit in Snowflake** | Build an interactive banking dashboard |
""")

st.markdown("---")

st.markdown("### Prerequisites")

st.markdown("""
- Access to a Snowflake account in the RBC AZ or AWS Sandbox
- Basic SQL knowledge (SELECT, WHERE, JOIN, GROUP BY)
- A modern web browser (Chrome, Edge, Firefox)
""")

st.markdown("---")

st.markdown("### Pre-provisioned data")

st.markdown("""
Your lab environment includes **`TU30_ZERO_TO_SNOWFLAKE_LAB.RETAIL_BANKING_XX`** (where XX is your seat number) with:
""")

st.markdown("""
| Table | Rows | Description |
|-------|------|-------------|
| `CUSTOMERS` | 500 | Canadian retail banking customers |
| `PRODUCTS` | 15 | Banking products |
| `TRANSACTIONS` | 1,000 | Transaction history |

**Relationships:**  
`TRANSACTIONS.CUSTOMER_ID` → `CUSTOMERS.CUSTOMER_ID`  
`TRANSACTIONS.PRODUCT_ID` → `PRODUCTS.PRODUCT_ID`
""")
