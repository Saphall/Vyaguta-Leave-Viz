CREATE OR REPLACE PROCEDURE dbo.dim_employee_allocations()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.dim_employee_allocations
  SELECT 
    DISTINCT
    emp_id,
    (data->>'id')::INT AS allocation_id
  FROM (
    SELECT 
      emp_id, 
      jsonb_array_elements(allocations) AS data
    FROM std.leave_information_interim 
  ) AS allocations
  ON CONFLICT (employee_id, allocation_id)
  DO NOTHING;
$$;
