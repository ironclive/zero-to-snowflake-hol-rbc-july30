import streamlit as st

st.title("⏪ Time Travel & UNDROP")

st.markdown("**Duration:** ~15 minutes")

st.markdown("---")

st.markdown("""
## What is Time Travel?

Every time data changes in Snowflake — an `INSERT`, `UPDATE`, `DELETE`, or `DROP` — Snowflake 
automatically preserves the **previous version** of the data. This means you can query any table 
as it existed at any point in the past, without configuring backups or snapshots.

**Key concepts for this section:**

| Concept | What it means |
|---------|--------------|
| **Time Travel** | Query historical data using `AT(OFFSET => -N)` or `AT(TIMESTAMP => '...')`. See what your table looked like 5 minutes ago, 1 hour ago, or yesterday. |
| **UNDROP** | Instantly restore a dropped table, schema, or database. No restore process, no waiting — it's immediate. |
| **Retention Period** | How long Snowflake keeps historical versions: 1 day (Standard edition), up to 90 days (Enterprise+). |
| **No configuration** | Time Travel is always on. You don't enable it, configure it, or manage it. It just works. |

**Why this matters in banking:**
- Accidentally deleted customer records? Restore them in seconds.
- Need to audit what data looked like at month-end? Query it directly.
- Someone dropped a critical table? `UNDROP` brings it back instantly.
- Compliance teams can verify data as-of any point within retention.

**In this section**, we'll delete data, query it from the past, restore it, and recover a dropped table.
""")

st.markdown("---")

st.header("Objectives")

st.markdown("""
By the end of this section, you will be able to:

- Understand Snowflake's Time Travel capability
- Query historical data using `AT` and `BEFORE` clauses
- Recover a dropped table instantly with `UNDROP`
- Appreciate how Time Travel supports data recovery without backups
""")

st.markdown("---")

st.header("Part A: Understanding Time Travel")

st.markdown("""
Snowflake automatically retains historical versions of your data for a configurable retention period 
(default: 1 day for Standard, up to 90 days for Enterprise+). This means you can query data **as it existed 
at any point** within that window — no snapshots or backups required.
""")

st.info("""
**Key Concept:** Time Travel operates at the micro-partition level. When data changes, Snowflake 
preserves the old micro-partitions for the retention period, enabling point-in-time queries at no 
additional configuration cost.
""")

st.markdown("---")

st.header("Part B: Querying Historical Data")

st.markdown("#### Exercise 4.1 — Check current row count")

st.code("""
SELECT COUNT(*) AS current_count FROM CUSTOMERS;
""", language="sql")

st.markdown("#### Exercise 4.2 — Delete some rows")

st.code("""
-- Delete customers in a specific segment
DELETE FROM CUSTOMERS
WHERE CUSTOMER_SEGMENT = 'Basic';

-- Confirm the delete
SELECT COUNT(*) AS after_delete FROM CUSTOMERS;
""", language="sql")

st.markdown("#### Exercise 4.3 — Query the table BEFORE the delete")

st.code("""
-- Query the table as it was 5 minutes ago
SELECT COUNT(*) AS before_delete
FROM CUSTOMERS AT(OFFSET => -60*5);
""", language="sql")

st.success("""
**What happened?** Even though we deleted rows, Snowflake still has the previous version of the data. 
The `AT(OFFSET => -300)` clause queries the table as it existed 300 seconds (5 minutes) ago.
""")

st.markdown("#### Exercise 4.4 — Restore the deleted data")

st.code("""
-- Re-insert the deleted rows from the historical version
INSERT INTO CUSTOMERS
SELECT * FROM CUSTOMERS AT(OFFSET => -60*5)
WHERE CUSTOMER_SEGMENT = 'Basic';

-- Verify restoration
SELECT COUNT(*) AS restored_count FROM CUSTOMERS;
""", language="sql")

st.markdown("---")

st.header("Part C: UNDROP a Table")

st.markdown("#### Exercise 4.5 — Accidentally drop a table")

st.code("""
-- Create a clone to experiment with safely
CREATE TABLE CUSTOMERS_BACKUP CLONE CUSTOMERS;

-- Oops! Drop the backup
DROP TABLE CUSTOMERS_BACKUP;

-- Verify it's gone
SHOW TABLES LIKE 'CUSTOMERS_BACKUP';
""", language="sql")

st.markdown("#### Exercise 4.6 — Recover with UNDROP")

st.code("""
-- Instantly restore the dropped table
UNDROP TABLE CUSTOMERS_BACKUP;

-- Verify it's back
SELECT COUNT(*) FROM CUSTOMERS_BACKUP;
""", language="sql")

st.success("""
**Key Takeaway:** `UNDROP` restores a dropped table to its exact state before deletion — instantly, 
with no restore-from-backup process. This works for tables, schemas, and entire databases.
""")

st.markdown("#### Exercise 4.7 — Clean up")

st.code("""
DROP TABLE CUSTOMERS_BACKUP;
""", language="sql")

st.markdown("---")

with st.expander("🤖 :blue[CoCo Sneak Peek] — Do this with Cortex Code"):
    st.markdown("""
CoCo makes Time Travel feel like a conversation:

| What you did | CoCo prompt |
|-------------|-------------|
| Check count | `How many customers do we have?` |
| Delete rows | `Delete all Basic segment customers from CUSTOMERS` |
| Query history | `Show me the CUSTOMERS table as it was 5 minutes ago` |
| Restore data | `Restore the Basic segment customers I just deleted using Time Travel` |
| Clone + Drop | `Clone CUSTOMERS to CUSTOMERS_BACKUP, then drop the backup` |
| UNDROP | `Undrop CUSTOMERS_BACKUP` |

You can also ask: `What was the customer count before my last DELETE?`
""")

st.markdown("---")

st.header("Key Concepts")

st.markdown("""
| Feature | Description |
|---------|-------------|
| `AT(OFFSET => -N)` | Query data as it was N seconds ago |
| `AT(TIMESTAMP => '...')` | Query data at a specific timestamp |
| `BEFORE(STATEMENT => 'id')` | Query data before a specific query ran |
| `UNDROP TABLE/SCHEMA/DATABASE` | Instantly recover dropped objects |
| Retention period | 1 day (Standard) / up to 90 days (Enterprise+) |
""")
