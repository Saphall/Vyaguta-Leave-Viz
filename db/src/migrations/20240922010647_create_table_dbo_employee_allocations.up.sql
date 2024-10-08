CREATE TABLE IF NOT EXISTS dbo.dim_employee_allocations (
  employee_id INT,
  allocation_id INT,
  CONSTRAINT pk_empid_allocation_id PRIMARY KEY (
    employee_id, allocation_id
  ),
  CONSTRAINT employee_allocations_emp_id_fk FOREIGN KEY (
    employee_id
  ) REFERENCES dbo.dim_employees (employee_id),
  CONSTRAINT employee_allocations_alloc_id_fk FOREIGN KEY (
    allocation_id
  ) REFERENCES dbo.dim_allocations (allocation_id)
);
