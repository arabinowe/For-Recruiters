## Remove specific record
SELECT * FROM departments;

DELETE FROM departments
WHERE dept_no='d010';
SELECT * FROM departments;
## successful record deletion