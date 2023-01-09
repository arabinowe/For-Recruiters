SELECT * FROM emp;

CREATE VIEW v_dept_emp_latest_date AS
SELECT
emp_no, MAX(from_date) as from_date, MAX(to_date) as to_date
FROM
dept_emp
GROUP BY emp_no;

SELECT * FROM dept_emp_latest_date;