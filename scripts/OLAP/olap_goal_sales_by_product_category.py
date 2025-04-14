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

def visualize_sales_by_category(filtered_data):
    """
    Create visualizations for sales by product category, month, and region.

    Parameters:
        filtered_data (pd.DataFrame): Filtered DataFrame for the last year.
    """
    try:
        sns.set_theme(style="whitegrid")

        # Bar chart: Total sales by product category and region
        plt.figure(figsize=(12, 6))
        sns.barplot(
            data=filtered_data,
            x="product_category",
            y="total_sales",
            hue="region",
            errorbar=None
        )
        plt.title("Total Sales by Product Category and Region (Last Year)")
        plt.xlabel("Product Category")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.legend(title="Region")
        plt.tight_layout()
        bar_chart_path = os.path.join(OUTPUT_DIR, "total_sales_by_product_category.png")
        plt.savefig(bar_chart_path)  # Save the bar chart as an image
        logging.info(f"Saved bar chart to {bar_chart_path}")
        plt.show()

        # Line chart: Monthly sales trends by product category
        plt.figure(figsize=(12, 6))
        sns.lineplot(
            data=filtered_data,
            x="month",
            y="total_sales",
            hue="product_category",
            marker="o"
        )
        plt.title("Monthly Sales Trends by Product Category (Last Year)")
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.legend(title="Product Category")
        plt.tight_layout()
        line_chart_path = os.path.join(OUTPUT_DIR, "monthly_sales_trends_by_product_category.png")
        plt.savefig(line_chart_path)  # Save the line chart as an image
        logging.info(f"Saved line chart to {line_chart_path}")
        plt.show()

    except Exception as e:
        logging.error(f"Error while visualizing sales by category: {e}")
        raise

if __name__ == "__main__":
    try:
        logging.info("Starting sales by product category analysis...")

        # Load the cube data
        cube_data = load_cube_data(CUBE_PATH)

        # Filter data for the last year
        filtered_data = filter_last_year_data(cube_data)

        # Visualize the results
        visualize_sales_by_category(filtered_data)

        logging.info("Sales by product category analysis completed successfully.")
    except Exception as e:
        logging.error(f"Unexpected error in main execution: {e}")
        print(f"An error occurred: {e}")