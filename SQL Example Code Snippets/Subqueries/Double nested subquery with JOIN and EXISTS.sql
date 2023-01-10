### second subquery requires an alias to be joined, it won't just grab it without giving it an assignment

SELECT * FROM (SELECT * FROM employees e
WHERE
EXISTS (SELECT *
FROM
titles t
WHERE t.emp_no=e.emp_no AND t.title='Assistant Engineer'
)
) AS blank
 JOIN titles t ON blank.emp_no=t.emp_no AND t.title='Assistant Engineer'
;

SELECT * FROM employees
LIMIT 1;