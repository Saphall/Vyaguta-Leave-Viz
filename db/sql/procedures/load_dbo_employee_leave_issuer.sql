CREATE OR REPLACE PROCEDURE dbo.employee_leave_issuer()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.employee_leave_issuer 
  SELECT DISTINCT 
    CAST(empid AS INT),
    CAST(currentleaveissuerid AS INT),
    TRUE AS is_current_leave_issuer 
  FROM raw.imported_leave_information ili 
  WHERE leaveissuerid = currentleaveissuerid
  UNION 
  SELECT DISTINCT 
    CAST(empid AS INT),
    CAST(leaveissuerid AS INT),
    FALSE AS is_current_leave_issuer 
  FROM raw.imported_leave_information ili 
  WHERE leaveissuerid <> currentleaveissuerid
  UNION
  SELECT DISTINCT 
    CAST(empid AS INT),
    CAST(currentleaveissuerid AS INT),
    TRUE AS is_current_leave_issuer 
  FROM raw.imported_leave_information ili 
  WHERE leaveissuerid <> currentleaveissuerid
  ON CONFLICT (employee_id, leave_issuer_id)
  DO NOTHING;
$$;
