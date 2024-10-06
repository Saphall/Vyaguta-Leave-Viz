CREATE TABLE IF NOT EXISTS dbo.dim_departments (
  department_id SERIAL PRIMARY KEY,
  department_name VARCHAR(100) UNIQUE
);
