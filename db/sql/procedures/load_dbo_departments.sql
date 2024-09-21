CREATE OR REPLACE PROCEDURE dbo.departments()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.departments(department_name)  
  SELECT DISTINCT departmentDescription
  FROM raw.imported_leave_information ili
  ON CONFLICT (department_id)
  DO NOTHING;
$$;
