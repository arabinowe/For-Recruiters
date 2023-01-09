SELECT
e.emp_no,
e.first_name,
e.last_name,
NULL AS dept_no,
NULL AS from_date
FROM
employees_dup e
WHERE
e.emp_no=10001
UNION ALL SELECT
NULL AS emp_no,
NULL AS first_name,
NULL AS last_name,
m.dept_no,
m.from_date
FROM dept_manager m;