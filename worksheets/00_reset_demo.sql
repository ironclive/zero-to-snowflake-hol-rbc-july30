/*
=============================================================================
  RESET DEMO ENVIRONMENT
  Run as: SYSADMIN (instructor's demo account)
  
  Run this BEFORE each demo to ensure a clean starting state.
=============================================================================
*/

USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TU30_ZERO_TO_SNOWFLAKE_LAB;
USE SCHEMA RETAIL_BANKING;

-- ============================================================
-- Section 3: Remove any clone tables
-- ============================================================
DROP TABLE IF EXISTS CUSTOMERS_CLONE;

-- ============================================================
-- Section 5: Drop dynamic tables (gold first, then silver)
-- ============================================================
DROP DYNAMIC TABLE IF EXISTS PRODUCT_PERFORMANCE;
DROP DYNAMIC TABLE IF EXISTS TRANSACTION_ENRICHED;

-- Section 5: Remove test transactions
DELETE FROM TRANSACTIONS WHERE AMOUNT = 5000.00;

-- ============================================================
-- Section 7: Unset policies before dropping them
-- ============================================================
ALTER TABLE CUSTOMERS MODIFY COLUMN EMAIL UNSET MASKING POLICY;
ALTER TABLE CUSTOMERS MODIFY COLUMN ANNUAL_INCOME UNSET MASKING POLICY;
ALTER TABLE CUSTOMERS DROP ROW ACCESS POLICY PROVINCE_ACCESS;

-- Section 7: Drop policies
DROP MASKING POLICY IF EXISTS EMAIL_MASK;
DROP MASKING POLICY IF EXISTS INCOME_MASK;
DROP ROW ACCESS POLICY IF EXISTS PROVINCE_ACCESS;

-- ============================================================
-- Section 8: Drop Streamlit app (if deployed)
-- ============================================================
DROP STREAMLIT IF EXISTS BANKING_DASHBOARD;

-- ============================================================
-- VERIFY CLEAN STATE
-- ============================================================
SELECT 'CUSTOMERS' AS tbl, COUNT(*) AS cnt FROM CUSTOMERS
UNION ALL
SELECT 'PRODUCTS', COUNT(*) FROM PRODUCTS
UNION ALL
SELECT 'TRANSACTIONS', COUNT(*) FROM TRANSACTIONS;
-- Expected: CUSTOMERS=500, PRODUCTS=15, TRANSACTIONS=1000
