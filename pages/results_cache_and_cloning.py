import streamlit as st

st.title("⚡ Results Cache & Cloning")
st.markdown("**Duration:** ~20 minutes")
st.markdown("---")

st.markdown("""
## Why Queries Are Fast (Even Without Tuning)

Traditional databases require you to build indexes, partition tables, and tune queries manually. 
Snowflake takes a different approach: it **automatically caches** results at multiple levels so 
repeat queries are instant, and it lets you **clone entire databases in seconds** without copying data.

**Key concepts for this section:**

| Concept | What it means |
|---------|--------------|
| **Results Cache** | If you run the exact same query twice (same SQL, same data), Snowflake returns the cached result in milliseconds — no compute used. |
| **Metadata Cache** | Simple queries like `COUNT(*)`, `MIN()`, `MAX()` are answered from metadata alone — no warehouse needed at all. |
| **Warehouse Cache** | Data recently scanned is kept on local SSD. Subsequent queries on the same data are faster. |
| **Zero-Copy Clone** | Create an instant, independent copy of a table, schema, or database. No data is duplicated — only changes are stored separately. |

**Why this matters in banking:**
- Dashboards that hit the same queries are essentially free (results cache)
- Dev/test environments can be spun up in seconds from production data (cloning)
- No storage penalty for maintaining development copies

**In this section**, we'll observe caching in action and create a zero-copy clone.
""")

st.markdown("---")

st.markdown("""
## Objectives

By the end of this section, you will be able to:
- Understand Snowflake's multi-layer caching architecture
- Observe the results cache in action (sub-second repeat queries)
- Create a zero-copy clone of a table
- Demonstrate that clones are independent from the source
""")

st.markdown("---")

st.header("Part A: The Results Cache")

st.markdown("""
### How Snowflake Caching Works

Snowflake has **three layers** of caching:

| Cache Layer | Scope | Duration | Cost |
|-------------|-------|----------|------|
| **Metadata Cache** | COUNT, MIN, MAX on columns | Indefinite | Free (no warehouse) |
| **Results Cache** | Exact same query, same data | 24 hours | Free (no warehouse) |
| **Warehouse Cache** | Data loaded into local SSD | Until warehouse suspends | Warehouse running |

### Exercise: Observe the Results Cache
""")

st.markdown("**Step 1:** Run this query and note the execution time in the **Query Profile**:")

st.code("""
SELECT C.CUSTOMER_SEGMENT,
       COUNT(DISTINCT T.CUSTOMER_ID) AS active_customers,
       SUM(T.AMOUNT) AS total_volume
FROM TRANSACTIONS T
JOIN CUSTOMERS C ON T.CUSTOMER_ID = C.CUSTOMER_ID
GROUP BY C.CUSTOMER_SEGMENT
ORDER BY total_volume DESC;
""", language="sql")

st.markdown("**Step 2:** Run the **exact same query** again immediately.")

st.info("""
💡 **What to observe:**
- The second run should complete in **milliseconds** (vs. seconds for the first)
- In the Query Profile, you'll see: `QUERY_RESULT_REUSE = true`
- No warehouse compute was consumed for the repeat query!
""")

st.markdown("**Step 3:** Now modify the query slightly (e.g., change the ORDER BY) and run again:")

st.code("""
SELECT C.CUSTOMER_SEGMENT,
       COUNT(DISTINCT T.CUSTOMER_ID) AS active_customers,
       SUM(T.AMOUNT) AS total_volume
FROM TRANSACTIONS T
JOIN CUSTOMERS C ON T.CUSTOMER_ID = C.CUSTOMER_ID
GROUP BY C.CUSTOMER_SEGMENT
ORDER BY active_customers DESC;  -- Changed!
""", language="sql")

st.warning("⚠️ The cache is **not reused** — even a minor change creates a different query hash.")

st.markdown("---")

st.markdown("""
### Exercise: Metadata Cache

Some queries don't need a warehouse at all. Try these with your warehouse **suspended**:
""")

st.code("""
-- Suspend your warehouse first
ALTER WAREHOUSE TU30_ZERO_TO_SNOWFLAKE_LAB_WH SUSPEND;

-- These still work (metadata cache)!
SELECT COUNT(*) FROM CUSTOMERS;
SELECT MIN(TRANSACTION_DATE) FROM TRANSACTIONS;
SELECT MAX(AMOUNT) FROM TRANSACTIONS;
""", language="sql")

st.success("These queries return instantly because Snowflake stores metadata (row counts, min/max) automatically.")

st.code("""
-- Resume the warehouse for the next exercises
ALTER WAREHOUSE TU30_ZERO_TO_SNOWFLAKE_LAB_WH RESUME;
""", language="sql")

st.markdown("---")

st.header("Part B: Zero-Copy Cloning")

st.markdown("""
### What is Zero-Copy Cloning?

Cloning creates a **copy** of a database, schema, or table that:
- Is **instant** (regardless of data size)
- Consumes **no additional storage** (until changes are made)
- Is **fully independent** — changes to the clone don't affect the original

### How Does It Work?

Snowflake stores data in immutable **micro-partitions**. When you clone a table, Snowflake 
doesn't copy any data — it creates a new metadata pointer to the **same underlying micro-partitions**.

```
┌──────────────┐         ┌──────────────────────────┐
│  CUSTOMERS   │────────▶│  Micro-partitions (data) │
└──────────────┘         └──────────────────────────┘
                                     ▲
┌──────────────────┐                 │
│  CUSTOMERS_CLONE │─────────────────┘  (same data, no copy)
└──────────────────┘
```

- **At clone time:** Both tables point to the same partitions → **zero additional storage cost**
- **When you modify the clone:** Only the *changed* micro-partitions are written as new data. You pay for storage of those changed partitions only — not the entire cloned table.
- **Result:** A 10 TB table clones in seconds. If you modify 1 GB of data in the clone, you only pay for 1 GB of additional storage.

This is incredibly powerful for:
- Development & testing (full production copy, no storage bill)
- Experimentation without risk
- Point-in-time snapshots for auditing
""")

st.markdown("### Exercise: Clone and Modify")

st.markdown("**Step 1:** Clone the CUSTOMERS table within your own schema:")

st.code("""
CREATE TABLE CUSTOMERS_CLONE CLONE CUSTOMERS;
""", language="sql")

st.markdown("**Step 2:** Verify the clone has the same data:")

st.code("""
SELECT COUNT(*) FROM CUSTOMERS_CLONE;
-- Should return 500
""", language="sql")

st.markdown("**Step 3:** Make a change in the clone (delete some rows):")

st.code("""
DELETE FROM CUSTOMERS_CLONE
WHERE PROVINCE = 'Alberta';

-- Check the count
SELECT COUNT(*) FROM CUSTOMERS_CLONE;
""", language="sql")

st.markdown("**Step 4:** Confirm the original is **unaffected**:")

st.code("""
SELECT COUNT(*) FROM CUSTOMERS;
-- Still 500!
""", language="sql")

st.success("The original data is completely untouched. This is the power of zero-copy cloning.")

st.markdown("**Step 5:** Clean up — drop the clone:")

st.code("""
DROP TABLE CUSTOMERS_CLONE;
""", language="sql")

st.markdown("---")

with st.expander("🤖 :blue[CoCo Sneak Peek] — Do this with Cortex Code"):
    st.markdown("""
CoCo can help you explore caching and cloning conversationally:

| What you did | CoCo prompt |
|-------------|-------------|
| Run a query twice | `Run this query and tell me the execution time, then run it again` |
| Test metadata cache | `Suspend TU30_ZERO_TO_SNOWFLAKE_LAB_WH, then get the row count of CUSTOMERS` |
| Clone a table | `Create a clone of CUSTOMERS called CUSTOMERS_CLONE` |
| Modify the clone | `Delete all Alberta customers from CUSTOMERS_CLONE` |
| Verify isolation | `Compare customer counts between CUSTOMERS and CUSTOMERS_CLONE` |
| Clean up | `Drop the CUSTOMERS_CLONE table` |

CoCo can also explain **why** queries are fast: `Why did my last query run in 0ms?`
""")

st.markdown("---")

st.success("""
## ✅ Section Complete!

You've learned:
- Snowflake's 3-layer caching automatically accelerates repeated queries
- The results cache saves compute costs on identical queries
- Zero-copy cloning creates instant, independent copies of data
- Clones are perfect for safe experimentation

**Next →** Head to **Section 4: Time Travel & UNDROP** to see how Snowflake protects your data.
""")
