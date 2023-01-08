SELECT e.emp_no, e.first_name, e.last_name, t.title
FROM
employees e
LEFT JOIN
titles t ON e.emp_no=t.emp_no
WHERE e.first_name='Margareta' AND e.last_name='Markovitch';