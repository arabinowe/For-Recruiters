## Delete statement - removing records from a database
USE employees;

## Check record to delete
SELECT 
    *
FROM
    titles
WHERE
    emp_no = '999903';
    
DELETE FROM employees 
WHERE
    emp_no = '999903';

## Check record deletion (CASCADES)
SELECT 
    *
FROM
    employees
WHERE
    emp_no = '999903';
    
SELECT 
    *
FROM
    titles
WHERE
    emp_no = '999903';

## Successful deletion from cascading tables.
