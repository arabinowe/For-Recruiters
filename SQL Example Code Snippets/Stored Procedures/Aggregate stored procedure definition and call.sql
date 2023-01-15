USE employees;

DROP PROCEDURE IF EXISTS avg_emp_salary;

DELIMITER $$
CREATE PROCEDURE avg_emp_salary(IN p_emp_no INTEGER)
BEGIN
SELECT
AVG(s.salary)
FROM
employees e
JOIN salaries s ON e.emp_no=s.emp_no
WHERE e.emp_no=p_emp_no;
END$$

DELIMITER ;

CALL avg_emp_salary(10001);