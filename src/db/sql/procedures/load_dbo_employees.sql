CREATE OR REPLACE PROCEDURE dbo.employees()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.employees 
  SELECT DISTINCT 
    CAST(ili.empid AS INT), 
    ili.firstname, 
    ili.middlename, 
    ili.lastname, 
    ili.email, 
    CAST(ili.ishr AS BOOLEAN), 
    CAST(ili.issupervisor AS BOOLEAN),
    CAST(ili.designationid AS INT), 
    CAST(ili.teammanagerid AS INT), 
    d.department_id  
  FROM raw.imported_leave_information ili 
  INNER JOIN dbo.departments d ON d.department_name = ili.departmentdescription
  ON CONFLICT (employee_id)
  DO NOTHING;
$$;
