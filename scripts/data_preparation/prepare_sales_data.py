import sys
from pathlib import Path

########################################
# Utilities
########################################

def add_parent_dir_to_sys_path(levels_up: int = 2) -> None:
    """Adds the parent directory (a specified number of levels up) to sys.path."""
    parent_dir = Path(__file__).resolve().parents[levels_up]
    sys.path.append(str(parent_dir))

add_parent_dir_to_sys_path()

from utils.logger import logger  # Import after updating sys.path
import pandas as pd
import os

########################################
# Column Validation
########################################

def verify_columns(df: pd.DataFrame, expected_columns: dict) -> bool:
    """
    Validates the DataFrame's columns and their data types.
    """
    logger.info("Verifying columns and data types...")
    
    # Check the column count
    if set(expected_columns.keys()) != set(df.columns):
        logger.error(f"Column mismatch. Expected: {list(expected_columns.keys())}, Found: {list(df.columns)}")
        return False
    
    # Check data types
    for col, expected_type in expected_columns.items():
        actual_type = df[col].dtype.name
        if actual_type != expected_type:
            logger.error(f"Column {col}: Expected {expected_type}, Found {actual_type}")
            return False

    logger.info("Column validation succeeded.")
    return True

########################################
# Data Cleaning
########################################

def clean_dataframe(df: pd.DataFrame, allowed_payment_types: list = ["Card", "Cash"]) -> pd.DataFrame:
    """
    Cleans the DataFrame by removing duplicates and filtering out sales data based on PaymentType.
    """
    df = df.drop_duplicates()
    logger.info("Removed duplicates.")
    
    # Filter rows based on allowed payment types
    df = df[df['PaymentType'].isin(allowed_payment_types)]
    logger.info(f"Filtered sales data to include only allowed PaymentTypes: {allowed_payment_types}.")
    
    return df

########################################
# Main Execution
########################################

def process_data(input_file: str, output_file: str, expected_columns: dict) -> None:
    """
    Processes the raw customer data, validates it, cleans it, and saves the prepared data.
    """
    try:
        df = pd.read_csv(input_file)
        df["SaleDate"] = pd.to_datetime(df["SaleDate"])
        logger.info("Loaded and preprocessed raw data.")
        
        if verify_columns(df, expected_columns):
            cleaned_df = clean_dataframe(df)
            output_path = Path(output_file).parent
            output_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
            cleaned_df.to_csv(output_file, index=False)
            logger.info(f"Prepared data saved to {output_file}")
        else:
            logger.error("Validation failed. Exiting process.")
    except FileNotFoundError:
        logger.error(f"File {input_file} not found.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    logger.info("Starting the data preparation process...")

    input_filepath = "data/raw/sales_data.csv"
    output_filepath = "data/prepared/sales_data_prepared.csv"
    expected_columns = {
            "TransactionID": "int64",
            "SaleDate": "datetime64[ns]",
            "ProductID": "int64",
            "StoreID": "int64",
            "CustomerID": "int64",
            "CampaignID": "int64",
            "SaleAmount": "float64",
            "DiscountPercent": "int64",
            "PaymentType": "object",
        }

    process_data(input_filepath, output_filepath, expected_columns)
    logger.info("Data preparation completed.")
