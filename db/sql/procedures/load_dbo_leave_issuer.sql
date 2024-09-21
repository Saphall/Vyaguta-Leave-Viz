CREATE OR REPLACE PROCEDURE dbo.leave_issuer()
LANGUAGE SQL
AS $$
  -- Case 1: selecting distinct leave issuers whose default leave issuer id and current leave issuer id are same
  INSERT INTO dbo.leave_issuer 
  SELECT DISTINCT
    CAST(currentleaveissuerid AS INT), 
    issuerfirstname, 
    issuerlastname, 
    currentleaveissueremail 
  FROM raw.imported_leave_information ili
  WHERE CAST(currentleaveissuerid AS INT) = CAST(leaveissuerid AS INT)
  ON CONFLICT (leave_issuer_id)
  DO NOTHING;

  -- CASE 2: Selecting distinct default leave issuers who are not the current leave issuers
  INSERT INTO dbo.leave_issuer 
  SELECT DISTINCT
    CAST(ili.leaveissuerid AS INT), 
    ili.issuerfirstname, 
    ili.issuerlastname, 
    ili2.currentleaveissueremail 
  FROM raw.imported_leave_information ili
  LEFT JOIN raw.imported_leave_information ili2 
  ON ili.leaveissuerid = ili2.currentleaveissuerid 
  WHERE ili.leaveissuerid <> ili.currentleaveissuerid
  ON CONFLICT (leave_issuer_id)
  DO NOTHING;

  -- CASE 3: Selecting distinct current leave issuers who are not the default leave issuers 
  INSERT INTO dbo.leave_issuer(leave_issuer_id, email)
  SELECT DISTINCT
    CAST(ili.currentleaveissuerid AS INT),
    ili.currentleaveissueremail 
  FROM raw.imported_leave_information ili
  WHERE ili.leaveissuerid <> ili.currentleaveissuerid
  ON CONFLICT (leave_issuer_id)
  DO NOTHING;
$$;
