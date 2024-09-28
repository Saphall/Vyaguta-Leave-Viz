# Create a new PostgreSQL database
resource "postgresql_database" "vyaguta_db" {
  name = "vyaguta_db"
}

# Create a new PostgreSQL user
resource "postgresql_role" "vyaguta_user" {
  name     = var.vyaguta_user_name
  password = var.vyaguta_user_password
  # Grant SUPERUSER privileges to make the user an admin
  superuser  = true
  login      = true
  create_role = true
}

# Grant privileges to the new user
resource "postgresql_grant" "grant_permission" {
  database   = postgresql_database.vyaguta_db.name
  role       = postgresql_role.vyaguta_user.name
  privileges = ["ALL"]
  object_type = "database"
}
