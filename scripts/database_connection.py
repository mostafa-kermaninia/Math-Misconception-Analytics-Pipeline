import sqlalchemy
import os

def get_db_engine():
    """Returns a connection engine for MySQL with enhanced compatibility."""
    db_config = {
        "user": os.getenv('DB_USER', 'workbench_user'),
        "password": os.getenv('DB_PASSWORD', '1'),
        "host": os.getenv('DB_HOST', '172.24.96.194'),  # مقدار پیش‌فرض برای محیط محلی
        "port": os.getenv('DB_PORT', '3306'),
        "database": os.getenv('DB_NAME', 'University_DB'),
        "connect_args": {
            'connect_timeout': 10,
            'client_flag': 0,
            'ssl': False
        }
    }
    
    if os.getenv('GITHUB_ACTIONS') == 'true':
        db_config.update({
            "host": os.getenv('DB_HOST', '172.18.0.2'),  
            "connect_args": {
                'connect_timeout': 20,
                'client_flag': 0,
                'ssl': False
            }
        })
    
    connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    
    engine = sqlalchemy.create_engine(
        connection_string,
        pool_pre_ping=True,  
        pool_recycle=3600,  
        pool_size=5,         
        max_overflow=10,    
        echo=False          
    )
    return engine