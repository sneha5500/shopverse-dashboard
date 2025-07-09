import sqlite3

db_path = "/Users/snehagurram/retail_pipeline_project/retail_data.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Add ProfileImage column if not exists
cur.execute("ALTER TABLE customers ADD COLUMN ProfileImage TEXT")

conn.commit()
conn.close()

print("✅ ProfileImage column added to customers table.")

