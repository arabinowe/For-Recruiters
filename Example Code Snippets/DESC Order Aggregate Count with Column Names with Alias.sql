SELECT 
    first_name, COUNT(first_name) as names_count
FROM
    employees
GROUP BY first_name
ORDER BY COUNT(first_name) DESC;