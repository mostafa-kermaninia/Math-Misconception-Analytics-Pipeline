from sqlalchemy import create_engine

# Database configuration
DB_CONFIG = {
    "user": "Mosiyo",
    "password": "1383",
    "host": "172.29.143.138",
    "port": "3306",
    "database": "DataScience_DB"
}

# Function to create and return the database connection engine
def get_db_engine():
    return create_engine(f"mysql+pymysql://{DB_CONFIG['user']}:\
        {DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG\
            ['port']}/{DB_CONFIG['database']}")
