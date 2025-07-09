import pandas as pd
import sqlite3
from pathlib import Path

# === Load CSV ===
csv_path = f"{str(Path.home())}/retail_pipeline_project/clean_data/sales_data_clean.csv"
df = pd.read_csv(csv_path)

print("Raw data preview:")
print(df.head())

# === Clean the data ===
df_clean = df.dropna(subset=['Quantity', 'UnitPrice'])

print("\nCleaned data preview:")
print(df_clean.head())

# === Save to SQLite DB ===
db_path = f"{str(Path.home())}/retail_pipeline_project/retail_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
df_clean.to_sql('sales', conn, if_exists='replace', index=False)
print(f"\n✅ Data loaded into SQLite DB at {db_path}")

# === Deduct inventory ===
print("\n📦 Updating inventory...")

for _, row in df_clean.iterrows():
    product_id = row['ProductID']
    qty_sold = int(row['Quantity'])

    cursor.execute("SELECT StockQuantity FROM inventory WHERE ProductID = ?", (product_id,))
    result = cursor.fetchone()

    if result:
        current_stock = result[0]
        new_stock = max(0, current_stock - qty_sold)
        cursor.execute("UPDATE inventory SET StockQuantity = ? WHERE ProductID = ?", (new_stock, product_id))

# === Detect Low Stock ===
low_stock_df = pd.read_sql_query("SELECT * FROM inventory WHERE StockQuantity <= 10", conn)
output_path = f"{str(Path.home())}/retail_pipeline_project/outputs/low_stock.csv"

if not low_stock_df.empty:
    low_stock_df.to_csv(output_path, index=False)
    print(f"⚠️  Low stock items detected and saved to: {output_path}")
else:
    print("✅ No low stock items detected.")

conn.commit()
conn.close()
