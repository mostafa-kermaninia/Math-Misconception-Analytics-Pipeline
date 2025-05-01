# import pandas as pd
# from sqlalchemy import create_engine

# # تنظیمات اتصال به دیتابیس
# username = 'Mosiyo'       # نام کاربری دیتابیس
# password = '1383' # رمز عبور
# host = '172.29.143.138'        # یا آدرس سرور (مثلاً 127.0.0.1)
# port = '3306'             # پورت پیشفرض MySQL
# database = 'DataScience_DB' # نام دیتابیس هدف

# # ایجاد connection string برای SQLAlchemy
# connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

# # ایجاد موتور اتصال
# engine = create_engine(connection_string)

# # تست اتصال
# try:
#     with engine.connect() as conn:
#         print("✅ Connected to MySQL successfully!")
# except Exception as e:
#     print(f"❌ Connection failed: {e}")
#     exit()
    
    
# # خواندن فایل (بر اساس فرمت دیتاست)
# file_path = "cleaned_data.csv"  # مسیر فایل تمیزشده
# df = pd.read_csv(file_path)     # یا pd.read_excel() برای اکسل

# # نمایش نمونه دادهها
# print(df.head())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_db_connection():

    DB_USER = 'Mosiyo'  # جایگزین با نام کاربری دیتابیس شما
    DB_PASS = '1383'  # جایگزین با رمز عبور دیتابیس شما
    DB_HOST = '172.29.143.138'
    DB_NAME = 'DataScience_DB'  # جایگزین با نام دیتابیس شما
    
    # ایجاد موتور اتصال
    engine = create_engine(
        f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}',
        echo=False  # غیرفعال کردن لاگ‌گیری برای اجرای تمیزتر
    )
    
    # ایجاد session برای تعامل با دیتابیس
    Session = sessionmaker(bind=engine)
    return engine, Session()
