import sqlalchemy
import os

# Database configurations
DB_CONFIGS = {
    "local": {
        "user": "workbench_user",
        "password": "1",
        "host": "172.24.96.194",
        "port": "3306",
        "database": "University_DB"
    },
    "github": {
        "user": "root",
        "password": "root",
        "host": "localhost",
        "port": "3306",
        "database": "University_DB"
    }
}

def get_db_engine():
    """Returns a connection engine for MySQL."""
    # Check if running in GitHub Actions
    if os.getenv('GITHUB_ACTIONS') == 'true':
        config = DB_CONFIGS["github"]
    else:
        config = DB_CONFIGS["local"]
    
    connection_string = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    engine = sqlalchemy.create_engine(connection_string)
    return engine