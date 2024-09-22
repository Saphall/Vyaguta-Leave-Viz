CREATE OR REPLACE PROCEDURE dbo.fact_employee_leaves()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.fact_employee_leaves
  SELECT
    id,
    CASE
      WHEN (leave_issuer_id IS NULL OR leave_issuer_id <> current_leave_issuer_id)
      THEN current_leave_issuer_id
      ELSE leave_issuer_id
    END,
    leave_type_id,
    emp_id,
    fiscal_id,
    leave_days,
    reason,
    status,
    response_remarks,
    is_consecutive,
    start_date,
    end_date,
    created_at,
    updated_at
  FROM std.leave_information_interim ili
  ON CONFLICT (leave_id)
  DO NOTHING;
$$;
