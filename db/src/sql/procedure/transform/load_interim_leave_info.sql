CREATE OR REPLACE PROCEDURE std.extract_leave_info_interim()
LANGUAGE SQL
AS $$

    TRUNCATE TABLE std.leave_information_interim;
    
    INSERT INTO std.leave_information_interim (  
      id,
      user_id,
      emp_id,
      team_manager_id,
      designation_id,
      designation_name,
      first_name,
      middle_name,
      last_name,
      email,
      is_hr,
      is_supervisor,
      allocations,
      leave_issuer_id,
      issuer_first_name,
      issuer_middle_name,
      issuer_last_name,
      current_leave_issuer_id,
      current_leave_issuer_email,
      department_description,
      start_date,
      end_date,
      leave_days,
      reason,
      leave_status,
      status,
      response_remarks,
      leave_type_id,
      leave_type,
      default_days,
      transferable_days,
      is_consecutive,
      fiscal_id,
      fiscal_start_date,
      fiscal_end_date,
      fiscal_is_current,
      created_at,
      updated_at,
      is_automated,
      is_converted,
      total_count,
      ingested_at
    )
    SELECT 
      CAST(id AS INT) AS id, 
      CAST(userid AS INT) AS user_id,
      CAST(empid AS INT) AS emp_id,
      CAST(teammanagerid AS INT) AS team_manager_id,
      CAST(designationid AS INT) AS designation_id,
      designationname AS designation_name,
      firstname AS first_name,
      middlename AS middle_name,
      lastname AS last_name,
      CASE
          WHEN lastname IS NULL THEN email
          WHEN POSITION(lastname IN email) > 0 THEN email
          ELSE LOWER(
            CONCAT(
            REPLACE(firstname, ' ', ''),
            REPLACE(lastname, ' ', ''),
            SUBSTRING(
            email
            FROM POSITION('@' IN email)
          )))
      END AS email,
      CAST(ishr AS BOOLEAN) AS is_hr,
      CAST(issupervisor AS BOOLEAN) AS is_supervisor,
      CAST(allocations AS JSONB) AS allocations,
      CAST(leaveissuerid AS INT) AS leave_issuer_id,
      issuerfirstname AS issuer_first_name,
      issuermiddlename AS issuer_middle_name,
      issuerlastname AS issuer_last_name,
      CAST(currentleaveissuerid AS INT) AS current_leave_issuer_id,
      CASE
         WHEN issuerlastname IS NULL THEN currentleaveissueremail
         WHEN POSITION(issuerlastname IN currentleaveissueremail) > 0 THEN currentleaveissueremail
         ELSE LOWER(
           CONCAT(
           REPLACE(issuerfirstname, ' ', ''),
           REPLACE(issuerlastname, ' ', ''),
           SUBSTRING(
           currentleaveissueremail
           FROM POSITION('@' IN currentleaveissueremail)
         )))
      END AS current_leave_issuer_email,
      departmentdescription AS department_description,
      CAST(startdate AS TIMESTAMP) AS start_date,
      CAST(enddate AS TIMESTAMP) AS end_date,
      CAST(leavedays AS INT) AS leave_days,
      reason AS reason,
      leavestatus AS leave_status,
      status AS status,
      responseremarks AS response_remarks,
      CAST(leavetypeid AS INT) AS leave_type_id,
      leavetype AS leave_type,
      CAST(defaultdays AS INT) AS default_days,
      CAST(transferabledays AS INT) AS transferable_days,
      CAST(isconsecutive AS BOOLEAN) AS is_consecutive,
      CAST(fiscalid AS INT) AS fiscal_id,
      CAST(fiscalstartdate AS TIMESTAMP) AS fiscal_start_date,
      CAST(fiscalenddate AS TIMESTAMP) AS fiscal_end_date,
      CAST(fiscaliscurrent AS BOOLEAN) AS fiscal_is_current,
      CAST(createdat AS TIMESTAMP) AS created_at,
      CAST(updatedat AS TIMESTAMP) AS updated_at,
      CAST(isautomated AS INT) AS is_automated,
      CAST(isconverted AS INT) AS is_converted,
      CAST(totalcount AS INT) AS total_count,
      NOW() AS ingested_at
    FROM raw.imported_leave_information
    WHERE lastname !~ '[=()]';
$$;
