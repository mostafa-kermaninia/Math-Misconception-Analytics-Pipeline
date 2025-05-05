import pandas as pd
from sqlalchemy import create_engine
from scripts.database_connection import get_db_engine

def import_dataframe(df):
    """Import dataframe data into the database."""
    df.to_sql(name="Dataset", con=get_db_engine(), if_exists="append", index=False)
    print("✅ Dataset imported!")
