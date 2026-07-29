/*
=============================================================================
  SECTION 5: DYNAMIC TABLES (Medallion Architecture)
  Zero to Snowflake HOL — July 30, 2026
=============================================================================
*/

-- ============================================================
-- SILVER LAYER: Enrich transactions
-- Joins all 3 bronze tables into a single enriched view
-- ============================================================

-- Exercise 5.2: Create the Silver layer Dynamic Table
CREATE OR REPLACE DYNAMIC TABLE TRANSACTION_ENRICHED
    TARGET_LAG = '1 minute'
    WAREHOUSE = COMPUTE_WH
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

-- Exercise 5.3: Query the Silver layer
SELECT * FROM TRANSACTION_ENRICHED
LIMIT 20;

-- ============================================================
-- GOLD LAYER: Business KPIs
-- Aggregates from Silver into dashboard-ready metrics
-- ============================================================

-- Exercise 5.4: Create the Gold layer Dynamic Table
CREATE OR REPLACE DYNAMIC TABLE PRODUCT_PERFORMANCE
    TARGET_LAG = '2 minutes'
    WAREHOUSE = COMPUTE_WH
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

-- Exercise 5.5: Query the Gold layer
SELECT * FROM PRODUCT_PERFORMANCE
ORDER BY revenue_rank;

-- ============================================================
-- SIMULATE A DATA CHANGE
-- Insert 3 x $5,000 deposits into Bronze, then verify they
-- flow automatically into Silver (enriched) and Gold (aggregated)
-- ============================================================

-- Exercise 5.6: Insert 3 new transactions into Bronze
-- This inserts 3 rows of $5,000 each (= $15,000 total new revenue)
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
-- Expected result: "3 rows inserted"

-- Exercise 5.7: Verify the 3 transactions appear in Silver
-- Wait ~1 minute (TARGET_LAG = '1 minute'), then run:
SELECT * FROM TRANSACTION_ENRICHED
WHERE AMOUNT = 5000.00 AND TRANSACTION_DATE = CURRENT_DATE();
-- Expected: 3 rows — your deposits now enriched with customer & product details

-- Exercise 5.8: Verify the $15,000 shows up in Gold
-- Wait ~2 more minutes (TARGET_LAG = '2 minutes'), then run:
SELECT * FROM PRODUCT_PERFORMANCE
ORDER BY revenue_rank;
-- Look for "Essential Chequing": total_transactions +3, total_revenue +$15,000

-- ============================================================
-- CLEAN UP
-- ============================================================

DROP DYNAMIC TABLE IF EXISTS PRODUCT_PERFORMANCE;
DROP DYNAMIC TABLE IF EXISTS TRANSACTION_ENRICHED;

-- Remove the test transactions
DELETE FROM TRANSACTIONS WHERE AMOUNT = 5000.00 AND TRANSACTION_DATE = CURRENT_DATE();
