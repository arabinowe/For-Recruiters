SELECT 
    e.emp_no, e.first_name, e.last_name, m.dept_no, m.from_date
FROM
    employees e
        RIGHT JOIN
   dept_manager m  ON e.emp_no = m.emp_no
WHERE e.last_name='Markovitch'
ORDER BY m.dept_no DESC, e.emp_no;

