import streamlit as st

st.title("🔄 Dynamic Tables")

st.markdown("**Duration:** ~20 minutes")

st.markdown("---")

st.markdown("""
## What are Dynamic Tables?

In most data platforms, building a data pipeline means writing stored procedures, scheduling jobs 
with cron or Airflow, and managing complex orchestration. Snowflake's **Dynamic Tables** eliminate 
all of that — you just write a `SELECT` describing what you want, and Snowflake keeps the result 
up-to-date automatically.

**Key concepts for this section:**

| Concept | What it means |
|---------|--------------|
| **Dynamic Table** | A table defined by a SQL query that Snowflake automatically refreshes when source data changes. |
| **TARGET_LAG** | The maximum staleness you'll accept (e.g., `'1 minute'`). Snowflake ensures the table is never more stale than this. |
| **Declarative** | You say *what* you want (the SELECT), not *how* to get there. No scheduling, no incremental logic, no orchestration. |
| **Chaining** | Dynamic Tables can read from other Dynamic Tables, forming a pipeline (DAG). |
| **Medallion Architecture** | A pattern organizing data into Bronze (raw), Silver (enriched), and Gold (business-ready) layers. |

**Why this matters in banking:**
- Risk dashboards need fresh data without complex ETL pipelines
- Regulatory reporting requires traceable, repeatable transformations
- Teams want to build pipelines without depending on data engineering for orchestration
- The medallion pattern ensures data quality improves at each stage

**In this section**, we'll build a Bronze → Silver → Gold pipeline using Dynamic Tables.
""")

st.markdown("---")

st.header("Objectives")

st.markdown("""
By the end of this section, you will be able to:

- Understand the **Medallion Architecture** (Bronze → Silver → Gold)
- Build a medallion pipeline using Dynamic Tables
- See how data flows automatically through the layers
- Compare this approach to dbt as an alternative
""")

st.markdown("---")

st.header("Part A: The Medallion Architecture")

st.markdown("""
The **medallion architecture** is a data design pattern that organizes your pipeline into three layers, 
each increasing in quality and business value:
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    #### 🥉 Bronze
    **Raw source data**
    - Landed as-is from source systems
    - No transformations
    - Full history preserved
    """)
with col2:
    st.markdown("""
    #### 🥈 Silver
    **Cleaned & enriched**
    - Joins across sources
    - Data quality applied
    - Business logic added
    """)
with col3:
    st.markdown("""
    #### 🥇 Gold
    **Business-ready**
    - Aggregated KPIs
    - Dashboard-ready metrics
    - Consumption-optimized
    """)

st.markdown("")

st.info("""
**In our lab, the medallion layers map to:**

| Layer | Table(s) | What it represents |
|-------|----------|-------------------|
| 🥉 Bronze | `TRANSACTIONS`, `CUSTOMERS`, `PRODUCTS` | Raw source tables (already loaded) |
| 🥈 Silver | `TRANSACTION_ENRICHED` | Transactions joined with customer & product context |
| 🥇 Gold | `PRODUCT_PERFORMANCE` | Business KPIs — revenue, rankings, customer counts by product |
""")

st.markdown("---")

st.header("Part B: Building the Pipeline with Dynamic Tables")

st.markdown("""
**Dynamic Tables** let you define each medallion layer **declaratively** — you write a `SELECT` 
describing the desired result, and Snowflake keeps it up-to-date automatically as source data changes.
""")

st.markdown("#### Exercise 5.1 — Confirm your context")

st.info("Make sure you're still using your assigned role and schema from Section 1. If not, re-run the `USE ROLE` / `USE SCHEMA` commands from the Snowflake UI Tour.")

st.markdown("#### Exercise 5.2 — Silver Layer: Enrich transactions")

st.markdown("""
Our bronze tables are raw and isolated. The silver layer **joins** them together and adds business context:
""")

st.code("""
CREATE OR REPLACE DYNAMIC TABLE TRANSACTION_ENRICHED
    TARGET_LAG = '1 minute'
    WAREHOUSE = TU30_ZERO_TO_SNOWFLAKE_LAB_WH
AS
SELECT
    t.TRANSACTION_ID,
    t.TRANSACTION_DATE,
    t.AMOUNT,
    t.TRANSACTION_TYPE,
    t.CHANNEL,
    t.STATUS,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS customer_name,
    c.CUSTOMER_SEGMENT,
    c.PROVINCE,
    p.PRODUCT_NAME,
    p.PRODUCT_CATEGORY
FROM TRANSACTIONS t
JOIN CUSTOMERS c ON t.CUSTOMER_ID = c.CUSTOMER_ID
JOIN PRODUCTS p ON t.PRODUCT_ID = p.PRODUCT_ID;
""", language="sql")

st.markdown("#### Exercise 5.3 — Query the Silver layer")

st.code("""
SELECT * FROM TRANSACTION_ENRICHED
LIMIT 20;
""", language="sql")

st.success("""
**What happened?** The silver layer now has a single, enriched view of every transaction — 
with customer name, segment, province, and product details all in one place. No more JOINs 
needed downstream.
""")

st.markdown("---")

st.markdown("#### Exercise 5.4 — Gold Layer: Business KPIs")

st.markdown("""
The gold layer reads from silver and produces **aggregated, consumption-ready metrics**:
""")

st.code("""
CREATE OR REPLACE DYNAMIC TABLE PRODUCT_PERFORMANCE
    TARGET_LAG = '2 minutes'
    WAREHOUSE = TU30_ZERO_TO_SNOWFLAKE_LAB_WH
AS
SELECT
    PRODUCT_NAME,
    PRODUCT_CATEGORY,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT customer_name) AS unique_customers,
    SUM(AMOUNT) AS total_revenue,
    AVG(AMOUNT) AS avg_transaction_value,
    RANK() OVER (ORDER BY SUM(AMOUNT) DESC) AS revenue_rank
FROM TRANSACTION_ENRICHED
GROUP BY PRODUCT_NAME, PRODUCT_CATEGORY;
""", language="sql")

st.markdown("#### Exercise 5.5 — Query the Gold layer")

st.code("""
SELECT * FROM PRODUCT_PERFORMANCE
ORDER BY revenue_rank;
""", language="sql")

st.success("""
**The full pipeline:** `TRANSACTIONS` + `CUSTOMERS` + `PRODUCTS` (Bronze) → `TRANSACTION_ENRICHED` (Silver) → `PRODUCT_PERFORMANCE` (Gold)

Each layer refreshes automatically. Change a source table and the entire pipeline updates within minutes.
""")

st.markdown("---")

st.header("Part C: Simulate a Data Change")

st.markdown("""
Now let's see the pipeline in action. We'll insert **3 new transactions** into the Bronze layer 
(the `TRANSACTIONS` table) and then verify they automatically flow through to Silver and Gold.

We're inserting 3 × \\$5,000 deposits into **Essential Chequing** (Product ID 1) — that's \\$15,000 
of new revenue that should be easy to spot when it appears in the downstream layers.
""")

st.markdown("#### Exercise 5.6 — Insert 3 new transactions into Bronze")

st.code("""
INSERT INTO TRANSACTIONS (TRANSACTION_ID, CUSTOMER_ID, PRODUCT_ID, TRANSACTION_DATE, TRANSACTION_TYPE, AMOUNT, BALANCE_AFTER, CHANNEL, MERCHANT_CATEGORY, STATUS)
SELECT
    m.max_id + SEQ4() + 1,
    1,
    1,
    CURRENT_DATE(),
    'Deposit',
    5000.00,
    NULL,
    'Online',
    NULL,
    'Completed'
FROM (SELECT MAX(TRANSACTION_ID) AS max_id FROM TRANSACTIONS) m,
     TABLE(GENERATOR(ROWCOUNT => 3));
""", language="sql")

st.info("""
**What this does:** Inserts 3 rows of \\$5,000 each into the `TRANSACTIONS` table (Bronze layer). 
The `GENERATOR(ROWCOUNT => 3)` produces 3 rows, and `SEQ4()` gives each one a unique ID.

You should see: **"3 rows inserted"**
""")

st.markdown("#### Exercise 5.7 — Verify the data flows to Silver")

st.markdown("""
Wait **~1 minute** (the Silver layer has `TARGET_LAG = '1 minute'`), then run:
""")

st.code("""
SELECT * FROM TRANSACTION_ENRICHED
WHERE AMOUNT = 5000.00 AND TRANSACTION_DATE = CURRENT_DATE();
""", language="sql")

st.success("""
**Expected result:** 3 rows — your \\$5,000 deposits, now enriched with customer name, 
segment, province, product name, and category. The Dynamic Table automatically joined 
them with CUSTOMERS and PRODUCTS.
""")

st.markdown("#### Exercise 5.8 — Verify the data flows to Gold")

st.markdown("""
Wait **~2 more minutes** (the Gold layer has `TARGET_LAG = '2 minutes'`), then run:
""")

st.code("""
SELECT * FROM PRODUCT_PERFORMANCE
ORDER BY revenue_rank;
""", language="sql")

st.success("""
**What to look for:** Find **Essential Chequing** in the results. Before the insert, its baseline was:

- `total_transactions` = **70**
- `total_revenue` = **-$9,193.83**

After the pipeline refreshes, you should see:

- `total_transactions` = **73** (+3)
- `total_revenue` = **$5,806.17** (+$15,000)

This is the power of Dynamic Tables — one INSERT into Bronze, and the entire pipeline 
updates automatically. No scheduling, no orchestration, no code to maintain.
""")

st.markdown("---")

st.header("Part D: Visualize the DAG")

st.markdown("""
To see your medallion pipeline in Snowsight:

1. Navigate to **Catalog → Database Explorer**
2. Expand `TU30_ZERO_TO_SNOWFLAKE_LAB` → `RETAIL_BANKING_XX` → **Dynamic Tables**
3. Click on `PRODUCT_PERFORMANCE`
4. Select the **Graph** tab

You'll see the full lineage: Bronze sources → Silver (`TRANSACTION_ENRICHED`) → Gold (`PRODUCT_PERFORMANCE`)
""")

st.markdown("---")

st.header("Part E: Clean up")

st.code("""
DROP DYNAMIC TABLE IF EXISTS PRODUCT_PERFORMANCE;
DROP DYNAMIC TABLE IF EXISTS TRANSACTION_ENRICHED;

-- Remove the test transactions
DELETE FROM TRANSACTIONS WHERE AMOUNT = 5000.00 AND TRANSACTION_DATE = CURRENT_DATE();
""", language="sql")

st.markdown("---")

with st.expander("🤖 :blue[CoCo Sneak Peek] — Do this with Cortex Code"):
    st.markdown("""
CoCo can build entire medallion pipelines from a description:

| What you did | CoCo prompt |
|-------------|-------------|
| Silver layer | `Create a dynamic table TRANSACTION_ENRICHED that joins transactions with customers and products, refreshing every 1 minute` |
| Gold layer | `Create a dynamic table PRODUCT_PERFORMANCE that aggregates revenue and ranks products from TRANSACTION_ENRICHED, with 2 minute lag` |
| Insert test data | `Insert 3 test deposit transactions of $5000 each for customer 1, product 1` |
| Check flow | `Query TRANSACTION_ENRICHED to see if the new deposits flowed through` |
| Clean up | `Drop PRODUCT_PERFORMANCE and TRANSACTION_ENRICHED and delete today's $5000 test transactions` |

You can also ask: `Show me the DAG for my dynamic tables in RETAIL_BANKING_XX`
""")

st.markdown("---")

with st.expander("🔀 Alternative Approach — How would you do this with dbt?"):
    st.markdown("""
Many teams use **dbt (data build tool)** to implement the same medallion architecture — especially 
when they want version-controlled SQL, automated testing, and CI/CD governance.

### Same pipeline, different tool

In dbt, each layer is a **model** (a `.sql` file). dbt resolves dependencies via `{{ ref() }}`, 
runs them in order, and materializes results as tables or views in Snowflake.

```
models/
├── staging/          ← Bronze (thin wrappers on source tables)
│   ├── stg_transactions.sql
│   ├── stg_customers.sql
│   └── stg_products.sql
├── intermediate/     ← Silver (joins, enrichment)
│   └── transaction_enriched.sql
└── marts/            ← Gold (business KPIs)
    └── product_performance.sql
```

**Silver: `models/intermediate/transaction_enriched.sql`**
```sql
SELECT
    t.TRANSACTION_ID,
    t.TRANSACTION_DATE,
    t.AMOUNT,
    t.TRANSACTION_TYPE,
    t.CHANNEL,
    t.STATUS,
    c.FIRST_NAME || ' ' || c.LAST_NAME AS customer_name,
    c.CUSTOMER_SEGMENT,
    c.PROVINCE,
    p.PRODUCT_NAME,
    p.PRODUCT_CATEGORY
FROM {{ ref('stg_transactions') }} t
JOIN {{ ref('stg_customers') }} c ON t.CUSTOMER_ID = c.CUSTOMER_ID
JOIN {{ ref('stg_products') }} p ON t.PRODUCT_ID = p.PRODUCT_ID
```

**Gold: `models/marts/product_performance.sql`**
```sql
SELECT
    PRODUCT_NAME,
    PRODUCT_CATEGORY,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT customer_name) AS unique_customers,
    SUM(AMOUNT) AS total_revenue,
    AVG(AMOUNT) AS avg_transaction_value,
    RANK() OVER (ORDER BY SUM(AMOUNT) DESC) AS revenue_rank
FROM {{ ref('transaction_enriched') }}
GROUP BY 1, 2
```

Then run: `dbt run` — dbt builds Bronze → Silver → Gold in dependency order.

### When to use which?

| | Dynamic Tables | dbt |
|-|---------------|-----|
| **Orchestration** | None — Snowflake auto-refreshes | Requires scheduler (cron, Airflow, dbt Cloud) |
| **Freshness** | Near real-time (TARGET_LAG) | Batch (e.g., hourly, daily) |
| **Version control** | SQL lives in Snowflake | SQL lives in Git with PR reviews |
| **Testing** | Manual validation | Built-in tests (`not_null`, `unique`, custom assertions) |
| **Documentation** | Snowsight Graph tab | Auto-generated docs site + lineage graph |
| **Incremental logic** | Automatic | Explicit (`is_incremental()` macro) |
| **Best for** | Real-time dashboards, simple pipelines | Governed, testable, CI/CD-driven pipelines |

**Bottom line:** Both implement the same medallion pattern. Dynamic Tables give you real-time 
freshness with zero orchestration. dbt gives you version control, testing, and CI/CD governance. 
Many teams use **both** — dbt for scheduled batch pipelines and Dynamic Tables for low-latency use cases.
""")

st.markdown("---")

st.header("Key Concepts")

st.markdown("""
| Feature | Description |
|---------|-------------|
| Medallion Architecture | Bronze (raw) → Silver (enriched) → Gold (business-ready) |
| `TARGET_LAG` | Maximum allowed staleness (e.g., '1 minute', '1 hour') |
| Incremental refresh | Snowflake processes only changed data when possible |
| DAG visualization | See pipeline dependencies in Snowsight Graph tab |
| No orchestration | No Tasks, no cron — Snowflake handles scheduling |
| Chaining | Dynamic Tables can read from other Dynamic Tables |
""")
