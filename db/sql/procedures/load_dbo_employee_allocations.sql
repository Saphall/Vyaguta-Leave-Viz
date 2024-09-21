CREATE OR REPLACE PROCEDURE dbo.employee_allocations()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.employee_allocations
  SELECT 
    DISTINCT
    CAST(empid AS INT),
    (data->>'id')::INT AS allocation_id
  FROM (
    SELECT empid, jsonb_array_elements(allocations) AS data
    FROM raw.imported_leave_information 
  ) AS allocations
  ON CONFLICT (employee_id, allocation_id)
  DO NOTHING;
$$;
