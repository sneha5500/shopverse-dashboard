import sqlite3

DB_PATH = "/Users/snehagurram/retail_pipeline_project/retail_data.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create returns table
cur.execute("""
CREATE TABLE IF NOT EXISTS returns (
    ReturnID TEXT PRIMARY KEY,
    CustomerID TEXT,
    OrderID TEXT,
    ProductID TEXT,
    ReturnReason TEXT,
    ReturnDate TEXT
);
""")

# Create refunds table
cur.execute("""
CREATE TABLE IF NOT EXISTS refunds (
    RefundID TEXT PRIMARY KEY,
    ReturnID TEXT,
    RefundAmount REAL,
    RefundDate TEXT,
    RefundMethod TEXT,
    FOREIGN KEY (ReturnID) REFERENCES returns(ReturnID)
);
""")

conn.commit()
conn.close()

print("✅ Returns and Refunds tables created successfully.")
