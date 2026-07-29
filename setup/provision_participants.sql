/*
=============================================================================
  ZERO TO SNOWFLAKE HOL — PARTICIPANT ENVIRONMENT SETUP
  Run as: ACCOUNTADMIN
  
  This script creates:
    - A dedicated database (TU30_ZERO_TO_SNOWFLAKE_LAB)
    - A shared warehouse (COMPUTE_WH)
    - 30 roles (TU30_ZERO_TO_SNOWFLAKE_LAB_USER_01 .. TU30_ZERO_TO_SNOWFLAKE_LAB_USER_30) granted to PUBLIC
    - 30 schemas cloned from RETAIL_BANKING (RETAIL_BANKING_01 .. _30)
    - All necessary grants for every exercise in the HOL
    
  Roles are granted to PUBLIC so participants self-select their seat number.
  No admin assignment needed at check-in.
  
  Run this ONCE before the lab starts in each sandbox (AWS / AZ).
=============================================================================
*/

-- ============================================================
-- CONFIGURATION
-- ============================================================
SET DB_NAME       = 'TU30_ZERO_TO_SNOWFLAKE_LAB';
SET SOURCE_DB     = 'TU30_CORTEX_ANALYST_LAB';
SET SOURCE_SCHEMA = 'RETAIL_BANKING';
SET WAREHOUSE     = 'COMPUTE_WH';
SET NUM_USERS     = 30;

USE ROLE ACCOUNTADMIN;

-- ============================================================
-- STEP 1: Create dedicated database and warehouse
-- ============================================================
CREATE DATABASE IF NOT EXISTS IDENTIFIER($DB_NAME);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($WAREHOUSE)
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND   = 60
    AUTO_RESUME    = TRUE
    INITIALLY_SUSPENDED = TRUE;

-- ============================================================
-- STEP 2: Clone source schema into the new database
-- ============================================================
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($DB_NAME || '.' || $SOURCE_SCHEMA)
    CLONE IDENTIFIER($SOURCE_DB || '.' || $SOURCE_SCHEMA);

-- ============================================================
-- STEP 3: Create roles and per-participant schemas
-- ============================================================

BEGIN
    LET i INTEGER := 1;
    LET role_name VARCHAR;
    LET schema_name VARCHAR;
    
    FOR i IN 1 TO $NUM_USERS DO
        role_name   := 'TU30_ZERO_TO_SNOWFLAKE_LAB_USER_' || LPAD(i::VARCHAR, 2, '0');
        schema_name := $SOURCE_SCHEMA || '_' || LPAD(i::VARCHAR, 2, '0');
        
        -- Create the role
        EXECUTE IMMEDIATE 'CREATE ROLE IF NOT EXISTS ' || role_name;
        
        -- Grant role to SYSADMIN (admin management)
        EXECUTE IMMEDIATE 'GRANT ROLE ' || role_name || ' TO ROLE SYSADMIN';
        
        -- Grant role to PUBLIC (self-service: participants pick their seat number)
        EXECUTE IMMEDIATE 'GRANT ROLE ' || role_name || ' TO ROLE PUBLIC';
        
        -- Clone the schema (instant, zero storage)
        EXECUTE IMMEDIATE 'CREATE SCHEMA IF NOT EXISTS ' || $DB_NAME || '.' || schema_name || ' CLONE ' || $DB_NAME || '.' || $SOURCE_SCHEMA;
        
        -- ============================================================
        -- GRANT: Database level
        -- ============================================================
        EXECUTE IMMEDIATE 'GRANT USAGE ON DATABASE ' || $DB_NAME || ' TO ROLE ' || role_name;
        
        -- CREATE SCHEMA needed for Section 3 (clone exercise)
        EXECUTE IMMEDIATE 'GRANT CREATE SCHEMA ON DATABASE ' || $DB_NAME || ' TO ROLE ' || role_name;
        
        -- ============================================================
        -- GRANT: Schema ownership (their isolated workspace)
        -- Covers: CREATE/DROP TABLE, DYNAMIC TABLE, VIEW, MASKING POLICY,
        --         ROW ACCESS POLICY, STREAMLIT, ALTER TABLE, UNDROP, etc.
        -- ============================================================
        EXECUTE IMMEDIATE 'GRANT OWNERSHIP ON SCHEMA ' || $DB_NAME || '.' || schema_name || ' TO ROLE ' || role_name || ' REVOKE CURRENT GRANTS';
        EXECUTE IMMEDIATE 'GRANT OWNERSHIP ON ALL TABLES IN SCHEMA ' || $DB_NAME || '.' || schema_name || ' TO ROLE ' || role_name || ' REVOKE CURRENT GRANTS';
        
        -- ============================================================
        -- GRANT: Warehouse (USAGE = queries, OPERATE = suspend/resume)
        -- ============================================================
        EXECUTE IMMEDIATE 'GRANT USAGE, OPERATE ON WAREHOUSE ' || $WAREHOUSE || ' TO ROLE ' || role_name;
        
        -- ============================================================
        -- GRANT: Source schema (read-only reference)
        -- ============================================================
        EXECUTE IMMEDIATE 'GRANT USAGE ON SCHEMA ' || $DB_NAME || '.' || $SOURCE_SCHEMA || ' TO ROLE ' || role_name;
        EXECUTE IMMEDIATE 'GRANT SELECT ON ALL TABLES IN SCHEMA ' || $DB_NAME || '.' || $SOURCE_SCHEMA || ' TO ROLE ' || role_name;
        
    END FOR;
END;

-- ============================================================
-- STEP 4: Marketplace data (subscribe BEFORE the lab)
-- ============================================================
-- 1. Go to Data Products → Marketplace
-- 2. Search for "Snowflake Public Data (Free)"
-- 3. Click "Get"
-- 4. In the dialog, under "Grant access to", select PUBLIC
-- 5. Click "Get"
--
-- This grants IMPORTED PRIVILEGES to all users automatically.
-- No additional SQL needed.
-- ============================================================

-- ============================================================
-- VERIFICATION
-- ============================================================
SHOW ROLES LIKE 'TU30_ZERO_TO_SNOWFLAKE_LAB_USER_%';
SHOW SCHEMAS IN DATABASE TU30_ZERO_TO_SNOWFLAKE_LAB STARTS WITH 'RETAIL_BANKING_';
SELECT COUNT(*) AS schema_count FROM INFORMATION_SCHEMA.SCHEMATA 
WHERE CATALOG_NAME = 'TU30_ZERO_TO_SNOWFLAKE_LAB' AND SCHEMA_NAME LIKE 'RETAIL_BANKING_%';

-- ============================================================
-- GRANTS SUMMARY PER ROLE (TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX)
-- ============================================================
--
-- ROLE ACCESSIBILITY:
--   ✅ Granted to PUBLIC — participants USE ROLE TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX (seat number)
--
-- DATABASE (TU30_ZERO_TO_SNOWFLAKE_LAB):
--   ✅ USAGE
--   ✅ CREATE SCHEMA (for clone exercise in Section 3)
--
-- THEIR SCHEMA (RETAIL_BANKING_XX):
--   ✅ OWNERSHIP — full control of all objects:
--      • SELECT, INSERT, UPDATE, DELETE on tables
--      • CREATE/DROP TABLE, VIEW, DYNAMIC TABLE
--      • CREATE/DROP MASKING POLICY, ROW ACCESS POLICY
--      • CREATE STREAMLIT
--      • ALTER TABLE (apply/remove policies)
--      • DROP TABLE + UNDROP TABLE (Time Travel)
--
-- SOURCE SCHEMA (RETAIL_BANKING):
--   ✅ USAGE + SELECT (read-only reference)
--
-- WAREHOUSE (COMPUTE_WH):
--   ✅ USAGE (run queries)
--   ✅ OPERATE (suspend/resume for cache exercise)
--
-- MARKETPLACE DB (after subscription):
--   ✅ IMPORTED PRIVILEGES (query shared data)
--
-- ============================================================


-- ============================================================
-- TEARDOWN (run AFTER the lab to clean up everything)
-- ============================================================
/*
USE ROLE ACCOUNTADMIN;

-- Drop the entire HOL database (removes all 30 schemas + source)
DROP DATABASE IF EXISTS TU30_ZERO_TO_SNOWFLAKE_LAB;
DROP WAREHOUSE IF EXISTS COMPUTE_WH;

-- Drop all roles
BEGIN
    LET i INTEGER := 1;
    LET role_name VARCHAR;
    
    FOR i IN 1 TO 30 DO
        role_name := 'TU30_ZERO_TO_SNOWFLAKE_LAB_USER_' || LPAD(i::VARCHAR, 2, '0');
        EXECUTE IMMEDIATE 'DROP ROLE IF EXISTS ' || role_name;
    END FOR;
END;
*/
