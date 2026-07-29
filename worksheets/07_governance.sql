/*
=============================================================================
  SECTION 7: GOVERNANCE WITH HORIZON
  Zero to Snowflake HOL — July 30, 2026

  NOTE: Replace XX with your participant number (e.g., 05)
=============================================================================
*/

-- ============================================================
-- PART B: Column-Level Masking
-- ============================================================

-- Exercise 7.1: View sensitive data (before masking)
SELECT
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    EMAIL,
    ANNUAL_INCOME
FROM CUSTOMERS
LIMIT 10;

-- Exercise 7.2: Create a masking policy for email
-- ⚠️ Replace XX with your participant number!
CREATE OR REPLACE MASKING POLICY EMAIL_MASK AS (val STRING)
RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() = 'TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX'
            THEN val
        ELSE REGEXP_REPLACE(val, '.+@', '****@')
    END;

-- Exercise 7.3: Apply the masking policy
ALTER TABLE CUSTOMERS
    MODIFY COLUMN EMAIL
    SET MASKING POLICY EMAIL_MASK;

-- Exercise 7.4: Create and apply a masking policy for income
-- ⚠️ Replace XX with your participant number!
CREATE OR REPLACE MASKING POLICY INCOME_MASK AS (val NUMBER)
RETURNS NUMBER ->
    CASE
        WHEN CURRENT_ROLE() = 'TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX'
            THEN val
        ELSE NULL
    END;

ALTER TABLE CUSTOMERS
    MODIFY COLUMN ANNUAL_INCOME
    SET MASKING POLICY INCOME_MASK;

-- Exercise 7.5: Test — query YOUR schema (you see unmasked data)
SELECT CUSTOMER_ID, EMAIL, ANNUAL_INCOME
FROM CUSTOMERS LIMIT 5;

-- Exercise 7.6: Test — query ANOTHER participant's schema (you see masked data!)
-- ⚠️ Pick a neighbor's schema number (e.g., RETAIL_BANKING_01)
SELECT CUSTOMER_ID, EMAIL, ANNUAL_INCOME
FROM TU30_ZERO_TO_SNOWFLAKE_LAB.RETAIL_BANKING_01.CUSTOMERS
LIMIT 5;

-- ============================================================
-- PART C: Row Access Policies
-- ============================================================

-- Exercise 7.7: Create a row access policy
-- ⚠️ Replace XX with your participant number!
CREATE OR REPLACE ROW ACCESS POLICY PROVINCE_ACCESS AS (province_val VARCHAR)
RETURNS BOOLEAN ->
    CASE
        WHEN CURRENT_ROLE() = 'TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX'
            THEN TRUE
        ELSE province_val = 'Ontario'
    END;

-- Exercise 7.8: Apply the row access policy
ALTER TABLE CUSTOMERS
    ADD ROW ACCESS POLICY PROVINCE_ACCESS ON (PROVINCE);

-- Exercise 7.9: Test — query YOUR schema (all provinces visible)
SELECT PROVINCE, COUNT(*) AS customer_count
FROM CUSTOMERS
GROUP BY PROVINCE
ORDER BY customer_count DESC;

-- Exercise 7.10: Test — query ANOTHER participant's schema (only Ontario)
-- ⚠️ Pick a neighbor's schema number
SELECT PROVINCE, COUNT(*) AS customer_count
FROM TU30_ZERO_TO_SNOWFLAKE_LAB.RETAIL_BANKING_01.CUSTOMERS
GROUP BY PROVINCE
ORDER BY customer_count DESC;

-- ============================================================
-- PART D: Clean up
-- ============================================================

-- Remove policies from your table
ALTER TABLE CUSTOMERS MODIFY COLUMN EMAIL UNSET MASKING POLICY;
ALTER TABLE CUSTOMERS MODIFY COLUMN ANNUAL_INCOME UNSET MASKING POLICY;
ALTER TABLE CUSTOMERS DROP ROW ACCESS POLICY PROVINCE_ACCESS;

-- Drop policy objects
DROP MASKING POLICY IF EXISTS EMAIL_MASK;
DROP MASKING POLICY IF EXISTS INCOME_MASK;
DROP ROW ACCESS POLICY IF EXISTS PROVINCE_ACCESS;
