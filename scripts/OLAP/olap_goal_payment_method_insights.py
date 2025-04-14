import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
CUBE_PATH = "data/cube/sales_cube.csv"
OUTPUT_DIR = "images"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_cube_data(cube_path):
    """
    Load the prebuilt sales cube from a CSV file.

    Parameters:
        cube_path (str): Path to the sales cube CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the sales cube data.

    Raises:
        FileNotFoundError: If the cube file is not found.
        Exception: For any other unexpected errors.
    """
    try:
        logging.info(f"Loading sales cube from {cube_path}...")
        return pd.read_csv(cube_path)
    except FileNotFoundError as e:
        logging.error(f"Cube file not found: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error while loading cube: {e}")
        raise

def filter_last_year_data(cube_data):
    """
    Filter the sales cube data for the last year.

    Parameters:
        cube_data (pd.DataFrame): DataFrame containing the sales cube data.

    Returns:
        pd.DataFrame: Filtered DataFrame for the last year.
    """
    try:
        logging.info("Filtering data for the last year...")
        cube_data["month"] = pd.to_datetime(cube_data["month"])
        last_year = cube_data["month"].max() - pd.DateOffset(years=1)
        return cube_data[cube_data["month"] > last_year]
    except Exception as e:
        logging.error(f"Error while filtering data: {e}")
        raise

def group_by_payment_type(filtered_data):
    """
    Group the filtered data by payment type and calculate metrics.

    Parameters:
        filtered_data (pd.DataFrame): Filtered DataFrame for the last year.

    Returns:
        pd.DataFrame: Aggregated DataFrame grouped by payment type.
    """
    try:
        logging.info("Grouping data by payment type...")
        return filtered_data.groupby("payment_type").agg(
            total_sales=("total_sales", "sum"),
            transaction_count=("transaction_count", "sum")
        ).reset_index()
    except Exception as e:
        logging.error(f"Error while grouping data: {e}")
        raise

def visualize_payment_methods(payment_data):
    """
    Create visualizations for payment methods and their contribution to total sales.

    Parameters:
        payment_data (pd.DataFrame): Aggregated DataFrame grouped by payment type.
    """
    try:
        sns.set_theme(style="whitegrid")

        # Pie chart: Contribution of payment methods to total sales
        plt.figure(figsize=(8, 8))
        plt.pie(
            payment_data["total_sales"],
            labels=payment_data["payment_type"],
            autopct='%1.1f%%',
            startangle=140,
            colors=sns.color_palette("pastel")
        )
        plt.title("Contribution of Payment Methods to Total Sales (Last Year)")
        plt.tight_layout()
        pie_chart_path = os.path.join(OUTPUT_DIR, "contribution_payment_methods.png")
        plt.savefig(pie_chart_path)  # Save the pie chart as an image
        logging.info(f"Saved pie chart to {pie_chart_path}")
        plt.show()

        # Horizontal bar chart: Transaction count by payment method
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=payment_data,
            y="payment_type",
            x="transaction_count",
            hue="payment_type",  # Assign the `payment_type` column to `hue`
            dodge=False,         # Ensure bars are not split by hue
            palette="muted",
            legend=False         # Disable the legend since `hue` is used only for color
        )
        plt.title("Transaction Count by Payment Method (Last Year)")
        plt.xlabel("Transaction Count")
        plt.ylabel("Payment Method")
        plt.tight_layout()
        bar_chart_path = os.path.join(OUTPUT_DIR, "transaction_count_payment_methods.png")
        plt.savefig(bar_chart_path)  # Save the bar chart as an image
        logging.info(f"Saved bar chart to {bar_chart_path}")
        plt.show()

    except Exception as e:
        logging.error(f"Error while visualizing payment methods: {e}")
        raise

if __name__ == "__main__":
    try:
        logging.info("Starting payment method insights analysis...")

        # Load the cube data
        cube_data = load_cube_data(CUBE_PATH)

        # Filter data for the last year
        filtered_data = filter_last_year_data(cube_data)

        # Group data by payment type
        payment_data = group_by_payment_type(filtered_data)

        # Visualize the results
        visualize_payment_methods(payment_data)

        logging.info("Payment method insights analysis completed successfully.")
    except Exception as e:
        logging.error(f"Unexpected error in main execution: {e}")
        print(f"An error occurred: {e}")