import sqlite3
import pandas as pd
import logging
import os

# Configure logging
LOG_FILE = "logs/project_log.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
DB_PATH = "data/dw/smart_sales.db"
CUBE_OUTPUT_PATH = "data/cube/sales_cube.csv"

def create_sales_cube():
    """
    Create a sales data cube by aggregating data from the SQLite database.

    The cube includes dimensions such as month, region, product category, and payment type,
    and metrics such as total sales and transaction count.

    The resulting cube is saved as a CSV file for reuse.

    Raises:
        FileNotFoundError: If the database file is not found.
        sqlite3.Error: If there is an issue executing the SQL query.
        Exception: For any other unexpected errors.
    """
    try:
        # Ensure the database file exists
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Database file not found at {DB_PATH}")

        # Connect to the SQLite database
        logging.info("Connecting to the SQLite database...")
        conn = sqlite3.connect(DB_PATH)

        # Define the SQL query to aggregate data
        query = """
        SELECT 
            strftime('%Y-%m', s.sale_date) AS month,
            c.region,
            p.category AS product_category,
            s.payment_type,
            SUM(s.sale_amount) AS total_sales,
            COUNT(*) AS transaction_count
        FROM sales s
        JOIN customers c ON s.customer_id = c.customer_id
        JOIN products p ON s.product_id = p.product_id
        GROUP BY month, c.region, p.category, s.payment_type
        """

        # Execute the query and load the data into a DataFrame
        logging.info("Executing the SQL query to create the sales cube...")
        cube_data = pd.read_sql_query(query, conn)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(CUBE_OUTPUT_PATH), exist_ok=True)

        # Save the cube to a CSV file
        logging.info(f"Saving the sales cube to {CUBE_OUTPUT_PATH}...")
        cube_data.to_csv(CUBE_OUTPUT_PATH, index=False)

        logging.info("Sales cube created and saved successfully.")

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        print(f"Error: {e}")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        print(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    logging.info("Starting the OLAP cubing process...")
    create_sales_cube()
    logging.info("OLAP cubing process completed.")