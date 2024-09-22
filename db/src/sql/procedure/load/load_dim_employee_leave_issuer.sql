CREATE OR REPLACE PROCEDURE dbo.dim_employee_leave_issuer()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.dim_employee_leave_issuer
  SELECT DISTINCT
    emp_id,
    current_leave_issuer_id,
    TRUE AS is_current_leave_issuer
  FROM std.leave_information_interim ili 
  WHERE leave_issuer_id = current_leave_issuer_id
  UNION 
  SELECT DISTINCT
    emp_id,
    leave_issuer_id,
    FALSE AS is_current_leave_issuer
  FROM std.leave_information_interim ili 
  WHERE leave_issuer_id <> current_leave_issuer_id
  UNION
  SELECT DISTINCT
    emp_id,
    current_leave_issuer_id,
    TRUE AS is_current_leave_issuer
  FROM std.leave_information_interim ili
  WHERE leave_issuer_id <> current_leave_issuer_id
    ON CONFLICT (employee_id, leave_issuer_id)
  DO NOTHING;
$$;
