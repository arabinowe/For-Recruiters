SELECT *
FROM dept_manager_dup m
INNER JOIN 
departments_dup d 
ON m.dept_no=d.dept_no
ORDER BY m.dept_no;



