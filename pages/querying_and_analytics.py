import streamlit as st

st.title("📊 Querying & Analytics")
st.markdown("**Duration:** ~40 minutes")
st.markdown("---")

st.markdown("""
## SQL in Snowflake — What You Need to Know

Snowflake uses **standard ANSI SQL** — if you've written SQL before, you already know 90% of what 
you need. Queries run in **SQL files** inside Snowsight, and results appear instantly below your code.

**Key concepts for this section:**

| Concept | What it means |
|---------|--------------|
| **SELECT** | Retrieve data from tables — the foundation of everything |
| **JOIN** | Combine rows from multiple tables using a shared key (e.g., `CUSTOMER_ID`) |
| **GROUP BY + Aggregates** | Summarize data: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` |
| **Window Functions** | Compute analytics across rows without collapsing results (e.g., `RANK`, `SUM() OVER`) |
| **Date Functions** | `DATE_TRUNC`, `DAYNAME`, `DATEDIFF` — essential for time-series analysis |

**How it works in Snowflake:**
- Write SQL in a **SQL file** (like a scratch pad)
- Highlight one or more statements and click **▶ Run**
- Results appear below; you can sort columns, download CSV, or chart them directly
- Snowflake compiles and optimizes your query automatically — no indexes or hints needed

**In this section**, we'll write progressively complex queries across our banking dataset.
""")

st.markdown("---")

st.markdown("""
## Objectives

By the end of this section, you will be able to:
- Write SELECT queries with filtering, sorting, and limiting
- Use aggregate functions (COUNT, SUM, AVG) with GROUP BY
- Join multiple tables together
- Use window functions for advanced analytics
- Perform date-based analysis on transaction data
""")

st.markdown("---")

st.header("Exercise 1: Exploring Customers")

st.markdown("""
Let's start by getting familiar with the CUSTOMERS table.

**1a.** View the first 10 customers:
""")

st.code("""
SELECT *
FROM CUSTOMERS
LIMIT 10;
""", language="sql")

st.markdown("**1b.** Find all customers in Ontario with an income above $100,000:")

st.code("""
SELECT FIRST_NAME, LAST_NAME, CITY, ANNUAL_INCOME, CREDIT_SCORE
FROM CUSTOMERS
WHERE PROVINCE = 'Ontario'
  AND ANNUAL_INCOME > 100000
ORDER BY ANNUAL_INCOME DESC;
""", language="sql")

st.markdown("**1c.** Count customers by segment:")

st.code("""
SELECT CUSTOMER_SEGMENT, COUNT(*) AS customer_count
FROM CUSTOMERS
GROUP BY CUSTOMER_SEGMENT
ORDER BY customer_count DESC;
""", language="sql")

st.markdown("---")

st.header("Exercise 2: Exploring Transactions")

st.markdown("""
Now let's dig into the TRANSACTIONS table.

**2a.** What are the transaction types and how frequently do they occur?
""")

st.code("""
SELECT TRANSACTION_TYPE, 
       COUNT(*) AS txn_count,
       SUM(AMOUNT) AS total_amount,
       AVG(AMOUNT) AS avg_amount
FROM TRANSACTIONS
GROUP BY TRANSACTION_TYPE
ORDER BY total_amount DESC;
""", language="sql")

st.markdown("**2b.** What are the top 5 highest-value transactions?")

st.code("""
SELECT T.TRANSACTION_ID, 
       T.TRANSACTION_DATE, 
       T.AMOUNT, 
       T.TRANSACTION_TYPE,
       C.FIRST_NAME || ' ' || C.LAST_NAME AS CUSTOMER_NAME
FROM TRANSACTIONS T
JOIN CUSTOMERS C ON T.CUSTOMER_ID = C.CUSTOMER_ID
ORDER BY T.AMOUNT DESC
LIMIT 5;
""", language="sql")

st.markdown("---")

st.header("Exercise 3: Joining All Three Tables")

st.markdown("""
Let's bring all three tables together for real analytics.

**3a.** Revenue by product category — which products generate the most transaction volume?
""")

st.code("""
SELECT P.PRODUCT_CATEGORY,
       P.PRODUCT_NAME,
       COUNT(T.TRANSACTION_ID) AS txn_count,
       SUM(T.AMOUNT) AS total_volume,
       AVG(T.AMOUNT) AS avg_transaction
FROM TRANSACTIONS T
JOIN PRODUCTS P ON T.PRODUCT_ID = P.PRODUCT_ID
GROUP BY P.PRODUCT_CATEGORY, P.PRODUCT_NAME
ORDER BY total_volume DESC;
""", language="sql")

st.markdown("**3b.** Average transaction value by customer segment and product category:")

st.code("""
SELECT C.CUSTOMER_SEGMENT,
       P.PRODUCT_CATEGORY,
       COUNT(T.TRANSACTION_ID) AS txn_count,
       ROUND(AVG(T.AMOUNT), 2) AS avg_amount,
       ROUND(SUM(T.AMOUNT), 2) AS total_amount
FROM TRANSACTIONS T
JOIN CUSTOMERS C ON T.CUSTOMER_ID = C.CUSTOMER_ID
JOIN PRODUCTS P ON T.PRODUCT_ID = P.PRODUCT_ID
GROUP BY C.CUSTOMER_SEGMENT, P.PRODUCT_CATEGORY
ORDER BY C.CUSTOMER_SEGMENT, total_amount DESC;
""", language="sql")

st.markdown("---")

st.header("Exercise 4: Window Functions")

st.markdown("""
Window functions let you compute analytics across rows without collapsing results.

**4a.** Rank customers by total spend:
""")

st.code("""
SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS CUSTOMER_NAME,
       C.CUSTOMER_SEGMENT,
       SUM(T.AMOUNT) AS total_spend,
       RANK() OVER (ORDER BY SUM(T.AMOUNT) DESC) AS spend_rank
FROM TRANSACTIONS T
JOIN CUSTOMERS C ON T.CUSTOMER_ID = C.CUSTOMER_ID
WHERE T.TRANSACTION_TYPE = 'Purchase'
GROUP BY C.CUSTOMER_ID, C.FIRST_NAME, C.LAST_NAME, C.CUSTOMER_SEGMENT
ORDER BY spend_rank
LIMIT 20;
""", language="sql")

st.markdown("**4b.** Running total of transactions by date:")

st.code("""
SELECT TRANSACTION_DATE,
       COUNT(*) AS daily_txns,
       SUM(AMOUNT) AS daily_volume,
       SUM(SUM(AMOUNT)) OVER (ORDER BY TRANSACTION_DATE) AS running_total
FROM TRANSACTIONS
GROUP BY TRANSACTION_DATE
ORDER BY TRANSACTION_DATE;
""", language="sql")

st.markdown("---")

st.header("Exercise 5: Date-Based Analytics")

st.markdown("""
Time-series analysis is critical in banking. Let's look at trends.

**5a.** Monthly transaction summary:
""")

st.code("""
SELECT DATE_TRUNC('MONTH', TRANSACTION_DATE) AS month,
       COUNT(*) AS txn_count,
       SUM(AMOUNT) AS total_volume,
       COUNT(DISTINCT CUSTOMER_ID) AS active_customers
FROM TRANSACTIONS
GROUP BY month
ORDER BY month;
""", language="sql")

st.markdown("**5b.** Which day of the week sees the most transactions?")

st.code("""
SELECT DAYNAME(TRANSACTION_DATE) AS day_of_week,
       DAYOFWEEK(TRANSACTION_DATE) AS day_num,
       COUNT(*) AS txn_count,
       SUM(AMOUNT) AS total_volume
FROM TRANSACTIONS
GROUP BY day_of_week, day_num
ORDER BY day_num;
""", language="sql")

st.markdown("**5c.** Channel analysis — how do customers transact?")

st.code("""
SELECT CHANNEL,
       COUNT(*) AS txn_count,
       ROUND(AVG(AMOUNT), 2) AS avg_amount,
       ROUND(SUM(AMOUNT), 2) AS total_volume
FROM TRANSACTIONS
GROUP BY CHANNEL
ORDER BY total_volume DESC;
""", language="sql")

st.markdown("---")

with st.expander("🤖 :blue[CoCo Sneak Peek] — Do this with Cortex Code"):
    st.markdown("""
Instead of writing SQL by hand, you could ask **Cortex Code (CoCo)** in natural language:

| What you did | CoCo prompt |
|-------------|-------------|
| Filter customers | `Show me all customers in Ontario with annual income above 100K` |
| Aggregate transactions | `What are the transaction types and their total amounts?` |
| Join tables | `Show revenue by product category with transaction counts` |
| Window functions | `Rank customers by total purchase spend` |
| Time-series | `Give me a monthly transaction summary with active customer counts` |
| Day-of-week analysis | `Which day of the week has the most transactions?` |

CoCo generates and runs the SQL for you — you can review, modify, and re-run.
""")

st.success("""
## ✅ Section Complete!

You've written queries that:
- Filter and sort customer data
- Aggregate transaction volumes by type, product, and segment
- Join all three tables for cross-dimensional analysis
- Use window functions for rankings and running totals
- Analyze time-based trends

**Next →** Head to **Section 3: Results Cache & Cloning** to see Snowflake's performance magic.
""")
