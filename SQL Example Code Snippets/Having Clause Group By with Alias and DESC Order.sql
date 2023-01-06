USE employees;

SELECT 
    emp_no, AVG(salary) AS average_salary
FROM
    Salaries
GROUP BY emp_no
HAVING AVG(salary) > 120000
ORDER BY average_salary DESC;