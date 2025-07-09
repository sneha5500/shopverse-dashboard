import sqlite3
import pandas as pd
import random

# DB path
db_path = "/Users/snehagurram/retail_pipeline_project/retail_data.db"

# Connect to SQLite DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get distinct ProductIDs from sales
sales_df = pd.read_sql_query("SELECT DISTINCT ProductID FROM sales", conn)

# Prepare inventory data with random low stock for some
inventory_data = []
for i, pid in enumerate(sales_df['ProductID']):
    product_name = f"Product {pid[-3:]}"
    
    if i % 7 == 0:  # every 7th product will be low-stock intentionally
        stock_qty = random.randint(1, 9)
    else:
        stock_qty = random.randint(20, 100)

    inventory_data.append((pid, product_name, stock_qty))

# Recreate inventory table
cursor.execute("DROP TABLE IF EXISTS inventory")
cursor.execute("""
    CREATE TABLE inventory (
        ProductID TEXT PRIMARY KEY,
        ProductName TEXT,
        StockQuantity INTEGER
    )
""")

# Insert data
cursor.executemany("INSERT INTO inventory (ProductID, ProductName, StockQuantity) VALUES (?, ?, ?)", inventory_data)
conn.commit()
conn.close()

print("✅ Inventory table re-initialized.")
print("⚠️  Some products set to low stock (<10) for testing low_stock report.")
