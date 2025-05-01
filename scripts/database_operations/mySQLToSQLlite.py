import pandas as pd
from sqlalchemy import create_engine

# ---------------------------
# اتصال به MySQL (منبع)
# ---------------------------
mysql_engine = create_engine("mysql+pymysql://Mosiyo:1383@172.29.143.138:3306/DataScience_DB")

# ---------------------------
# اتصال به SQLite (مقصد)
# ---------------------------
sqlite_engine = create_engine('sqlite:///database.db')

# ---------------------------
# لیست جداول موجود در MySQL
# ---------------------------
tables = ['Misconceptions', 'Questions', 'Answers']

# ---------------------------
# انتقال دادهها
# ---------------------------
for table in tables:
    # خواندن داده از MySQL
    df = pd.read_sql_table(table, mysql_engine)
    
    # نوشتن داده در SQLite
    df.to_sql(
        name=table,
        con=sqlite_engine,
        if_exists='replace',
        index=False
    )
    print(f"✅ Table {table} exported to SQLite!")

print("🎉 All data migrated to database.db!")