CREATE OR REPLACE PROCEDURE dbo.dim_designations()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.dim_designations
  SELECT DISTINCT
    designation_id,
    designation_name  
  FROM std.leave_information_interim
  ON CONFLICT (designation_id)
  DO NOTHING;
$$;
