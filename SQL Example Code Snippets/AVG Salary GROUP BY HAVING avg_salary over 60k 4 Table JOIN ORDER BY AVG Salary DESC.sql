SELECT 
    d.dept_name, AVG(salary) as avg_salary
FROM
    salaries s
        JOIN
    employees e ON e.emp_no = s.emp_no
        JOIN
    dept_emp de ON e.emp_no = de.emp_no
        JOIN
    departments d ON de.dept_no = d.dept_no
GROUP BY d.dept_name
HAVING avg_salary>60000
ORDER BY avg_salary DESC;