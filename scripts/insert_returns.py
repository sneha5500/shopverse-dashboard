import sqlite3
from datetime import datetime, timedelta
import random
from pathlib import Path

# === CONFIG ===
DB_PATH = str(Path.home() / "retail_pipeline_project" / "retail_data.db")
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# === CLEAN OLD DATA ===
cur.execute("DELETE FROM returns")
cur.execute("DELETE FROM refunds")

# === SAMPLE DATA ===
customer_ids = [f"C10{i}" for i in range(10)]
order_ids = [f"O10{i}" for i in range(10)]
product_ids = [f"P10{i}" for i in range(10)]
reasons = ["Defective", "Wrong Item", "Not Needed", "Late Delivery", "Changed Mind"]
methods = ["Card", "Cash", "Store Credit"]

# === INSERT RETURNS + REFUNDS ===
for i in range(1, 11):
    customer = random.choice(customer_ids)
    order = random.choice(order_ids)
    product = random.choice(product_ids)
    reason = random.choice(reasons)
    return_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")

    cur.execute(
        "INSERT INTO returns (ReturnID, CustomerID, OrderID, ProductID, Reason, ReturnDate) VALUES (?, ?, ?, ?, ?, ?)",
        (i, customer, order, product, reason, return_date)
    )

    amount = round(random.uniform(10, 200), 2)
    method = random.choice(methods)
    refund_date = (datetime.now() - timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d")

    cur.execute(
        "INSERT INTO refunds (RefundID, ReturnID, Amount, Method, RefundDate) VALUES (?, ?, ?, ?, ?)",
        (i, i, amount, method, refund_date)
    )

conn.commit()
conn.close()

print("✅ 10 Dummy returns and refunds inserted into:", DB_PATH)
