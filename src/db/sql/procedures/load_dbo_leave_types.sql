CREATE OR REPLACE PROCEDURE dbo.extract_leave_types()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.leave_types 
  SELECT 
    DISTINCT 
    CAST(leaveTypeId AS INT), 
    leaveType,
    CAST(defaultDays AS INT), 
    CAST(transferableDays AS INT)  
  FROM raw.imported_leave_information ili
  ON CONFLICT (leave_type_id)
  DO NOTHING;
$$;
