DELETE FROM departments_dup;
## All data gone. ALWAYS ATTACH A CONDITIONAL CLAUSE
SELECT * FROM departments_dup;
## Rollback
ROLLBACK;
SELECT * FROM departments_dup;
## Data back to previous committed state