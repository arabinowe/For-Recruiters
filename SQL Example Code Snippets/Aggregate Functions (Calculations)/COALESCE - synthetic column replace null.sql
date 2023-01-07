SELECT 
    dept_no,
    dept_name,
    COALESCE('N/A') AS not_null
FROM
    departments_dup
ORDER BY dept_name ASC;