# Query to insert leave data into raw table

LEAVE_DATA_INSERT_QUERY = """
    INSERT INTO {raw_table_name} (
      id, userId, empId, teamManagerId, designationId, designationName, firstName, middleName, lastName, email, sHr, isSupervisor, 
      allocations, leaveIssuerId, currentLeaveIssuerId, issuerFirstName, issuerMiddleName, issuerLastName, currentLeaveIssuerEmail, 
      departmentDescription, startDate, endDate, leaveDays, reason, leaveStatus, status, responseRemarks, leaveTypeId, leaveType, 
      defaultDays, transferableDays, isConsecutive, fiscalId, fiscalStartDate, fiscalEndDate, fiscalIsCurrent, createdAt, updatedAt, 
      isAutomated, isConverted, totalCount
    ) 
    VALUES (
      %(id)s, %(userId)s, %(empId)s, %(teamManagerId)s, %(designationId)s, %(designationName)s, %(firstName)s, %(middleName)s, %(lastName)s, 
      %(email)s, %(isHr)s, %(isSupervisor)s, %(allocations)s, %(leaveIssuerId)s, %(currentLeaveIssuerId)s, %(issuerFirstName)s, %(issuerMiddleName)s, 
      %(issuerLastName)s, %(currentLeaveIssuerEmail)s, %(departmentDescription)s, %(startDate)s, %(endDate)s, %(leaveDays)s, %(reason)s, %(leaveStatus)s,
      %(status)s, %(responseRemarks)s, %(leaveTypeId)s, %(leaveType)s, %(defaultDays)s, %(transferableDays)s, %(isConsecutive)s, %(fiscalId)s, 
      %(fiscalStartDate)s, %(fiscalEndDate)s, %(fiscalIsCurrent)s, %(createdAt)s, %(updatedAt)s, %(isAutomated)s, %(isConverted)s, %(totalCount)s
    )
"""
