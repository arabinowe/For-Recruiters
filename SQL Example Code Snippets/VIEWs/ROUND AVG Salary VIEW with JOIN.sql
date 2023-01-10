CREATE OR REPLACE VIEW avg_dept_manager_salary AS
SELECT 
ROUND(AVG(salary),2)
FROM
salaries s
JOIN
dept_manager dm ON s.emp_no=dm.emp_no
;

SELECT * FROM avg_dept_manager_salary;

SELECT * FROM dept_manager;
#connector may be emp_no 

SELECT * FROM salaries;
#connector may be emp_no