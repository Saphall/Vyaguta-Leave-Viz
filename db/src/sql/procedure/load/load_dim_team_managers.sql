CREATE OR REPLACE PROCEDURE dbo.dim_team_managers()
LANGUAGE SQL
AS $$
  INSERT INTO dbo.dim_team_managers(team_manager_id)
  SELECT DISTINCT 
    team_manager_id
  FROM std.leave_information_interim
  WHERE team_manager_id IS NOT NULL
  ON CONFLICT (team_manager_id)
  DO NOTHING;
$$;
