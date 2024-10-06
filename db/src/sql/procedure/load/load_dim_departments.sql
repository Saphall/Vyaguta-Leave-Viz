CREATE OR REPLACE PROCEDURE dbo.dim_departments()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.dim_departments(department_name)  
  SELECT DISTINCT department_description
  FROM std.leave_information_interim
  ON CONFLICT (department_name)
  DO NOTHING;
$$;
