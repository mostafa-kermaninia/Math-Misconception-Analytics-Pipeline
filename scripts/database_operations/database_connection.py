import sqlalchemy
import os

def get_db_engine():
    """Returns a connection engine for MySQL with enhanced compatibility."""
    # استفاده از متغیرهای محیطی اگر وجود دارند، در غیر این صورت از مقادیر پیش‌فرض
    db_config = {
        "user": os.getenv('DB_USER', 'workbench_user'),
        "password": os.getenv('DB_PASSWORD', '1'),
        "host": os.getenv('DB_HOST', '172.24.96.194'),
        "port": os.getenv('DB_PORT', '3306'),
        "database": os.getenv('DB_NAME', 'University_DB'),
        "connect_args": {
            'connect_timeout': 10  # افزایش زمان انتظار برای اتصال
        }
    }
    
    # تنظیمات خاص برای GitHub Actions
    if os.getenv('GITHUB_ACTIONS') == 'true':
        db_config.update({
            "host": "127.0.0.1",  # استفاده از localhost در GitHub Actions
            "port": "3306",
            "connect_args": {
                'connect_timeout': 20  # زمان بیشتر برای محیط CI
            }
        })
    
    connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = sqlalchemy.create_engine(
        connection_string,
        pool_pre_ping=True,  # بررسی سلامت اتصال قبل از استفاده
    )
    return engine