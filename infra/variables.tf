# Define input variables for the configuration
variable "db_host" {
  description = "PostgreSQL host"
  type        = string
  default     = "localhost"
}

variable "db_port" {
  description = "PostgreSQL port"
  type        = number
  default     = 5432
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "postgres" # The default database for the connection
}

variable "db_user" {
  description = "Database user"
  type        = string
  default     = "postgres" # The default user, adjust as needed
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true # Marks this as a sensitive value to hide it in logs
}

variable "vyaguta_user_name" {
    description = "The name of the PostgreSQL user"
    type        = string
    default     = "vyaguta_user"
  }

variable "vyaguta_user_password" {
    description = "The password for the PostgreSQL user"
    type        = string
  }