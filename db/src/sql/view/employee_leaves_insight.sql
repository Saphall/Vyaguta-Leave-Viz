CREATE OR REPLACE VIEW dbo.vw_employee_leaves_insight AS
WITH RankedLeaves AS (
  SELECT
    e.employee_id,
    e.first_name AS employee_first_name,
    e.middle_name AS employee_middle_name,
    e.last_name AS employee_last_name,
    e.first_name || ' ' || e.last_name AS employee_name,
    e.email AS employee_email,
    e.is_hr AS employee_is_hr,
    e.is_supervisor AS employee_is_supv,
    e.team_manager_id AS employee_team_manager,
    d.designation_id,
    d.designation_name AS employee_designation,
    d2.department_id,
    d2.department_name AS employee_department,
    li.leave_issuer_id,
    li.first_name AS leave_issuer_first_name,
    li.last_name AS leave_issuer_last_name,
    li.email AS leave_issuer_email,
    el.leave_days,
    lt.leave_type,
    lt.default_days,
    lt.transferrable_days,
    el.leave_id,
    el.status,
    el.reason,
    el.response_remarks,
    el.is_consecutive,
    el.start_date,
    el.end_date,
    el.created_at,
    el.updated_at,
    e.first_name || ' ' || e.last_name AS full_name,
    LEFT(CAST(fy.start_date AS VARCHAR), 4) || '/' || LEFT(CAST(fy.end_date AS VARCHAR), 4) AS fiscal_date,
    TO_CHAR(el.start_date, 'YYYY') AS leave_year,
    TO_CHAR(el.start_date, 'Mon') AS leave_month,
    TO_CHAR(el.start_date, 'MonDD') AS leave_month_dd,
    TO_CHAR(el.start_date, 'DY') AS leave_day,
    TO_CHAR(el.start_date, 'MM') AS month_number,
    ROW_NUMBER()
      OVER (
        PARTITION BY e.employee_id, el.created_at, el.updated_at, el.leave_type_id, el.fiscal_id
        ORDER BY el.created_at DESC
      )
    AS rn
  FROM dbo.fact_employee_leaves AS el
  INNER JOIN dbo.dim_employees AS e
    ON el.employee_id = e.employee_id
  INNER JOIN dbo.dim_designations AS d
    ON e.designation_id = d.designation_id
  INNER JOIN dbo.dim_leave_types AS lt
    ON el.leave_type_id = lt.leave_type_id
  LEFT JOIN dbo.dim_team_managers AS tm
    ON e.team_manager_id = tm.team_manager_id
  INNER JOIN dbo.dim_departments AS d2
    ON e.department_id = d2.department_id
  LEFT JOIN dbo.dim_leave_issuer AS li
    ON el.leave_issuer_id = li.leave_issuer_id
  INNER JOIN dbo.dim_fiscal_year AS fy
    ON el.fiscal_id = fy.fiscal_id
)
SELECT
  employee_id,
  employee_first_name,
  employee_middle_name,
  employee_last_name,
  employee_name,
  employee_email,
  employee_is_hr,
  employee_is_supv,
  employee_team_manager,
  designation_id,
  employee_designation,
  department_id,
  employee_department,
  leave_issuer_id,
  leave_issuer_first_name,
  leave_issuer_last_name,
  leave_issuer_email,
  leave_days,
  leave_type,
  default_days,
  transferrable_days,
  leave_id,
  status,
  reason,
  response_remarks,
  is_consecutive,
  start_date,
  end_date,
  created_at,
  updated_at,
  full_name,
  fiscal_date,
  leave_year,
  leave_month,
  leave_month_dd,
  leave_day,
  month_number
FROM RankedLeaves
WHERE rn = 1;
