import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = PROJECT_ROOT.joinpath("data", "dw")
DB_PATH = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR = PROJECT_ROOT.joinpath("data", "prepared")
SQL_FILE_PATH = PROJECT_ROOT.joinpath("sql", "dw_tables.sql")  # Path to SQL file

def create_schema_from_file(cursor: sqlite3.Cursor) -> None:
    """
    Create tables in the data warehouse by reading SQL from a file.

    Parameters:
        cursor (sqlite3.Cursor): SQLite cursor to execute SQL commands.
    """
    try:
        with open(SQL_FILE_PATH, 'r') as file:  # to read dw_tables.sql
            sql_script = file.read()
            cursor.executescript(sql_script)
    except FileNotFoundError:
        print(f"Error: SQL file not found at {SQL_FILE_PATH}")
        raise
    except Exception as e:
        print(f"Error while creating schema: {e}")
        raise

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """
    Delete all existing records from the customers, products, and sales tables.

    Parameters:
        cursor (sqlite3.Cursor): SQLite cursor to execute SQL commands.
    """
    try:
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM sales")
    except Exception as e:
        print(f"Error while deleting existing records: {e}")
        raise

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """
    Insert customer data into the customers table.

    Parameters:
        customers_df (pd.DataFrame): DataFrame containing customer data.
        cursor (sqlite3.Cursor): SQLite cursor to execute SQL commands.
    """
    try:
        # Rename columns to match the database schema
        customers_df = customers_df.rename(columns={
            "CustomerID": "customer_id",
            "Name": "name",
            "Region": "region",
            "JoinDate": "join_date",
            "LoyaltyPoints": "loyalty_points",
            "PreferredContactMethod": "preferred_contact_method"
        })
        customers_df.to_sql("customers", cursor.connection, if_exists="append", index=False)
    except Exception as e:
        print(f"Error while inserting customers: {e}")
        raise

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """
    Insert product data into the products table.

    Parameters:
        products_df (pd.DataFrame): DataFrame containing product data.
        cursor (sqlite3.Cursor): SQLite cursor to execute SQL commands.
    """
    try:
        # Rename columns to match the database schema
        products_df = products_df.rename(columns={
            "ProductID": "product_id",
            "ProductName": "product_name",
            "Category": "category",
            "UnitPrice": "unit_price",
            "StockQuantity": "stock_quantity",
            "Supplier": "supplier"
        })
        products_df.to_sql("products", cursor.connection, if_exists="append", index=False)
    except Exception as e:
        print(f"Error while inserting products: {e}")
        raise

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """
    Insert sales data into the sales table.

    Parameters:
        sales_df (pd.DataFrame): DataFrame containing sales data.
        cursor (sqlite3.Cursor): SQLite cursor to execute SQL commands.
    """
    try:
        # Rename columns to match the database schema
        sales_df = sales_df.rename(columns={
            "TransactionID": "transaction_id",
            "SaleDate": "sale_date",
            "CustomerID": "customer_id",
            "ProductID": "product_id",
            "StoreID": "store_id",
            "CampaignID": "campaign_id",
            "SaleAmount": "sale_amount",
            "DiscountPercent": "discount_percent",
            "PaymentType": "payment_type"
        })
        sales_df.to_sql("sales", cursor.connection, if_exists="append", index=False)
    except Exception as e:
        print(f"Error while inserting sales: {e}")
        raise

def load_data_to_db() -> None:
    """
    Load prepared data into the SQLite database.

    Steps:
        1. Create the database schema by reading the SQL file.
        2. Delete existing records from the tables.
        3. Load prepared data from CSV files.
        4. Insert the data into the respective tables.
    """
    conn = None
    try:
        # Ensure the data warehouse directory exists
        DW_DIR.mkdir(parents=True, exist_ok=True)

        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema_from_file(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_data_prepared.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_data_prepared.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv"))

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        # Commit the transaction
        conn.commit()
        print("Data successfully loaded into the database.")
    except Exception as e:
        print(f"Error during ETL process: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()