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

def add_year_column(cube_data):
    """
    Add a 'year' column to the cube data based on the 'month' column.

    Parameters:
        cube_data (pd.DataFrame): DataFrame containing the sales cube data.

    Returns:
        pd.DataFrame: DataFrame with an additional 'year' column.
    """
    try:
        logging.info("Adding 'year' column to the cube data...")
        cube_data["month"] = pd.to_datetime(cube_data["month"])
        cube_data["year"] = cube_data["month"].dt.year
        return cube_data
    except Exception as e:
        logging.error(f"Error while adding 'year' column: {e}")
        raise

def group_by_year(cube_data):
    """
    Group the cube data by year and calculate total sales.

    Parameters:
        cube_data (pd.DataFrame): DataFrame containing the sales cube data.

    Returns:
        pd.DataFrame: Aggregated DataFrame grouped by year.
    """
    try:
        logging.info("Grouping data by year...")
        return cube_data.groupby("year").agg(
            total_sales=("total_sales", "sum")
        ).reset_index()
    except Exception as e:
        logging.error(f"Error while grouping data by year: {e}")
        raise

def group_by_month(cube_data):
    """
    Group the cube data by month and calculate total sales.

    Parameters:
        cube_data (pd.DataFrame): DataFrame containing the sales cube data.

    Returns:
        pd.DataFrame: Aggregated DataFrame grouped by month.
    """
    try:
        logging.info("Grouping data by month...")
        return cube_data.groupby("month").agg(
            total_sales=("total_sales", "sum")
        ).reset_index()
    except Exception as e:
        logging.error(f"Error while grouping data by month: {e}")
        raise

def visualize_drilldown(yearly_data, monthly_data):
    """
    Create visualizations for yearly and monthly total sales.

    Parameters:
        yearly_data (pd.DataFrame): Aggregated DataFrame grouped by year.
        monthly_data (pd.DataFrame): Aggregated DataFrame grouped by month.
    """
    try:
        sns.set_theme(style="whitegrid")

        # Bar chart: Total sales by year
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=yearly_data,
            x="year",
            y="total_sales",
            color="blue"
        )
        plt.title("Total Sales by Year")
        plt.xlabel("Year")
        plt.ylabel("Total Sales")
        plt.tight_layout()
        yearly_chart_path = os.path.join(OUTPUT_DIR, "total_sales_by_year_bar.png")
        plt.savefig(yearly_chart_path)  # Save the yearly chart as an image
        logging.info(f"Saved yearly bar chart to {yearly_chart_path}")
        plt.show()

        # Line chart: Total sales by month
        plt.figure(figsize=(12, 6))
        sns.lineplot(
            data=monthly_data,
            x="month",
            y="total_sales",
            marker="o",
            color="green"
        )
        plt.title("Total Sales by Month")
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()
        monthly_chart_path = os.path.join(OUTPUT_DIR, "total_sales_by_month.png")
        plt.savefig(monthly_chart_path)  # Save the monthly chart as an image
        logging.info(f"Saved monthly chart to {monthly_chart_path}")
        plt.show()

    except Exception as e:
        logging.error(f"Error while visualizing drilldown data: {e}")
        raise

if __name__ == "__main__":
    try:
        logging.info("Starting drilldown analysis (year → month)...")

        # Load the cube data
        cube_data = load_cube_data(CUBE_PATH)

        # Add a 'year' column
        cube_data = add_year_column(cube_data)

        # Group data by year
        yearly_data = group_by_year(cube_data)

        # Group data by month
        monthly_data = group_by_month(cube_data)

        # Visualize the results
        visualize_drilldown(yearly_data, monthly_data)

        logging.info("Drilldown analysis (year → month) completed successfully.")
    except Exception as e:
        logging.error(f"Unexpected error in main execution: {e}")
        print(f"An error occurred: {e}")