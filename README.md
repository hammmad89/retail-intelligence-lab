# Retail Intelligence Lab

### E-Commerce Sales & Customer Behavior Analysis

**A Data Analytics Portfolio Project by Ali Hammad**

Turning historical retail transactions into business insights using SQL, Python, and data visualization.

---
## Explore the Notebook

**[Open Retail Intelligence Lab in Google Colab](https://colab.research.google.com/drive/1zNr9_R6lUsp2N1MywZz9RpLjsM7tpbKY?usp=sharing)**

Open the notebook to explore the SQL queries, Python analysis, visualizations, and business recommendations.

## Project Overview

Retail Intelligence Lab explores an online retail transaction dataset to understand sales performance, product trends, customer purchasing behavior, and differences across markets.

The project demonstrates an end-to-end analytical workflow: querying transaction data with SQL, analyzing results using Python, visualizing patterns, and translating findings into business recommendations.

## Business Objectives

- Evaluate sales performance and monthly trends.
- Identify products with the highest recorded sales value.
- Analyze high-value customers and purchasing frequency.
- Segment customers by number of orders.
- Compare country-level sales and average invoice value.
- Recommend opportunities for further business investigation.

## Tech Stack

- **SQL & SQLite** — querying, aggregation, filtering, grouping, CTEs, and customer segmentation.
- **Python** — analysis and workflow development.
- **Pandas** — data loading, transformation, and result handling.
- **Matplotlib** — business-focused data visualizations.
- **Google Colab** — notebook development and execution.

## Dataset

**Online Retail — UCI Machine Learning Repository**

Source: [https://archive.ics.uci.edu/dataset/352/online+retail](https://archive.ics.uci.edu/dataset/352/online+retail)

The dataset contains historical transactions from a UK-based online retailer, including invoice identifiers, product codes, quantities, invoice dates, unit prices, customer identifiers, and countries.

The original dataset is provided by UCI. Please obtain it from the official source and follow its applicable terms.

## Analysis Performed

### 1. Executive Sales Snapshot

Calculated overall transaction value, sales invoices, identified customers, products sold, and average invoice value.

### 2. Data Quality Exploration

Investigated cancellation invoices, negative quantities, missing customer identifiers, and zero or negative prices.

### 3. Country-Level Sales

Compared transaction value, invoice counts, and identified customers across countries.

### 4. Product Performance

Ranked products by recorded sales value and examined units sold and invoice counts.

### 5. Monthly Sales Trends

Analyzed changes in transaction value over time to identify historical peaks and patterns for further investigation.

### 6. Customer Analysis

Ranked identified customers by purchase value and examined order frequency.

### 7. Customer Segmentation

Grouped customers into one-time, occasional, and frequent segments based on distinct order counts.

### 8. Average Invoice Value by Country

Compared average invoice values for countries with at least ten invoices.

## Visualizations

The notebook includes a themed set of visualizations covering:

- Executive sales KPIs
- Top countries by sales value
- Top products by sales value
- Monthly sales trends
- Highest-value customers
- Customer segment distribution
- Average invoice value by country

## Business Applications

The analysis can help businesses investigate:

- Which products contribute most to recorded sales value.
- Which markets have higher transaction volume.
- How purchase frequency differs among customers.
- Which months deserve further seasonal analysis.
- Where customer retention or product planning experiments may be worthwhile.

These are potential applications, not proof of causation or guaranteed business outcomes.

## How to Run the Project

1. Download the `Online Retail.xlsx` dataset from the official UCI source.
2. Open the notebook in Google Colab.
3. Upload the dataset when prompted, or update the file path to match your environment.
4. Run the setup cells in order to load the dataset, create the SQLite database, and execute the analyses.
5. Run the remaining cells to generate the tables, visualizations, and business report.

The notebook currently uses an in-memory SQLite database. Re-running the setup cells is necessary in a fresh session.

## Data & Methodology Notes

- Cancellation invoices are excluded from the positive-sales analyses.
- Transactions with nonpositive quantities or unit prices are excluded from those analyses.
- Customer-level analyses exclude rows without a customer identifier.
- Sales value is calculated as `Quantity × UnitPrice`.
- **Sales transaction value is not profit.** The dataset does not provide all costs required to calculate profitability.
- Customer segments are simple, project-defined categories based on order frequency.
- Findings describe the historical dataset and should be validated before real business decisions are made.

## Author

**Ali Hammad**
Data Analytics Portfolio Project

**Skills demonstrated:** SQL · Python · Pandas · Matplotlib · Data Quality Analysis · Customer Analytics · Business Storytelling

---

*From raw transactions to retail intelligence.*
