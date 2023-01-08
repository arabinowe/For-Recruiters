SELECT e.emp_no, e.first_name, e.last_name, s.salary
FROM
employees e
LEFT JOIN 
salaries s ON e.emp_no=s.emp_no
WHERE salary>145000;