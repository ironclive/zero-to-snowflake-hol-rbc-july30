import streamlit as st

st.title("📱 Streamlit in Snowflake")

st.markdown("**Duration:** ~20 minutes")

st.markdown("---")

st.markdown("""
## What is Streamlit in Snowflake?

**Streamlit** is a Python framework for building interactive data apps — dashboards, forms, 
visualizations — with just a few lines of code. **Streamlit in Snowflake (SiS)** lets you run 
these apps entirely inside your Snowflake account, with no external servers, no deployment 
pipelines, and no data leaving Snowflake.

**Key concepts for this section:**

| Concept | What it means |
|---------|--------------|
| **Streamlit** | An open-source Python library where you write code like `st.bar_chart(data)` and get an interactive web app. |
| **Streamlit in Snowflake** | Run Streamlit apps natively inside Snowflake. The app queries live data, respects all governance policies, and is shared via roles. |
| **Compute Pool** | SiS apps run on compute pools (not warehouses). Each appcode environment has its own compute pool automatically assigned. |
| **`get_active_session()`** | Connects your app to Snowflake — no credentials needed since you're already running inside the platform. |
| **Snowpark** | Snowflake's Python API for querying and transforming data. Used in SiS apps to run SQL and get DataFrames. |
| **Role-based sharing** | Share your app with any role in your account. Users see only the data their role permits (masking + row access apply automatically). |

**Why this matters in banking:**
- Build internal dashboards without provisioning web servers
- Data never leaves Snowflake — no export, no external BI tool credentials
- Governance policies (masking, row access) apply automatically to app queries
- Non-technical stakeholders get self-service analytics with filters and charts
- Apps can be built in minutes, not weeks

**In this section**, we'll create a banking dashboard with filters, metrics, and charts — entirely inside Snowflake.
""")

st.markdown("---")

st.header("Objectives")

st.markdown("""
By the end of this section, you will be able to:

- Understand what Streamlit in Snowflake (SiS) is
- Create an interactive data app directly inside Snowflake
- Build filters, charts, and metrics from your banking data
- Share apps securely via role-based access
""")

st.markdown("---")

st.header("Part A: What is Streamlit in Snowflake?")

st.markdown("""
Streamlit in Snowflake lets you build **interactive Python data applications** that run entirely 
within your Snowflake account — no external infrastructure, no data movement, no separate 
authentication. Apps run on **compute pools** (automatically assigned) and execute with the 
permissions of the owning role. Data never leaves Snowflake.
""")

st.info("""
**Banking Relevance:** Build internal dashboards, self-service analytics tools, and operational 
monitoring apps that are governed by the same RBAC, masking, and row access policies you already have.
""")

st.markdown("---")

st.header("Part B: Create a Streamlit App")

st.markdown("#### Exercise 8.1 — Create a new Streamlit app in Workspaces")

st.markdown("""
1. In Snowsight, click **Projects → Workspaces** in the left navigation
2. Click the **+** button and select **Streamlit App**
3. Configure:
   - **App name:** `Banking_Dashboard`
   - **Database:** `TU30_ZERO_TO_SNOWFLAKE_LAB`
   - **Schema:** `RETAIL_BANKING_XX` (your participant number)
4. Click **Create**

The app will automatically be assigned a **compute pool** — no warehouse configuration needed.
""")

st.markdown("#### Exercise 8.2 — Replace the default code")

st.markdown("Delete the template code and paste the following:")

st.code("""
import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()
session.sql("USE DATABASE TU30_ZERO_TO_SNOWFLAKE_LAB").collect()
session.sql("USE SCHEMA RETAIL_BANKING").collect()

st.title("🏦 Retail Banking Dashboard")
st.markdown("Interactive view of customer and transaction data.")

# --- Filters ---
st.sidebar.header("Filters")

provinces = session.sql("SELECT DISTINCT PROVINCE FROM CUSTOMERS ORDER BY 1").collect()
province_list = ["All"] + [row[0] for row in provinces]
selected_province = st.sidebar.selectbox("Province", province_list)

segments = session.sql("SELECT DISTINCT CUSTOMER_SEGMENT FROM CUSTOMERS ORDER BY 1").collect()
segment_list = ["All"] + [row[0] for row in segments]
selected_segment = st.sidebar.selectbox("Segment", segment_list)

# --- Build query ---
where_clauses = []
if selected_province != "All":
    where_clauses.append(f"c.PROVINCE = '{selected_province}'")
if selected_segment != "All":
    where_clauses.append(f"c.CUSTOMER_SEGMENT = '{selected_segment}'")

where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

# --- Metrics ---
metrics_df = session.sql(f\"\"\"
    SELECT
        COUNT(DISTINCT c.CUSTOMER_ID) AS customers,
        COUNT(t.TRANSACTION_ID) AS transactions,
        SUM(t.AMOUNT) AS total_volume,
        AVG(t.AMOUNT) AS avg_transaction
    FROM CUSTOMERS c
    LEFT JOIN TRANSACTIONS t ON c.CUSTOMER_ID = t.CUSTOMER_ID
    {where_sql}
\"\"\").collect()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers", f"{metrics_df[0][0]:,}")
col2.metric("Transactions", f"{metrics_df[0][1]:,}")
col3.metric("Total Volume", f"${metrics_df[0][2]:,.0f}")
col4.metric("Avg Transaction", f"${metrics_df[0][3]:,.2f}")

st.markdown("---")

# --- Transactions by Channel ---
st.subheader("Transactions by Channel")
channel_df = session.sql(f\"\"\"
    SELECT t.CHANNEL, COUNT(*) AS count, SUM(t.AMOUNT) AS total
    FROM TRANSACTIONS t
    JOIN CUSTOMERS c ON t.CUSTOMER_ID = c.CUSTOMER_ID
    {where_sql}
    GROUP BY t.CHANNEL
    ORDER BY total DESC
\"\"\").to_pandas()

st.bar_chart(channel_df.set_index("CHANNEL")["TOTAL"])

# --- Top Products ---
st.subheader("Top Products by Revenue")
product_df = session.sql(f\"\"\"
    SELECT p.PRODUCT_NAME, SUM(t.AMOUNT) AS revenue
    FROM TRANSACTIONS t
    JOIN PRODUCTS p ON t.PRODUCT_ID = p.PRODUCT_ID
    JOIN CUSTOMERS c ON t.CUSTOMER_ID = c.CUSTOMER_ID
    {where_sql}
    GROUP BY p.PRODUCT_NAME
    ORDER BY revenue DESC
    LIMIT 10
\"\"\").to_pandas()

st.bar_chart(product_df.set_index("PRODUCT_NAME")["REVENUE"])
""", language="python")

st.markdown("#### Exercise 8.3 — Run the app")

st.markdown("""
1. Click **Run** (top-left) to execute the app
2. Use the sidebar filters to explore data by Province and Segment
3. Observe how metrics and charts update in real-time

> 💡 **Tip:** The **Deploy** button (top-right) creates the Streamlit object in your schema for publishing.
""")

st.success("""
**What happened?** You built a fully interactive dashboard that queries live Snowflake data, 
respects your governance policies (masking, row access), and requires zero external infrastructure. 
The app runs on a compute pool — no warehouse needed.
""")

st.markdown("---")

st.header("Part C: Key Features to Explore")

st.markdown("""
Try these enhancements in the app editor:

**Add a data table:**
```python
st.subheader("Recent Transactions")
recent = session.sql(f\"\"\"
    SELECT t.TRANSACTION_DATE, c.FIRST_NAME, c.LAST_NAME,
           p.PRODUCT_NAME, t.AMOUNT, t.CHANNEL
    FROM TRANSACTIONS t
    JOIN CUSTOMERS c ON t.CUSTOMER_ID = c.CUSTOMER_ID
    JOIN PRODUCTS p ON t.PRODUCT_ID = p.PRODUCT_ID
    {where_sql}
    ORDER BY t.TRANSACTION_DATE DESC
    LIMIT 20
\"\"\").to_pandas()
st.dataframe(recent, use_container_width=True)
```

**Add a download button:**
```python
csv = recent.to_csv(index=False)
st.download_button("Download CSV", csv, "transactions.csv", "text/csv")
```
""")

st.markdown("---")

st.markdown("---")

with st.expander("🤖 :blue[CoCo Sneak Peek] — Do this with Cortex Code"):
    st.markdown("""
CoCo can build entire Streamlit apps from a description:

| What you did | CoCo prompt |
|-------------|-------------|
| Scaffold an app | `Build me a Streamlit in Snowflake app that shows a banking dashboard with filters for province and segment` |
| Add charts | `Add a bar chart showing transactions by channel` |
| Add filters | `Add a sidebar selectbox to filter by CUSTOMER_SEGMENT` |
| Add metrics | `Show KPI metrics for total customers, transactions, and volume at the top` |
| Add a table | `Add a data table showing the 20 most recent transactions` |

CoCo writes the full Python code, tests it, and can deploy it — all from natural language.
""")

st.markdown("---")

st.header("Key Concepts")

st.markdown("""
| Feature | Description |
|---------|-------------|
| `get_active_session()` | Connect to Snowflake from within SiS (no credentials needed) |
| Compute Pool | SiS apps run on compute pools, automatically assigned per appcode |
| Snowpark DataFrames | Query and transform data using Python |
| Sidebar filters | `st.sidebar.selectbox()` for interactive filtering |
| Charts | `st.bar_chart()`, `st.line_chart()`, `st.area_chart()` |
| Governance | Masking and row access policies apply automatically |
| Sharing | Role-based access to apps via Workspaces |
""")
