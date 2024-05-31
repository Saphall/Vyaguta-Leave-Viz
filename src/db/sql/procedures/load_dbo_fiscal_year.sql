CREATE OR REPLACE PROCEDURE dbo.fiscal_year()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.fiscal_year 
  SELECT 
    DISTINCT CAST(fiscalId AS INT), 
    CAST(fiscalStartDate AS TIMESTAMP),
    CAST(fiscalEndDate AS TIMESTAMP)  
  FROM raw.imported_leave_information ili
  ON CONFLICT (fiscal_id)
  DO NOTHING;
$$;
