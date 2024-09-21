CREATE OR REPLACE PROCEDURE dbo.team_managers()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.team_managers(team_manager_id) 
  SELECT DISTINCT CAST(teammanagerid AS INT)
  FROM raw.imported_leave_information ili
  WHERE CAST(teammanagerid AS INT) IS NOT NULL
  ON CONFLICT (team_manager_id)
  DO NOTHING;
$$;
