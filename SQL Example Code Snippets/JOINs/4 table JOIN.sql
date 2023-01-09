SELECT 
e.first_name, e.last_name, e.hire_date, t.title, dm.from_date, d.dept_name
FROM
dept_manager dm
JOIN 
employees e ON e.emp_no=dm.emp_no
JOIN
titles t ON dm.emp_no=t.emp_no
JOIN
departments d ON dm.dept_no=d.dept_no
;