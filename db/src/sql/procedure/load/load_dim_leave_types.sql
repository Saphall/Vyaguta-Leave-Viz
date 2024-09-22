CREATE OR REPLACE PROCEDURE dbo.dim_extract_leave_types()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.dim_leave_types
  SELECT 
    DISTINCT 
    leave_type_id, 
    leave_type,
    default_days, 
    transferable_days
  FROM std.leave_information_interim ili
  ON CONFLICT (leave_type_id)
  DO NOTHING;
$$;
