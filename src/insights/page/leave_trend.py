import pandas as pd


def leave_trend(conn):
    sql = """
        SELECT
          e.employee_id,
          e.first_name as employee_first_name,
          e.middle_name as employee_middle_name, 
          e.last_name as employee_last_name,
          e.email as employee_email,
          e.is_hr as employee_is_hr,
          e.is_supervisor as employee_is_supv,
          e.team_manager_id as employee_team_manager,
          d.designation_id,
          d.designation_name as employee_designation,
          d2.department_id,
          d2.department_name as employee_department,
          li.leave_issuer_id,
          li.first_name as leave_issuer_first_name,
          li.last_name as leave_issuer_last_name,
          li.email as leave_issuer_email,
          el.leave_days,
          lt.leave_type,
          lt.default_days,
          lt.transferrable_days,
          el.leave_id,
          LEFT(cast(fy.start_date as VARCHAR), 4) ||'/'|| LEFT(cast(fy.end_date as VARCHAR), 4) as fiscal_date,
          el.status,
          el.reason,
          el.remarks,
          el.is_consecutive,
          el.start_date,
          el.end_date,
          el.created_at,
          To_char(created_at, 'YYYY') as year,
          To_char(created_at, 'Mon') as hmonth,
          To_char(created_at, 'MonDD') as month,
          To_char(created_at, 'DY') as day,
          To_char(created_at, 'MM') as month_number,
          el.updated_at
        from dbo.employee_leaves el
        inner join dbo.employees e on e.employee_id =el.employee_id 
        inner join dbo.designations d on e.designation_id =d.designation_id
        inner join dbo.leave_types lt on lt.leave_type_id = el.leave_type_id  
        full join dbo.team_managers tm on tm.team_manager_id=e.team_manager_id
        inner join dbo.departments d2 on d2.department_id = e.department_id
        inner join dbo.leave_issuer li on li.leave_issuer_id = el.leave_issuer_id
        inner join dbo.fiscal_year fy on fy.fiscal_id = el.fiscal_id; 
        """

    all_data = pd.read_sql(sql, conn)
    return all_data
