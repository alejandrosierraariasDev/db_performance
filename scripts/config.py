import os

# Database connection settings, read from environment variables.
# Example:
#   export DB_NAME=my_db DB_USER=my_user DB_PASSWORD=... DB_HOST=localhost DB_PORT=5432
DB_CONFIG = {
    'dbname': os.environ.get('DB_NAME', 'postgres'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'REDACTED': os.environ.get('DB_PASSWORD', ''),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
}
