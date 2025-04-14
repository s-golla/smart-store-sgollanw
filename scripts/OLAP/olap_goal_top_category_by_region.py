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

def get_top_categories_by_region(filtered_data):
    """
    Identify the top-performing product category in each region.

    Parameters:
        filtered_data (pd.DataFrame): Filtered DataFrame for the last year.

    Returns:
        pd.DataFrame: DataFrame containing the top product category for each region.
    """
    try:
        logging.info("Identifying top-performing product categories by region...")
        grouped_data = filtered_data.groupby(["region", "product_category"]).agg(
            total_sales=("total_sales", "sum")
        ).reset_index()

        # Get the top product category for each region
        top_categories = grouped_data.loc[grouped_data.groupby("region")["total_sales"].idxmax()]
        return top_categories
    except Exception as e:
        logging.error(f"Error while identifying top categories: {e}")
        raise

def visualize_top_categories(top_categories):
    """
    Create a visualization for the top-performing product categories by region.

    Parameters:
        top_categories (pd.DataFrame): DataFrame containing the top product category for each region.
    """
    try:
        sns.set_theme(style="whitegrid")

        # Bar chart: Top product category by region
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=top_categories,
            x="region",
            y="total_sales",
            hue="product_category",
            dodge=False,
            palette="muted"
        )
        plt.title("Top-Performing Product Category by Region (Last Year)")
        plt.xlabel("Region")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.legend(title="Product Category", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        chart_path = os.path.join(OUTPUT_DIR, "top_category_by_region.png")
        plt.savefig(chart_path)  # Save the chart as an image
        logging.info(f"Saved chart to {chart_path}")
        plt.show()

    except Exception as e:
        logging.error(f"Error while visualizing top categories: {e}")
        raise

if __name__ == "__main__":
    try:
        logging.info("Starting top product category by region analysis...")

        # Load the cube data
        cube_data = load_cube_data(CUBE_PATH)

        # Filter data for the last year
        filtered_data = filter_last_year_data(cube_data)

        # Identify the top product category for each region
        top_categories = get_top_categories_by_region(filtered_data)

        # Visualize the results
        visualize_top_categories(top_categories)

        logging.info("Top product category by region analysis completed successfully.")
    except Exception as e:
        logging.error(f"Unexpected error in main execution: {e}")
        print(f"An error occurred: {e}")