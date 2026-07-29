import streamlit as st

st.title("📋 Agenda")

st.markdown("**Zero to Snowflake Hands-on Lab — July 30, 2026**")

st.markdown("---")

st.markdown("""
| Time | Duration | Section | Topic |
|------|----------|---------|-------|
| 9:00 AM | 15 min | — | **Welcome & Introductions** |
| 9:15 AM | 20 min | Section 1 | **Snowflake UI Tour** — Navigate Snowsight, set context, explore data |
| 9:35 AM | 40 min | Section 2 | **Querying & Analytics** — Joins, aggregations, window functions |
| 10:15 AM | 15 min | — | ☕ **Break** |
| 10:30 AM | 20 min | Section 3 | **Results Cache & Cloning** — Caching layers, zero-copy clones |
| 10:50 AM | 15 min | Section 4 | **Time Travel & UNDROP** — Historical queries, data recovery |
| 11:05 AM | 20 min | Section 5 | **Dynamic Tables** — Medallion architecture, auto-refreshing pipelines |
| 11:25 AM | 10 min | — | ☕ **Break** |
| 11:35 AM | 20 min | Section 6 | **Marketplace Data** — Subscribe to free data, enrich banking tables |
| 11:55 AM | 20 min | Section 7 | **Governance** — Masking policies, row access policies |
| 12:15 PM | 20 min | Section 8 | **Streamlit in Snowflake** — Build an interactive dashboard |
| 12:35 PM | 10 min | — | **Wrap-up & Q&A** |
| 12:45 PM | — | — | **End** |
""")

st.markdown("---")

st.info("""
**Total time:** ~3 hours 45 minutes (including breaks)

**Format:**
- Each section combines brief instructor guidance with hands-on exercises
- Follow along with the instructor — raise your hand if you need help
- CoCo Sneak Peeks in each section show how Cortex Code can accelerate your workflow
""")
