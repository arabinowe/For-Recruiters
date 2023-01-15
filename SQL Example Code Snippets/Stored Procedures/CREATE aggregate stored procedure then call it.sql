DELIMITER$$
CREATE PROCEDURE avg_salary()
BEGIN
SELECT avg(salary)
FROM salaries
END$$
DELIMITER ;

CALL avg_salary();