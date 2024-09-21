CREATE OR REPLACE PROCEDURE dbo.allocations()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.allocations
  SELECT 
    DISTINCT
    (data->>'id')::INT AS allocation_id,
    data->>'name' AS name,
    data->>'type' AS type
  FROM (
    SELECT jsonb_array_elements(allocations) AS data
    FROM raw.imported_leave_information 
  ) AS allocations
  ON CONFLICT (allocation_id)
  DO NOTHING;
$$;
