# smart-store-sgollanw
-----

## Project Setup Guide (1-Mac/Linux)

Run all commands from a terminal in the root project folder. 


### Step 1A - Create a Local Project Virtual Environment

```shell
python3 -m venv .venv
```

### Step 1B - Activate the Virtual Environment

```shell
source .venv/bin/activate
```

### Step 1C - Install Packages

```shell
python3 -m pip install --upgrade -r requirements.txt
```

### Step 1D - Optional: Verify .venv Setup

```shell
python3 -m datafun_venv_checker.venv_checker
```

### Step 1E - Run the initial project script

```shell
python3 scripts/data_prep.py
```

### Step 1F - Run the Data Preparation Scripts to cleanup the data

```shell
python3 scripts/data_preparation/prepare_customers_data.py
python3 scripts/data_preparation/prepare_products_data.py
python3 scripts/data_preparation/prepare_sales_data.py
```

-----

## Project Setup Guide (2-Windows)

Run all commands from a PowerShell terminal in the root project folder.

### Step 2A - Create a Local Project Virtual Environment

```shell
py -m venv .venv
```

### Step 2B - Activate the Virtual Environment

```shell
.venv\Scripts\activate
```

### Step 2C - Install Packages

```shell
py -m pip install --upgrade -r requirements.txt
```

### Step 2D - Optional: Verify .venv Setup

```shell
py -m datafun_venv_checker.venv_checker
```

### Step 2E - Run the initial project script

```shell
py scripts/data_prep.py
```

### Step 2F - Run the Data Preparation Scripts to cleanup the data

```shell
py scripts/data_preparation/prepare_customers_data.py
py scripts/data_preparation/prepare_products_data.py
py scripts/data_preparation/prepare_sales_data.py
```

-----


## Initial Package List (For Reference)

```
pip
setuptools
wheel
loguru
python-dotenv
pyttsx3
ipython
jupyter
ipykernel
ipywidgets
pandas
matplotlib
seaborn
```

## Commands Used (Frequently) to update GitHub 

```
# to check the status
git status
# to stage the files
git add .
# to commit with message
git commit -m "<<message to commit>>"
# to push into remote branch
git push -u origin main
```


-----


## Data warehouse Design


### Database Table Design

#### Customers Table

| Column Name              | Data Type | Constraints       | Description                          |
|--------------------------|-----------|-------------------|--------------------------------------|
| `customer_id`            | INTEGER   | PRIMARY KEY       | Unique identifier for each customer |
| `name`                   | TEXT      |                   | Name of the customer                |
| `region`                 | TEXT      |                   | Geographic region of the customer   |
| `join_date`              | TEXT      |                   | Date the customer joined            |
| `loyalty_points`         | INTEGER   |                   | Loyalty points earned by the customer |
| `preferred_contact_method` | TEXT    |                   | Preferred method of contact         |

#### Products Table

| Column Name      | Data Type | Constraints       | Description                          |
|------------------|-----------|-------------------|--------------------------------------|
| `product_id`     | INTEGER   | PRIMARY KEY       | Unique identifier for each product  |
| `product_name`   | TEXT      |                   | Name of the product                 |
| `category`       | TEXT      |                   | Category of the product             |
| `unit_price`     | REAL      |                   | Price per unit of the product       |
| `stock_quantity` | INTEGER   |                   | Quantity of product in stock        |
| `supplier`       | TEXT      |                   | Supplier of the product             |

#### Sales Table

| Column Name       | Data Type | Constraints                          | Description                          |
|-------------------|-----------|--------------------------------------|--------------------------------------|
| `transaction_id`  | INTEGER   | PRIMARY KEY                          | Unique identifier for each transaction |
| `sale_date`       | TEXT      |                                      | Date of the sale                     |
| `customer_id`     | INTEGER   | FOREIGN KEY REFERENCES `customers`   | ID of the customer making the purchase |
| `product_id`      | INTEGER   | FOREIGN KEY REFERENCES `products`    | ID of the product being purchased    |
| `store_id`        | INTEGER   |                                      | ID of the store where the sale occurred |
| `campaign_id`     | INTEGER   |                                      | ID of the marketing campaign         |
| `sale_amount`     | REAL      |                                      | Total amount of the sale             |
| `discount_percent`| INTEGER   |                                      | Discount percentage applied          |
| `payment_type`    | TEXT      |                                      | Payment method used                  |


**Relationships:**

```
`sales.customer_id` → References customers.customer_id.
`sales.product_id` → References products.product_id.
```

-----


### Load Data into the Data Warehouse

```shell
py scripts/etl_to_dw.py
```

-----

## SQL Queries and Reports

### SQL Queries
Below are some example SQL queries used to analyze the data in the data warehouse:

1. **Top 5 Customers by Loyalty Points**:
   ```sql
   SELECT name, loyalty_points
   FROM customers
   ORDER BY loyalty_points DESC
   LIMIT 5;
   ```

2. **Total Sales by Product**:
   ```sql
   SELECT p.product_name, SUM(s.sale_amount) AS total_sales
   FROM sales s
   JOIN products p ON s.product_id = p.product_id
   GROUP BY p.product_name
   ORDER BY total_sales DESC;
   ```

3. **Sales by Region**:
   ```sql
   SELECT c.region, SUM(s.sale_amount) AS total_sales
   FROM sales s
   JOIN customers c ON s.customer_id = c.customer_id
   GROUP BY c.region
   ORDER BY total_sales DESC;
   ```

4. **Payment Method Distribution**:
   ```sql
   SELECT payment_type, COUNT(*) AS transaction_count
   FROM sales
   GROUP BY payment_type;
   ```

### Reports
The SQL queries above were used to generate insights such as:
- Identifying the most loyal customers.
- Understanding which products generate the most revenue.
- Analyzing sales performance by region.
- Determining the most popular payment methods.

-----

## Dashboard Design

### Design Choices
The dashboard was designed with the following principles:
1. **Clarity**: Focused on presenting key metrics like total sales, top products, and customer loyalty in a clear and concise manner.
2. **Interactivity**: Included filters for regions, products, and time periods to allow dynamic exploration of the data.
3. **Visualization**: Used bar charts, pie charts, and line graphs to represent data trends and distributions effectively.

### Power BI Model View / Spark SQL Schema
Below is the Power BI Model View or Spark SQL Schema used to design the relationships between tables:

![Power BI Model View](images/model_view.jpg)

### Query Results
Here is a screenshot of the query results for "Total Sales by Product":

![Query Results](images/query_results.jpg)

### Final Dashboard / Charts
Below is the final dashboard showcasing key metrics and insights:

![Final Dashboard](images/final_dashboard.jpg)

-----

## Data Warehouse Sample Data Screenshots / Reference

**Customers data:**

![customers data table](images/customer_data.jpg)

**Products data:**

![products data table](images/products_data.jpg)

**Sales data:**

![sales data table](images/sales_data.jpg)

-----

# OLAP Module Summary

## Section 1: The Business Goal
The primary goal of this OLAP module is to analyze sales data to uncover actionable insights that can drive business decisions. The specific questions addressed include:
1. **Top-Performing Product Category by Region**: Which product categories generate the most revenue in each region?
2. **Payment Method Insights**: What are the most popular payment methods, and how do they contribute to total sales?
3. **Drilldown Analysis (Year → Month)**: How do sales trends vary from year-level to month-level granularity?
4. **Top-Performing Product Category by Region (Drilldown)**: How do regional preferences for product categories change over time?

These analyses are critical for optimizing inventory, tailoring marketing strategies, and improving customer satisfaction.

---

## Section 2: Data Source
The analysis was performed using a **pre-computed data cube** (`sales_cube.csv`) generated from the data warehouse. The cube aggregates data from the following tables:
1. **Customers Table**:
   - `region`: The geographic region of the customer.
2. **Products Table**:
   - `product_category`: The category of the product sold.
3. **Sales Table**:
   - `month`: The month of the transaction.
   - `payment_type`: The payment method used (e.g., Card, Cash).
   - `total_sales`: The total sales amount for the given combination of dimensions.
   - `transaction_count`: The number of transactions.

The cube was created using the `olap_cubing.py` script, which aggregates data by `month`, `region`, `product_category`, and `payment_type`.

---

## Section 3: Tools
The following tools were used for this project:
1. **Python**: For data processing, analysis, and visualization.
   - Libraries: `pandas`, `matplotlib`, `seaborn`, `logging`.
2. **SQLite**: To query the data warehouse and generate the data cube.
3. **Matplotlib & Seaborn**: For creating visualizations.
4. **VS Code**: For writing and debugging Python scripts.

These tools were chosen for their flexibility, ease of use, and ability to handle large datasets efficiently.

---

## Section 4: Workflow & Logic
### Dimensions and Aggregations:
1. **Dimensions**:
   - `region`, `product_category`, `payment_type`, `month`, `year`.
2. **Metrics**:
   - `total_sales`, `transaction_count`.
3. **Aggregations**:
   - Sum of `total_sales` and count of `transaction_count`.

### Workflow:
1. **Data Preparation**:
   - The `sales_cube.csv` file was generated using the `olap_cubing.py` script.
2. **Analysis**:
   - Filtered data for the last year.
   - Grouped data by relevant dimensions (e.g., `region`, `product_category`, `payment_type`).
   - Performed drilldown from year-level to month-level granularity.
3. **Visualization**:
   - Used bar charts, line charts, and pie charts to represent insights effectively.

---

## Section 5: Results
### Goal 1: Top-Performing Product Category by Region
- **Insights**:
  - **East**: Electronics dominated sales in the East region.
  - **North**: Clothing was the top-performing category.
  - **South**: Electronics generated the highest revenue.
  - **West**: Clothing performed best in this region.
- **Visualizations**:
  - **Bar chart**: Total sales by product category and region.
    ![Total sales by product category and region](images/total_sales_by_product_category.png)
  - **Line chart**: Monthly sales trends by product category.
    ![Monthly sales trends by product category](images/monthly_sales_trends_by_product_category.png)

### Goal 2: Payment Method Insights
- **Insights**:
  - Card payments accounted for the majority of total sales.
  - Cash payments had fewer transactions but were still significant in some regions.
- **Visualizations**:
  - **Pie Chart**: Contribution of payment methods to total sales.
    ![Payment Method Contribution](images/contribution_payment_methods.png)
  - **Bar Chart**: Transaction count by payment method.
    ![Transaction Count by Payment Method](images/transaction_count_payment_methods.png)

### Goal 3: Drilldown Analysis (Year → Month)
- **Insights**:
  - Yearly sales trends showed consistent growth over the last few years.
  - Monthly sales trends revealed seasonal spikes in specific months.
- **Visualizations**:
  - **Bar Chart**: Total sales by year.
    ![Total Sales by Year](images/total_sales_by_year_bar.png)
  - **Line Chart**: Total sales by month.
    ![Total Sales by Month](images/total_sales_by_month.png)

### Goal 4: Top-Performing Product Category by Region (Drilldown)
- **Insights**:
  - Electronics consistently performed well in the East and South regions.
  - Clothing was more popular in the North and West regions.
- **Visualization**:
  - **Bar Chart**: Top Product Categories by Region.
    ![Top Product Categories by Region](images/top_category_by_region.png)

---

## Section 6: Suggested Business Actions
1. **Inventory Management**:
   - Increase stock of Electronics in the East and South regions.
   - Focus on Clothing inventory in the North and West regions.
2. **Targeted Marketing**:
   - Run region-specific marketing campaigns highlighting the top-performing product categories.
   - Offer incentives for cash payments in regions where they are less common.
3. **Seasonal Planning**:
   - Plan inventory and staffing based on seasonal sales trends.
   - Focus marketing efforts during months with historically lower sales to boost revenue.

---

## Section 7: Challenges
1. **Data Cube Generation**:
   - **Challenge**: Ensuring the cube contained all necessary dimensions and metrics.
   - **Solution**: Used the `olap_cubing.py` script to pre-aggregate data from the data warehouse.

2. **Visualization**:
   - **Challenge**: Choosing the right visualization to represent the data.
   - **Solution**: Used bar charts, line charts, and pie charts to effectively communicate insights.

3. **Data Filtering**:
   - **Challenge**: Filtering the data for the last year while maintaining accuracy.
   - **Solution**: Used `pandas` to filter the data based on the `month` column.

---
