import streamlit as st

st.title("🖥️ The Snowflake UI Tour")
st.markdown("**Duration:** ~20 minutes")
st.markdown("---")

st.markdown("""
## What is Snowflake?

Snowflake is a **cloud data platform** — it stores and processes your data entirely in the cloud 
(AWS, Azure, or GCP). Unlike traditional databases that require you to install software and manage 
servers, Snowflake is fully managed: you just open a browser and start working.

**Key things that make Snowflake different:**

| Concept | What it means |
|---------|--------------|
| **Separation of storage & compute** | Your data is stored independently from the compute power that queries it. You can scale one without the other. |
| **Virtual Warehouses** | These are your compute engines. They start in seconds, auto-suspend when idle, and you only pay for what you use. |
| **Zero administration** | No indexes to build, no vacuuming, no tuning. Snowflake handles performance automatically. |
| **Snowsight** | The web-based UI where you write SQL, explore data, build charts, and manage your account. |

**In this section**, we'll tour Snowsight and get comfortable navigating before we start writing queries.
""")

st.markdown("---")

st.markdown("""
## Objectives

By the end of this section, you will be able to:
- Log in to Snowsight (Snowflake's web UI)
- Navigate the key areas: Worksheets, Databases, Warehouses, Marketplace
- Create and configure a SQL file
- Set your session context (role, warehouse, database, schema)
- Browse database objects and preview table data
""")

st.markdown("---")

st.markdown("""
## Step 1: Log in to Snowsight

1. Open your Snowflake account URL in a browser.
2. Log in using **SSO** (Single Sign-On).
3. You will land on the **Home** page.

> 💡 **Tip:** Bookmark your Snowflake URL for quick access.
""")

st.markdown("---")

st.markdown("""
## Step 2: Explore the Left Navigation

Take a moment to explore the left sidebar:

| Section | What It Contains |
|---------|-----------------|
| **Projects → Workspaces** | SQL editor — where you'll spend most of your time |
| **Projects → Dashboards** | Visual dashboards built from queries |
| **Catalog → Database Explorer** | Browse all databases, schemas, tables, views |
| **Data Products → Marketplace** | Free and paid data listings from providers |
| **Monitoring → Query History** | All queries run in your account |
| **Admin → Warehouses** | Compute resources (virtual warehouses) |
| **Admin → Users & Roles** | Identity and access management |
""")

st.markdown("---")

st.markdown("""
## Step 3: Create a New SQL File

1. Click **Projects → Workspaces** in the left nav.
2. Click the **+ Add New** button (top left) and select **SQL File**.
3. A new SQL file opens.

> 📝 **Name your file** by clicking the auto-generated name at the top and renaming it to: `Zero to Snowflake Lab`
""")

st.markdown("---")

st.markdown("""
## Step 4: Set Your Context

In your new SQL file, set the session context by running:
""")

st.code("""
USE ROLE TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX;  -- Replace XX with your seat number
USE WAREHOUSE TU30_ZERO_TO_SNOWFLAKE_LAB_WH;
USE DATABASE TU30_ZERO_TO_SNOWFLAKE_LAB;
USE SCHEMA RETAIL_BANKING_XX;  -- Replace XX with your seat number
""", language="sql")

st.info("💡 You can also set context using the dropdowns at the top of the SQL file.")

st.markdown("---")

st.markdown("""
## Step 5: Browse the Data

Navigate to **Catalog → Database Explorer** and drill into:

```
TU30_ZERO_TO_SNOWFLAKE_LAB → RETAIL_BANKING_XX → Tables
```

You should see three tables: **CUSTOMERS**, **PRODUCTS**, **TRANSACTIONS**.

Click on any table to see:
- **Columns** — data types and structure
- **Data Preview** — sample rows (no query required!)
- **Details** — row count, size, owner
""")

st.markdown("---")

st.markdown("""
## Step 6: Quick Preview from the SQL File

Back in your SQL file, run these quick queries to confirm your data is ready:
""")

st.code("""
-- How many customers?
SELECT COUNT(*) AS customer_count FROM CUSTOMERS;

-- How many products?
SELECT COUNT(*) AS product_count FROM PRODUCTS;

-- How many transactions?
SELECT COUNT(*) AS transaction_count FROM TRANSACTIONS;
""", language="sql")

st.success("""
**Expected Results:**
- Customers: 500
- Products: 15  
- Transactions: 1,000
""")

st.markdown("---")

with st.expander("🤖 :blue[CoCo Sneak Peek] — Do this with Cortex Code"):
    st.markdown("""
Instead of navigating the UI manually, you could ask **Cortex Code (CoCo)** to do it for you:

| What you did | CoCo prompt |
|-------------|-------------|
| Set context | `Use role TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX, warehouse TU30_ZERO_TO_SNOWFLAKE_LAB_WH, database TU30_ZERO_TO_SNOWFLAKE_LAB, schema RETAIL_BANKING_XX` |
| Browse tables | `What tables are in my current schema?` |
| Preview data | `Show me the first 10 rows of CUSTOMERS` |
| Check row counts | `How many rows are in each table in my schema?` |
| Explore columns | `Describe the TRANSACTIONS table` |

CoCo executes SQL on your behalf and returns formatted results — no SQL file needed.
""")

st.markdown("---")

st.markdown("""
## ✅ Section Complete!

You've successfully:
- Logged into Snowsight
- Navigated the UI
- Created a SQL file and set your context
- Confirmed access to the retail banking data

**Next →** Head to **Section 2: Querying & Analytics** to start writing real queries.
""")
