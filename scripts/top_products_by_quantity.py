import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Paths
db_path = os.path.expanduser("~/retail_pipeline_project/retail_data.db")
output_dir = os.path.expanduser("~/retail_pipeline_project/outputs")
os.makedirs(output_dir, exist_ok=True)

# Load data
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM sales", conn)
conn.close()
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# Top 10 most sold products by quantity
top_quantity_products = df.groupby('ProductID')['Quantity'].sum().sort_values(ascending=False).head(10)

# Plot
plt.figure(figsize=(10, 5))
top_quantity_products.plot(kind='bar', color='green')
plt.title("Top 10 Most Sold Products (by Quantity)")
plt.xlabel("Product ID")
plt.ylabel("Total Quantity Sold")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top_products_by_quantity.png"))
plt.close()

print("✅ Chart saved: top_products_by_quantity.png")
