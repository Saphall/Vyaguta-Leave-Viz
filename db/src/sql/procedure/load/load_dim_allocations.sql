CREATE OR REPLACE PROCEDURE dbo.dim_allocations()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.dim_allocations
  SELECT 
    DISTINCT
    (data->>'id')::INT AS allocation_id,
    data->>'name' AS name,
    data->>'type' AS type
  FROM (
    SELECT jsonb_array_elements(allocations) AS data
    FROM std.leave_information_interim
  ) AS allocations
  ON CONFLICT (allocation_id)
  DO NOTHING;
$$;
