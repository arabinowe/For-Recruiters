SELECT e.gender as Gender, count(gender) as Number_of_Managers

FROM
employees e
JOIN
dept_manager dm ON e.emp_no=dm.emp_no
GROUP BY gender;


SELECT count(emp_no) FROM dept_manager
LIMIT 1;