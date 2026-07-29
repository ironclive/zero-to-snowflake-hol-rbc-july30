/*
=============================================================================
  SECTION 6: MARKETPLACE DATA
  Zero to Snowflake HOL — July 30, 2026
  
  NOTE: The Marketplace subscription has been pre-provisioned.
  Browse the listing at Marketplace → Snowflake Marketplace, then run these queries.
=============================================================================
*/

-- ============================================================
-- PART B: Explore the Marketplace Data
-- ============================================================

-- Exercise 6.2: Discover available data
SHOW VIEWS IN SCHEMA TU30_SNOWFLAKE_PUBLIC_DATA.PUBLIC_DATA_FREE LIMIT 20;

-- Preview FX (foreign exchange) rate data — USD/CAD
SELECT *
FROM TU30_SNOWFLAKE_PUBLIC_DATA.PUBLIC_DATA_FREE.FX_RATES_TIMESERIES
WHERE BASE_CURRENCY_ID = 'USD' AND QUOTE_CURRENCY_ID = 'CAD'
ORDER BY DATE DESC
LIMIT 20;

-- Exercise 6.3: Explore Canadian economic data
SELECT VARIABLE_NAME, DATE, VALUE, UNIT
FROM TU30_SNOWFLAKE_PUBLIC_DATA.PUBLIC_DATA_FREE.CANADA_STATCAN_TIMESERIES
WHERE VARIABLE_NAME = 'Chartered bank administered interest rates - Prime rate'
ORDER BY DATE DESC
LIMIT 20;

-- ============================================================
-- PART C: Enrich Your Banking Data
-- ============================================================

-- Exercise 6.4: Join transactions with FX rates
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

-- Exercise 6.5: Monthly transaction volume with average exchange rate
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
