SELECT
  e.employee_id,
  e.first_name,
  e.middle_name,
  e.last_name,
  e.email,
  d.department_name,
  d2.designation_name,
  e.first_name || ' ' || e.last_name AS full_name
FROM dbo.employees AS e
INNER JOIN dbo.departments AS d
  ON e.department_id = d.department_id
INNER JOIN dbo.designations AS d2
  ON e.designation_id = d2.designation_id;
