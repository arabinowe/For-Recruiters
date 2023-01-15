DROP PROCEDURE IF EXISTS emp_info;

DELIMITER $$
CREATE PROCEDURE emp_info(IN p_first_name VARCHAR(255),IN p_last_name VARCHAR(255), OUT p_emp_no INTEGER)
BEGIN
SELECT e.emp_no
INTO p_emp_no
FROM
employees e
WHERE
e.first_name=p_first_name AND e.last_name=p_last_name LIMIT 1;
END$$
DELIMITER ;

CALL emp_info('Georgi','Facello',@p_emp_no);
SELECT @p_emp_no;