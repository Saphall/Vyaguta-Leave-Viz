CREATE TABLE IF NOT EXISTS dbo.fact_employee_leaves (
  leave_id INT PRIMARY KEY,
  leave_issuer_id INT,
  leave_type_id INT,
  employee_id INT,
  fiscal_id INT,
  leave_days INT,
  reason TEXT,
  status VARCHAR(100),
  response_remarks TEXT,
  is_consecutive BOOLEAN,
  start_date DATE,
  end_date DATE,
  created_at DATE,
  updated_at DATE,
  CONSTRAINT employee_leaves_leave_issuer_id_fk FOREIGN KEY (
    leave_issuer_id
  ) REFERENCES dbo.dim_leave_issuer (leave_issuer_id),
  CONSTRAINT employee_leaves_leave_type_id_fk FOREIGN KEY (
    leave_type_id
  ) REFERENCES dbo.dim_leave_types (leave_type_id),
  CONSTRAINT employee_leaves_emp_id_fk FOREIGN KEY (
    employee_id
  ) REFERENCES dbo.dim_employees (employee_id),
  CONSTRAINT employee_leaves_fiscal_id_fk FOREIGN KEY (
    fiscal_id
  ) REFERENCES dbo.dim_fiscal_year (fiscal_id)
);
