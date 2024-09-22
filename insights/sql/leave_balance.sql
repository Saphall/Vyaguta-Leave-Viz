WITH fiscal_dates AS (
  SELECT DISTINCT LEFT(CAST(start_date AS VARCHAR), 4) || '/' || LEFT(CAST(end_date AS VARCHAR), 4) AS fiscal_date
  FROM
    dbo.dim_fiscal_year
),
all_combinations AS (
  SELECT
    e.employee_id,
    lt.leave_type,
    lt.default_days,
    fiscal_dates.fiscal_date
  FROM
    dbo.dim_employees AS e
  CROSS JOIN
    dbo.dim_leave_types AS lt
  CROSS JOIN fiscal_dates
),
leave_data AS (
  SELECT
    e.employee_id,
    lt.leave_type,
    lt.default_days,
    LEFT(CAST(fy.start_date AS VARCHAR), 4) || '/' || LEFT(CAST(fy.end_date AS VARCHAR), 4) AS fiscal_date,
    COALESCE(SUM(CASE WHEN el.leave_type_id = lt.leave_type_id THEN el.leave_days ELSE 0 END), 0) AS total
  FROM
    dbo.dim_employees AS e
  INNER JOIN
    dbo.dim_leave_types AS lt ON lt.leave_type IN (SELECT DISTINCT leave_type FROM dbo.dim_leave_types)
  INNER JOIN
    dbo.dim_fiscal_year AS fy ON fy.fiscal_id = (SELECT fiscal_id FROM dbo.fact_employee_leaves LIMIT 1)
  LEFT JOIN
    dbo.fact_employee_leaves AS el ON e.employee_id = el.employee_id AND lt.leave_type_id = el.leave_type_id
  WHERE el.status = 'APPROVED'
  GROUP BY
    e.employee_id,
    fiscal_date,
    lt.leave_type,
    lt.default_days
)
SELECT
  ac.employee_id,
  ac.leave_type,
  ac.default_days,
  ac.fiscal_date,
  COALESCE(ld.total, 0) AS total
FROM
  all_combinations AS ac
LEFT JOIN
  leave_data AS ld
  ON ac.employee_id = ld.employee_id AND ac.leave_type = ld.leave_type AND ac.fiscal_date = ld.fiscal_date;
