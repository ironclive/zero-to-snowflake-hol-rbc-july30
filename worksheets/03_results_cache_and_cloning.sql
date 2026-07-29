/*
=============================================================================
  SECTION 3: RESULTS CACHE & CLONING
  Zero to Snowflake HOL — July 30, 2026
=============================================================================
*/

-- ============================================================
-- PART A: Results Cache
-- ============================================================

-- Step 1: Run this query and note the execution time
SELECT C.CUSTOMER_SEGMENT,
       COUNT(DISTINCT T.CUSTOMER_ID) AS active_customers,
       SUM(T.AMOUNT) AS total_volume
FROM TRANSACTIONS T
JOIN CUSTOMERS C ON T.CUSTOMER_ID = C.CUSTOMER_ID
GROUP BY C.CUSTOMER_SEGMENT
ORDER BY total_volume DESC;

-- Step 2: Run the EXACT same query again — observe the speed difference
SELECT C.CUSTOMER_SEGMENT,
       COUNT(DISTINCT T.CUSTOMER_ID) AS active_customers,
       SUM(T.AMOUNT) AS total_volume
FROM TRANSACTIONS T
JOIN CUSTOMERS C ON T.CUSTOMER_ID = C.CUSTOMER_ID
GROUP BY C.CUSTOMER_SEGMENT
ORDER BY total_volume DESC;

-- Step 3: Modify slightly (change ORDER BY) — cache NOT reused
SELECT C.CUSTOMER_SEGMENT,
       COUNT(DISTINCT T.CUSTOMER_ID) AS active_customers,
       SUM(T.AMOUNT) AS total_volume
FROM TRANSACTIONS T
JOIN CUSTOMERS C ON T.CUSTOMER_ID = C.CUSTOMER_ID
GROUP BY C.CUSTOMER_SEGMENT
ORDER BY active_customers DESC;  -- Changed!

-- ============================================================
-- Metadata Cache — works even with warehouse suspended
-- ============================================================

-- Suspend the warehouse
ALTER WAREHOUSE COMPUTE_WH SUSPEND;

-- These still work (metadata cache)!
SELECT COUNT(*) FROM CUSTOMERS;
SELECT MIN(TRANSACTION_DATE) FROM TRANSACTIONS;
SELECT MAX(AMOUNT) FROM TRANSACTIONS;

-- Resume the warehouse for the next exercises
ALTER WAREHOUSE COMPUTE_WH RESUME;

-- ============================================================
-- PART B: Zero-Copy Cloning
-- ============================================================

-- Step 1: Clone the CUSTOMERS table within your own schema
CREATE TABLE CUSTOMERS_CLONE CLONE CUSTOMERS;

-- Step 2: Verify the clone has the same data
SELECT COUNT(*) FROM CUSTOMERS_CLONE;
-- Should return 500

-- Step 3: Make a change in the clone (delete some rows)
DELETE FROM CUSTOMERS_CLONE
WHERE PROVINCE = 'Alberta';

-- Check the count
SELECT COUNT(*) FROM CUSTOMERS_CLONE;

-- Step 4: Confirm the original is UNAFFECTED
SELECT COUNT(*) FROM CUSTOMERS;
-- Still 500!

-- Step 5: Clean up — drop the clone
DROP TABLE CUSTOMERS_CLONE;
