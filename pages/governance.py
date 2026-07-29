import streamlit as st

st.title("🛡️ Governance with Horizon")

st.markdown("**Duration:** ~20 minutes")

st.markdown("---")

st.markdown("""
## What is Data Governance in Snowflake?

Data governance is about controlling **who can see what data** — without building separate databases 
for every team or hardcoding restrictions into every application. Snowflake's governance framework, 
called **Horizon**, lets you define rules once and enforce them everywhere, automatically.

**Key concepts for this section:**

| Concept | What it means |
|---------|--------------|
| **Role-Based Access Control (RBAC)** | Users are assigned roles; roles are granted privileges on objects. You never grant access to individual users directly. |
| **Masking Policy** | A rule that dynamically replaces sensitive column values (e.g., email, income) based on who's querying. The real data stays intact — it's just hidden from unauthorized roles. |
| **Row Access Policy** | A rule that silently filters rows based on the querying user's role. Restricted users simply don't see rows they shouldn't — no error, no empty result message. |
| **Declarative** | Define a policy once, apply it to any column or table. Every query automatically respects the policy — no application changes needed. |

**Why this matters in banking:**
- **PIPEDA / OSFI compliance** — mask PII for non-authorized roles without creating separate views
- **Multi-team access** — one table serves analysts, data scientists, and auditors with different visibility
- **No data duplication** — instead of copying data into restricted schemas, policies enforce access at query time
- **Auditability** — all access is logged; policies are centrally defined and easy to review

**In this section**, we'll create masking policies to hide email/income and a row access policy to restrict by province — then prove they work by querying another participant's schema.
""")

st.markdown("---")

st.header("Objectives")

st.markdown("""
By the end of this section, you will be able to:

- Understand Snowflake's governance framework (Horizon)
- Create and apply a column-level masking policy
- Create and apply a row access policy
- **See policies in action** by querying another participant's schema
""")

st.markdown("---")

st.header("Part A: Governance Overview")

st.markdown("""
Snowflake Horizon provides unified governance across your data estate:

| Capability | Description |
|-----------|-------------|
| **Role-Based Access Control (RBAC)** | Control who can access what objects |
| **Column-Level Masking** | Dynamically mask sensitive columns based on role |
| **Row Access Policies** | Filter rows based on the querying user's role |
| **Data Classification** | Automatically detect PII and sensitive data |
| **Object Tagging** | Label and categorize objects for compliance |
""")

st.info("""
**Banking Relevance:** Financial institutions must comply with regulations like PIPEDA, OSFI guidelines, 
and PCI-DSS. Snowflake's governance features let you enforce data protection rules declaratively — 
without modifying application code or creating separate views for each team.
""")

st.markdown("---")

st.header("Part B: Column-Level Masking")

st.markdown("""
A masking policy dynamically replaces column values at query time based on the role of the user 
running the query. The underlying data is never modified.
""")

st.markdown("#### Exercise 7.1 — View sensitive data (before masking)")

st.code("""
-- With your lab role, you can see all data
SELECT
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    EMAIL,
    ANNUAL_INCOME
FROM CUSTOMERS
LIMIT 10;
""", language="sql")

st.markdown("#### Exercise 7.2 — Create a masking policy for email")

st.warning("""
⚠️ **Replace `XX` with your participant number** (e.g., `_05` if you are User 05).
This ensures only YOUR role can see unmasked data.
""")

st.code("""
CREATE OR REPLACE MASKING POLICY EMAIL_MASK AS (val STRING)
RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() = 'TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX'
            THEN val
        ELSE REGEXP_REPLACE(val, '.+@', '****@')
    END;
""", language="sql")

st.info("""
**How this works:**
- The policy takes a string value (`val`) and returns a string
- At query time, Snowflake checks `CURRENT_ROLE()` — if it matches **your** role exactly, you see the real email
- For everyone else, `REGEXP_REPLACE` replaces everything before `@` with `****` (e.g., `john.smith@rbc.ca` → `****@rbc.ca`)
- The underlying data is never changed — masking happens dynamically at query time
""")

st.markdown("#### Exercise 7.3 — Apply the masking policy")

st.code("""
ALTER TABLE CUSTOMERS
    MODIFY COLUMN EMAIL
    SET MASKING POLICY EMAIL_MASK;
""", language="sql")

st.markdown("#### Exercise 7.4 — Create and apply a masking policy for income")

st.code("""
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
""", language="sql")

st.markdown("#### Exercise 7.5 — Test: Query YOUR schema (unmasked)")

st.code("""
-- Your role matches the policy — you see full data
SELECT CUSTOMER_ID, EMAIL, ANNUAL_INCOME
FROM CUSTOMERS LIMIT 5;
""", language="sql")

st.success("✅ You should see real email addresses and income values — your role is authorized.")

st.markdown("#### Exercise 7.6 — Test: Query ANOTHER participant's schema (masked)")

st.warning("⚠️ **Pick a neighbor's schema number** (e.g., if you are User 05, try RETAIL_BANKING_03). Your neighbor must have completed Exercises 7.2–7.5 for this to work — if they haven't applied their masking policy yet, you'll see unmasked data.")

st.code("""
-- Query another participant's table — your role does NOT match their policy
SELECT CUSTOMER_ID, EMAIL, ANNUAL_INCOME
FROM TU30_ZERO_TO_SNOWFLAKE_LAB.RETAIL_BANKING_01.CUSTOMERS
LIMIT 5;
""", language="sql")

st.success("""
🎉 **What happened?** You see `****@domain.com` for emails and `NULL` for income. Same table 
structure, same query — but the masking policy only allows the schema owner's role to see real 
data. **This is governance in action.**
""")

st.markdown("---")

st.header("Part C: Row Access Policies")

st.markdown("""
Row access policies filter which **rows** a user can see. This is powerful for multi-tenant 
scenarios or restricting access by geography, business unit, or segment.
""")

st.markdown("#### Exercise 7.7 — Create a row access policy")

st.warning("⚠️ **Replace `XX` with your participant number.**")

st.code("""
-- Only YOUR role sees all provinces; everyone else sees only Ontario
CREATE OR REPLACE ROW ACCESS POLICY PROVINCE_ACCESS AS (province_val VARCHAR)
RETURNS BOOLEAN ->
    CASE
        WHEN CURRENT_ROLE() = 'TU30_ZERO_TO_SNOWFLAKE_LAB_USER_XX'
            THEN TRUE
        ELSE province_val = 'Ontario'
    END;
""", language="sql")

st.markdown("#### Exercise 7.8 — Apply the row access policy")

st.code("""
ALTER TABLE CUSTOMERS
    ADD ROW ACCESS POLICY PROVINCE_ACCESS ON (PROVINCE);
""", language="sql")

st.markdown("#### Exercise 7.9 — Test: Query YOUR schema (all rows)")

st.code("""
-- Your role matches — you see all provinces
SELECT PROVINCE, COUNT(*) AS customer_count
FROM CUSTOMERS
GROUP BY PROVINCE
ORDER BY customer_count DESC;
""", language="sql")

st.success("✅ You should see all 6 provinces (Alberta, British Columbia, Manitoba, Nova Scotia, Ontario, Quebec).")

st.markdown("#### Exercise 7.10 — Test: Query ANOTHER participant's schema (restricted)")

st.warning("⚠️ Same neighbor as before — they must have completed Exercises 7.7–7.9 for the row access policy to be in effect.")

st.code("""
-- Query another participant's table — you only see Ontario rows
SELECT PROVINCE, COUNT(*) AS customer_count
FROM TU30_ZERO_TO_SNOWFLAKE_LAB.RETAIL_BANKING_01.CUSTOMERS
GROUP BY PROVINCE
ORDER BY customer_count DESC;
""", language="sql")

st.success("""
🎉 **What happened?** You only see Ontario customers. The other rows aren't hidden with an error — 
they simply don't exist from your perspective. The row access policy silently filters them out.
""")

st.markdown("---")

st.header("Part D: Clean up")

st.code("""
-- Remove policies from your table
ALTER TABLE CUSTOMERS MODIFY COLUMN EMAIL UNSET MASKING POLICY;
ALTER TABLE CUSTOMERS MODIFY COLUMN ANNUAL_INCOME UNSET MASKING POLICY;
ALTER TABLE CUSTOMERS DROP ROW ACCESS POLICY PROVINCE_ACCESS;

-- Drop policy objects
DROP MASKING POLICY IF EXISTS EMAIL_MASK;
DROP MASKING POLICY IF EXISTS INCOME_MASK;
DROP ROW ACCESS POLICY IF EXISTS PROVINCE_ACCESS;
""", language="sql")

st.markdown("---")

with st.expander("🤖 :blue[CoCo Sneak Peek] — Do this with Cortex Code"):
    st.markdown("""
CoCo can create governance policies from plain English:

| What you did | CoCo prompt |
|-------------|-------------|
| Create email mask | `Create a masking policy that hides email addresses for all roles except my own` |
| Create income mask | `Mask the ANNUAL_INCOME column so only my role can see it` |
| Apply policies | `Apply the email mask to CUSTOMERS.EMAIL` |
| Row access policy | `Create a row access policy so only my role sees all provinces, others see only Ontario` |
| Test policies | `Query CUSTOMERS and show me EMAIL and ANNUAL_INCOME` |
| Clean up | `Remove all masking and row access policies from CUSTOMERS` |

You can also ask: `What governance policies are applied to the CUSTOMERS table?`
""")

st.markdown("---")

st.header("Key Concepts")

st.markdown("""
| Feature | Description |
|---------|-------------|
| Masking Policy | Dynamically redacts column values based on role |
| Row Access Policy | Silently filters rows based on session context |
| Declarative | Policies are applied once, enforced everywhere |
| No data duplication | One table, many access levels |
| Centralized | Policies defined once, applied to any table/column |
""")
