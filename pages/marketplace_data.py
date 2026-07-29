import streamlit as st

st.title("🏪 Marketplace Data")
st.markdown("**Duration:** ~20 minutes")
st.markdown("---")

st.markdown("""
## What is the Snowflake Marketplace?

Traditionally, getting third-party data into your analytics platform means finding a provider, 
negotiating access, setting up an FTP transfer or API integration, loading it into your warehouse, 
and keeping it refreshed. The **Snowflake Marketplace** eliminates all of that.

**Key concepts for this section:**

| Concept | What it means |
|---------|--------------|
| **Marketplace** | A catalog of 2,000+ data listings from third-party providers, accessible directly inside Snowflake. |
| **Data Sharing** | Marketplace data appears as a shared database in your account — no ETL, no loading, no storage costs. |
| **Live data** | Providers maintain and refresh their data. You always see the latest version automatically. |
| **Free & paid listings** | Many high-value datasets (economic indicators, weather, demographics) are completely free. |
| **No data movement** | The data never leaves Snowflake's infrastructure. You `JOIN` it directly with your internal tables. |

**Why this matters in banking:**
- Enrich customer profiles with demographic or credit bureau data
- Add economic indicators (unemployment, GDP, interest rates) to risk models
- Bring in market data and FX rates for portfolio analytics — no vendor integration needed
- Compliance teams can reference regulatory datasets without separate infrastructure

**In this section**, we'll explore a pre-installed Marketplace listing and join FX rate data with our banking transactions.
""")

st.markdown("---")

st.markdown("""
## Objectives

By the end of this section, you will be able to:
- Navigate the Snowflake Marketplace
- Understand how Marketplace subscriptions work
- Explore shared data without any ETL or data loading
- Join Marketplace data with your banking tables for enriched analytics
""")

st.markdown("---")

st.header("Part A: Browse the Snowflake Marketplace")

st.markdown("""
#### Exercise 6.1 — Navigate to the Marketplace

1. In Snowsight, click **Marketplace → Snowflake Marketplace** in the left nav.
2. You'll see featured and recommended listings.
3. In the search bar, type: **`Snowflake Public Data`**
4. Look for the listing: **"Snowflake Public Data (Free)"** by Snowflake Inc.
5. Click on the listing to view details.
""")

st.info("""
💡 **Note:** This listing has already been subscribed for you. You'll see it marked as 
**"Already Installed"** — the instructor pre-provisioned it so everyone can use it immediately.

In a real scenario, you would click **Get**, accept the terms, and a new shared database 
would appear in your account instantly — no data loading required.
""")

st.markdown("---")

st.header("Part B: Explore the Marketplace Data")

st.markdown("""
The listing created a database called `TU30_SNOWFLAKE_PUBLIC_DATA` with a single schema 
`PUBLIC_DATA_FREE` containing **370 views** across domains like finance, economics, weather, 
demographics, and more.
""")

st.markdown("#### Exercise 6.2 — Discover available data")

st.code("""
-- See the schema structure
SHOW VIEWS IN SCHEMA TU30_SNOWFLAKE_PUBLIC_DATA.PUBLIC_DATA_FREE LIMIT 20;
""", language="sql")

st.code("""
-- Preview FX (foreign exchange) rate data — USD/CAD
SELECT *
FROM TU30_SNOWFLAKE_PUBLIC_DATA.PUBLIC_DATA_FREE.FX_RATES_TIMESERIES
WHERE BASE_CURRENCY_ID = 'USD' AND QUOTE_CURRENCY_ID = 'CAD'
ORDER BY DATE DESC
LIMIT 20;
""", language="sql")

st.success("""
**What happened?** You queried live exchange rate data maintained by the provider — no ETL, 
no pipelines, no storage costs on your end. This data refreshes automatically.
""")

st.markdown("#### Exercise 6.3 — Explore Canadian economic data")

st.code("""
-- Bank of Canada Prime Rate over time
SELECT VARIABLE_NAME, DATE, VALUE, UNIT
FROM TU30_SNOWFLAKE_PUBLIC_DATA.PUBLIC_DATA_FREE.CANADA_STATCAN_TIMESERIES
WHERE VARIABLE_NAME = 'Chartered bank administered interest rates - Prime rate'
ORDER BY DATE DESC
LIMIT 20;
""", language="sql")

st.markdown("---")

st.header("Part C: Enrich Your Banking Data")

st.markdown("""
Now for the powerful part — **join Marketplace data with your banking tables** to create 
enriched analytics without any data movement.

We'll join our `TRANSACTIONS` table with the `FX_RATES_TIMESERIES` view to see what the 
USD/CAD exchange rate was on each transaction date.
""")

st.markdown("#### Exercise 6.4 — Join transactions with FX rates")

st.code("""
-- Enrich transactions with the USD/CAD rate on the transaction date
SELECT
    t.TRANSACTION_ID,
    t.TRANSACTION_DATE,
    t.TRANSACTION_TYPE,
    t.AMOUNT,
    fx.VALUE AS USD_CAD_RATE,
    ROUND(t.AMOUNT * fx.VALUE, 2) AS AMOUNT_USD
FROM TRANSACTIONS t
JOIN TU30_SNOWFLAKE_PUBLIC_DATA.PUBLIC_DATA_FREE.FX_RATES_TIMESERIES fx
    ON t.TRANSACTION_DATE = fx.DATE
    AND fx.BASE_CURRENCY_ID = 'USD'
    AND fx.QUOTE_CURRENCY_ID = 'CAD'
ORDER BY t.TRANSACTION_DATE DESC
LIMIT 20;
""", language="sql")

st.success("""
**What happened?** You joined internal banking data with live Marketplace FX data in a single 
query — no data loading, no API calls, no ETL pipelines. The data lives in Snowflake's shared 
infrastructure and is always current.
""")

st.markdown("#### Exercise 6.5 — Aggregate by month with FX context")

st.code("""
-- Monthly transaction volume with average exchange rate
SELECT
    DATE_TRUNC('MONTH', t.TRANSACTION_DATE) AS MONTH,
    COUNT(*) AS transaction_count,
    SUM(t.AMOUNT) AS total_amount_cad,
    AVG(fx.VALUE) AS avg_usd_cad_rate,
    ROUND(SUM(t.AMOUNT) / AVG(fx.VALUE), 2) AS estimated_amount_usd
FROM TRANSACTIONS t
JOIN TU30_SNOWFLAKE_PUBLIC_DATA.PUBLIC_DATA_FREE.FX_RATES_TIMESERIES fx
    ON t.TRANSACTION_DATE = fx.DATE
    AND fx.BASE_CURRENCY_ID = 'USD'
    AND fx.QUOTE_CURRENCY_ID = 'CAD'
GROUP BY MONTH
ORDER BY MONTH DESC;
""", language="sql")

st.markdown("""
> 💡 **Key Insight:** In production, you would use this pattern to enrich risk models, 
> build multi-currency reporting, or add economic context to customer analytics — all 
> without any data movement or vendor integrations.
""")

st.markdown("---")

with st.expander("🤖 :blue[CoCo Sneak Peek] — Do this with Cortex Code"):
    st.markdown("""
CoCo can help you discover and use Marketplace data:

| What you did | CoCo prompt |
|-------------|-------------|
| Explore listing | `What views are in TU30_SNOWFLAKE_PUBLIC_DATA.PUBLIC_DATA_FREE?` |
| Preview FX data | `Show me the latest USD/CAD exchange rates from the public data listing` |
| Enrich banking data | `Join our transactions with USD/CAD FX rates from the marketplace data` |
| Find relevant data | `What marketplace views have Canadian economic data?` |

CoCo can also help you discover new listings: `Search the Snowflake Marketplace for Canadian economic data`
""")

st.markdown("---")

st.success("""
## ✅ Section Complete!

You've learned:
- The Snowflake Marketplace provides instant access to third-party data
- Subscribing is a click — no ETL, no pipelines, no data loading
- Marketplace data can be joined directly with your internal tables
- This pattern enables enriched analytics (FX rates, economic indicators) without data movement

**Next →** Head to **Section 7: Governance** to secure your data with masking and row access policies.
""")
