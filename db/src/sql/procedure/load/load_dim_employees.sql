CREATE OR REPLACE PROCEDURE dbo.dim_employees()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.dim_employees
  SELECT DISTINCT
    ili.emp_id,
    ili.first_name,
    ili.middle_name,
    ili.last_name,
    ili.email,
    ili.is_hr,
    ili.is_supervisor,
    ili.designation_id,
    ili.team_manager_id,
    d.department_id
  FROM std.leave_information_interim ili 
  INNER JOIN dbo.dim_departments d 
    ON d.department_name = ili.department_description
  ON CONFLICT (employee_id)
  DO NOTHING;
$$;
