SELECT
e.first_name, e.last_name, e.hire_date, dm.from_date, d.dept_name
FROM
employees e
JOIN
dept_manager dm ON e.emp_no=dm.emp_no
JOIN
departments d ON dm.dept_no=d.dept_no
;