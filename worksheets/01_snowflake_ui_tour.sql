/*
=============================================================================
  SECTION 1: SNOWFLAKE UI TOUR
  Zero to Snowflake HOL — July 30, 2026
=============================================================================
*/

-- ============================================================
-- STEP 4: Set Your Context
-- Replace XX with your assigned seat number (e.g., 03, 14, 23)
-- ============================================================

USE ROLE TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TU30_ZERO_TO_SNOWFLAKE_LAB;
USE SCHEMA RETAIL_BANKING_XX;

-- ============================================================
-- STEP 6: Quick Preview — Confirm your data is ready
-- ============================================================

-- How many customers?
SELECT COUNT(*) AS customer_count FROM CUSTOMERS;

-- How many products?
SELECT COUNT(*) AS product_count FROM PRODUCTS;

-- How many transactions?
SELECT COUNT(*) AS transaction_count FROM TRANSACTIONS;

-- Expected: Customers = 500, Products = 15, Transactions = 1,000
