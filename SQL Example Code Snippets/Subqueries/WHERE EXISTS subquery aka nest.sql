### EXISTS is similiar to IN, but EXISTS is much faster so it gets used for very large datasets

SELECT 	
e.first_name, e.last_name
FROM
employees e
WHERE
EXISTS (SELECT 
* FROM 
dept_manager dm
WHERE
dm.emp_no=e.emp_no
);