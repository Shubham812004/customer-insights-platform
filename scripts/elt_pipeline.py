import pandas as pd
from sqlalchemy import create_engine, text
import os

DB_CONNECTION_STRING = 'postgresql://neondb_owner:npg_Ua1WefwBjS8i@ep-rapid-dawn-a1xln7hx-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'

RAW_DATA_DIR = os.path.join('data', 'raw')
BANK_CHURN_CSV = os.path.join(RAW_DATA_DIR, 'Churn_Modelling.csv')
OLIST_CUSTOMERS_CSV = os.path.join(RAW_DATA_DIR, 'olist_customers_dataset.csv')
OLIST_ORDERS_CSV = os.path.join(RAW_DATA_DIR, 'olist_orders_dataset.csv')
OLIST_PAYMENTS_CSV = os.path.join(RAW_DATA_DIR, 'olist_order_payments_dataset.csv')
TRANSFORM_SQL_PATH = os.path.join('scripts', 'transform.sql')


def load_csv_to_db(filepath, table_name, engine):
    """Loads a CSV file into a PostgreSQL 'staging' table."""
    if not os.path.exists(filepath):
        print(f"ERROR: File not found at {filepath}. Skipping.")
        return
    print(f"Loading {os.path.basename(filepath)} into table '{table_name}'...")
    df = pd.read_csv(filepath)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Successfully loaded {len(df)} rows.")

def run_elt():
    """
    Runs the full ELT pipeline for both Bank Churn and Olist datasets.
    """
    print("--- Starting Customer 360 ELT Pipeline ---")
    
    try:
        engine = create_engine(DB_CONNECTION_STRING)
        
        print("\n--- Phase 1: Loading all raw data into PostgreSQL ---")
        load_csv_to_db(BANK_CHURN_CSV, 'raw_bank_churn', engine)
        load_csv_to_db(OLIST_CUSTOMERS_CSV, 'raw_olist_customers', engine)
        load_csv_to_db(OLIST_ORDERS_CSV, 'raw_olist_orders', engine)
        load_csv_to_db(OLIST_PAYMENTS_CSV, 'raw_olist_order_payments', engine)
        
        print("\n--- Phase 2: Running SQL script to clean and transform all data ---")
        with open(TRANSFORM_SQL_PATH, 'r') as file:
            sql_script = file.read()
        
        with engine.connect() as connection:
            connection.execute(text(sql_script))
            connection.commit()
        
        print("SQL transformation script executed and committed successfully.")
        
        print("\n--- ELT Pipeline Completed Successfully! ---")

    except Exception as e:
        print(f"\n--- An error occurred during the ELT pipeline ---")
        print(e)

if __name__ == "__main__":
    run_elt()

