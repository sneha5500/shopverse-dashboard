import sqlite3
from pathlib import Path

db_path = f"{str(Path.home())}/retail_pipeline_project/retail_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 1: Get quantity sold per product
cursor.execute("""
    SELECT ProductID, SUM(Quantity) as TotalSold
    FROM sales
    GROUP BY ProductID
""")
sales_data = cursor.fetchall()

# Step 2: Update inventory
for product_id, sold_qty in sales_data:
    cursor.execute("""
        UPDATE inventory
        SET StockQuantity = StockQuantity - ?
        WHERE ProductID = ?
    """, (sold_qty, product_id))

conn.commit()
conn.close()

print("✅ Inventory stock quantities updated based on sales.")
