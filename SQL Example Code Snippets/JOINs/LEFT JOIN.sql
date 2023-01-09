SELECT 
    e.emp_no, d.emp_no, e.first_name, e.last_name, m.dept_no
FROM
    dept_manager m
        LEFT JOIN
    employees e ON e.emp_no = d.emp_no
WHERE e.last_name='Markovitch'
ORDER BY e.emp_no;

