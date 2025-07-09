import sqlite3
import pandas as pd
import os

db_path = "/Users/snehagurram/retail_pipeline_project/retail_data.db"
output_dir = "/Users/snehagurram/retail_pipeline_project/outputs"

# Create outputs dir if missing
os.makedirs(output_dir, exist_ok=True)

conn = sqlite3.connect(db_path)
inventory_df = pd.read_sql_query("SELECT * FROM inventory", conn)
conn.close()

low_stock_df = inventory_df[inventory_df['StockQuantity'] < 10]

if not low_stock_df.empty:
    output_file = os.path.join(output_dir, "low_stock.csv")
    low_stock_df.to_csv(output_file, index=False)
    print(f"⚠️  Low stock items detected and saved to: {output_file}")
else:
    print("✅ No low stock items found.")

