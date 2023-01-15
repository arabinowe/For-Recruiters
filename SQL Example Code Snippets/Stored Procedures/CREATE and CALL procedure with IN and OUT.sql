USE employees;

DROP PROCEDURE IF EXISTS avg_emp_salary_out;

DELIMITER $$
CREATE PROCEDURE avg_emp_salary_out(IN p_emp_no INTEGER, OUT p_avg_salary DECIMAL(10,2))
BEGIN
SELECT
	AVG(s.salary)
INTO p_avg_salary
	FROM
	employees e
		JOIN 
    salaries s ON e.emp_no=s.emp_no
WHERE 
	e.emp_no=p_emp_no;
END$$

DELIMITER ;
set @p_avg_salary=0;
CALL avg_emp_salary_out(10001,@p_avg_salary);
SELECT @p_avg_salary;