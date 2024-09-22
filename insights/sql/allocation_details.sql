SELECT DISTINCT
  e.employee_id,
  a.allocation_id,
  a.name,
  a.type
FROM dbo.dim_employees AS e
INNER JOIN dbo.dim_employee_allocations AS ea
  ON e.employee_id = ea.employee_id
INNER JOIN dbo.dim_allocations AS a
  ON ea.allocation_id = a.allocation_id;
