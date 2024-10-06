CREATE OR REPLACE VIEW dbo.vw_employee_details_insight AS
SELECT DISTINCT
  e.employee_id,
  eli.employee_name,
  e.email,
  eli.employee_department,
  eli.employee_designation,
  a.allocation_id,
  a.name AS allocation_name,
  a.type AS allocation_type,
  eli.leave_issuer_id,
  eli.leave_issuer_first_name || ' ' || eli.leave_issuer_last_name AS leave_issuer_name,
  eli.leave_issuer_email,
  eli.fiscal_date,
  eli.start_date,
  eli.end_date
FROM dbo.dim_employees AS e
LEFT JOIN dbo.vw_employee_leaves_insight AS eli
  ON e.employee_id = eli.employee_id
LEFT JOIN dbo.dim_employee_allocations AS ea
  ON e.employee_id = ea.employee_id
LEFT JOIN dbo.dim_allocations AS a
  ON ea.allocation_id = a.allocation_id;
