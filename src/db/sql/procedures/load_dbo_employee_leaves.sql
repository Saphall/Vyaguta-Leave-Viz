CREATE OR REPLACE PROCEDURE dbo.employee_leaves()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.employee_leaves 
  SELECT 
    CAST(id AS INT),
    CASE 
      WHEN (leaveissuerid IS NULL OR leaveissuerid <> currentleaveissuerid)  
      THEN CAST(currentleaveissuerid AS INT)
      ELSE CAST(leaveissuerid AS INT)
    END,
    CAST(leavetypeid AS INT),
    CAST(empid AS INT),
    CAST(fiscalid AS INT),
    CAST(leavedays AS INT),
    reason,
    status,
    remarks,
    CAST(isconsecutive AS BOOLEAN),
    CAST(startdate AS TIMESTAMP),
    CAST(enddate AS TIMESTAMP),
    CAST(createdat AS TIMESTAMP),
    CAST(updatedat AS TIMESTAMP) 
  FROM raw.imported_leave_information ili
  ON CONFLICT (leave_id)
  DO NOTHING;
$$;
