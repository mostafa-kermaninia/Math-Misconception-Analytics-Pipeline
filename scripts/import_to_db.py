from sqlalchemy import inspect
from database_connection import get_db_connection
import pandas as pd

def import_data(df: pd.DataFrame, table_name: str):
    """
    ایمپورت DataFrame به جدول مورد نظر در دیتابیس
    """
    engine, session = get_db_connection()
    
    # بررسی وجود جدول در دیتابیس
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        # اگر جدول وجود ندارد، آن را ایجاد کن
        df.head(0).to_sql(table_name, engine, if_exists='fail', index=False)
    
    # ایمپورت داده‌ها
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',  # جایگزین با 'replace' برای بازنویسی جدول
        index=False
    )
    session.close()
    print(f"دیتا با موفقیت به جدول {table_name} اضافه شد!")