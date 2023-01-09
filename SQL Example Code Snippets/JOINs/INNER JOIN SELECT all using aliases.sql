SELECT *
FROM dept_manager_dup m
INNER JOIN 
employees d 
ON m.emp_no=d.emp_no
ORDER BY m.dept_no;



