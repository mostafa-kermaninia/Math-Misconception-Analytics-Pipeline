import sqlalchemy

# Database configuration
DB_CONFIG = {
    "user": "Mosiyo",           # Username for your database
    "password": "1383",         # Password for your database
    "host": "172.29.143.138",   # Host IP
    "port": "3306",             # Port number
    "database": "DataScience_DB"  # Database name
}

# Create a connection to the database
def get_db_engine():
    """Returns a connection engine for MySQL."""
    engine = sqlalchemy.create_engine(f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    return engine
