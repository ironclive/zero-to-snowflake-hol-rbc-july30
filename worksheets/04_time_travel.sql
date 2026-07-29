/*
=============================================================================
  SECTION 4: TIME TRAVEL & UNDROP
  Zero to Snowflake HOL — July 30, 2026
=============================================================================
*/

-- ============================================================
-- PART B: Querying Historical Data
-- ============================================================

-- Exercise 4.1: Check current row count
SELECT COUNT(*) AS current_count FROM CUSTOMERS;

-- Exercise 4.2: Delete some rows
DELETE FROM CUSTOMERS
WHERE CUSTOMER_SEGMENT = 'Basic';

-- Confirm the delete
SELECT COUNT(*) AS after_delete FROM CUSTOMERS;

-- Exercise 4.3: Query the table BEFORE the delete
-- (Query the table as it was 5 minutes ago)
SELECT COUNT(*) AS before_delete
FROM CUSTOMERS AT(OFFSET => -60*5);

-- Exercise 4.4: Restore the deleted data
INSERT INTO CUSTOMERS
SELECT * FROM CUSTOMERS AT(OFFSET => -60*5)
WHERE CUSTOMER_SEGMENT = 'Basic';

-- Verify restoration
SELECT COUNT(*) AS restored_count FROM CUSTOMERS;

-- ============================================================
-- PART C: UNDROP a Table
-- ============================================================

-- Exercise 4.5: Accidentally drop a table
CREATE TABLE CUSTOMERS_BACKUP CLONE CUSTOMERS;

-- Oops! Drop the backup
DROP TABLE CUSTOMERS_BACKUP;

-- Verify it's gone
SHOW TABLES LIKE 'CUSTOMERS_BACKUP';

-- Exercise 4.6: Recover with UNDROP
UNDROP TABLE CUSTOMERS_BACKUP;

-- Verify it's back
SELECT COUNT(*) FROM CUSTOMERS_BACKUP;

-- Exercise 4.7: Clean up
DROP TABLE CUSTOMERS_BACKUP;
