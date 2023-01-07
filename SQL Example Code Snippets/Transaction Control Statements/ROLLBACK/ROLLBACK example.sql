UPDATE departments_dup
SET
	dept_no='d011',
    dept_name='Quality Control' ;
## Be Careful!    
ROLLBACK;

SELECT * FROM departments_dup;

## Recommit rollback state
COMMIT;