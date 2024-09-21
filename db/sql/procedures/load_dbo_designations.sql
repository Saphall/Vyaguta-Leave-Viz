CREATE OR REPLACE PROCEDURE dbo.designations()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.designations 
  SELECT DISTINCT CAST(designationid AS INT),
    designationname  
  FROM raw.imported_leave_information ili
  ON CONFLICT (designation_id)
  DO NOTHING;
$$;
