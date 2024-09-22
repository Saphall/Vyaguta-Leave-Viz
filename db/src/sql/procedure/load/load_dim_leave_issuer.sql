CREATE OR REPLACE PROCEDURE dbo.dim_leave_issuer()
LANGUAGE SQL
AS $$
  -- Case 1: selecting distinct leave issuers whose default leave issuer id and current leave issuer id are same
  INSERT INTO dbo.dim_leave_issuer
  SELECT DISTINCT
    current_leave_issuer_id,
    issuer_first_name,
    issuer_last_name,
    current_leave_issuer_email
  FROM std.leave_information_interim
  WHERE current_leave_issuer_id = leave_issuer_id
  ON CONFLICT (leave_issuer_id)
  DO NOTHING;

  -- CASE 2: Selecting distinct default leave issuers who are not the current leave issuers
  INSERT INTO dbo.dim_leave_issuer
  SELECT DISTINCT
    ili.leave_issuer_id,
    ili.issuer_first_name,
    ili.issuer_last_name,
    ili2.current_leave_issuer_email
  FROM std.leave_information_interim ili
  LEFT JOIN std.leave_information_interim ili2
    ON ili.leave_issuer_id = ili2.current_leave_issuer_id
  WHERE ili.leave_issuer_id <> ili.current_leave_issuer_id
  ON CONFLICT (leave_issuer_id)
  DO NOTHING;

  -- CASE 3: Selecting distinct current leave issuers who are not the default leave issuers 
  INSERT INTO dbo.dim_leave_issuer(leave_issuer_id, email)
  SELECT DISTINCT
    ili.current_leave_issuer_id,
    ili.current_leave_issuer_email
  FROM std.leave_information_interim ili
  WHERE ili.leave_issuer_id <> ili.current_leave_issuer_id
  ON CONFLICT (leave_issuer_id)
  DO NOTHING;
$$;
