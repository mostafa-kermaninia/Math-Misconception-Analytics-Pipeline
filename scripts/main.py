from load_data import load_clean_data
from import_to_db import import_data

if __name__ == "__main__":
    # لود داده تمیز شده
    df = load_clean_data()
    
    # ایمپورت به دیتابیس (نام جدول را تنظیم کنید)
    import_data(df, table_name='questions')