# Define the PostgreSQL provider
provider "postgresql" {
  host     = var.db_host
  port     = var.db_port
  database = var.db_name
  username = var.db_user
  password = var.db_password
  sslmode  = "disable"
}
