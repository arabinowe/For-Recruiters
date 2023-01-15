DELIMITER $$
CREATE PROCEDURE avg_salary()
SELECT avg(salary)
FROM salaries$$
DELIMITER ;

CALL avg_salary();