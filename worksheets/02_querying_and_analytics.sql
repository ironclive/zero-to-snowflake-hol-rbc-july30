/*
=============================================================================
  SECTION 2: QUERYING & ANALYTICS
  Zero to Snowflake HOL — July 30, 2026
=============================================================================
*/

-- ============================================================
-- EXERCISE 1: Exploring Customers
-- ============================================================

-- 1a. View the first 10 customers
SELECT *
FROM CUSTOMERS
LIMIT 10;

-- 1b. Find all customers in Ontario with income above $100,000
SELECT FIRST_NAME, LAST_NAME, CITY, ANNUAL_INCOME, CREDIT_SCORE
FROM CUSTOMERS
WHERE PROVINCE = 'Ontario'
  AND ANNUAL_INCOME > 100000
ORDER BY ANNUAL_INCOME DESC;

-- 1c. Count customers by segment
SELECT CUSTOMER_SEGMENT, COUNT(*) AS customer_count
FROM CUSTOMERS
GROUP BY CUSTOMER_SEGMENT
ORDER BY customer_count DESC;

-- ============================================================
-- EXERCISE 2: Exploring Transactions
-- ============================================================

-- 2a. Transaction types and frequency
SELECT TRANSACTION_TYPE, 
       COUNT(*) AS txn_count,
       SUM(AMOUNT) AS total_amount,
       AVG(AMOUNT) AS avg_amount
FROM TRANSACTIONS
GROUP BY TRANSACTION_TYPE
ORDER BY total_amount DESC;

-- 2b. Top 5 highest-value transactions
SELECT T.TRANSACTION_ID, 
       T.TRANSACTION_DATE, 
       T.AMOUNT, 
       T.TRANSACTION_TYPE,
       C.FIRST_NAME || ' ' || C.LAST_NAME AS CUSTOMER_NAME
FROM TRANSACTIONS T
JOIN CUSTOMERS C ON T.CUSTOMER_ID = C.CUSTOMER_ID
ORDER BY T.AMOUNT DESC
LIMIT 5;

-- ============================================================
-- EXERCISE 3: Joining All Three Tables
-- ============================================================

-- 3a. Revenue by product category
SELECT P.PRODUCT_CATEGORY,
       P.PRODUCT_NAME,
       COUNT(T.TRANSACTION_ID) AS txn_count,
       SUM(T.AMOUNT) AS total_volume,
       AVG(T.AMOUNT) AS avg_transaction
FROM TRANSACTIONS T
JOIN PRODUCTS P ON T.PRODUCT_ID = P.PRODUCT_ID
GROUP BY P.PRODUCT_CATEGORY, P.PRODUCT_NAME
ORDER BY total_volume DESC;

-- 3b. Average transaction value by segment and product category
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

-- ============================================================
-- EXERCISE 4: Window Functions
-- ============================================================

-- 4a. Rank customers by total spend
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

-- 4b. Running total of transactions by date
SELECT TRANSACTION_DATE,
       COUNT(*) AS daily_txns,
       SUM(AMOUNT) AS daily_volume,
       SUM(SUM(AMOUNT)) OVER (ORDER BY TRANSACTION_DATE) AS running_total
FROM TRANSACTIONS
GROUP BY TRANSACTION_DATE
ORDER BY TRANSACTION_DATE;

-- ============================================================
-- EXERCISE 5: Date-Based Analytics
-- ============================================================

-- 5a. Monthly transaction summary
SELECT DATE_TRUNC('MONTH', TRANSACTION_DATE) AS month,
       COUNT(*) AS txn_count,
       SUM(AMOUNT) AS total_volume,
       COUNT(DISTINCT CUSTOMER_ID) AS active_customers
FROM TRANSACTIONS
GROUP BY month
ORDER BY month;

-- 5b. Which day of the week sees the most transactions?
SELECT DAYNAME(TRANSACTION_DATE) AS day_of_week,
       DAYOFWEEK(TRANSACTION_DATE) AS day_num,
       COUNT(*) AS txn_count,
       SUM(AMOUNT) AS total_volume
FROM TRANSACTIONS
GROUP BY day_of_week, day_num
ORDER BY day_num;

-- 5c. Channel analysis
SELECT CHANNEL,
       COUNT(*) AS txn_count,
       ROUND(AVG(AMOUNT), 2) AS avg_amount,
       ROUND(SUM(AMOUNT), 2) AS total_volume
FROM TRANSACTIONS
GROUP BY CHANNEL
ORDER BY total_volume DESC;
