CREATE OR REPLACE PROCEDURE dbo.dim_fiscal_year()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.dim_fiscal_year
  SELECT
    fiscal_id,
    fiscal_start_date,
    fiscal_end_date  
  FROM std.leave_information_interim
  ON CONFLICT (fiscal_id)
  DO NOTHING;
$$;
