import sqlite3

db_path = "/Users/snehagurram/retail_pipeline_project/retail_data.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get all customers
cur.execute("SELECT CustomerID FROM customers")
customers = cur.fetchall()

# Update each with corresponding profile image
for customer in customers:
    cust_id = customer[0]
    img_filename = cust_id.replace("CUST", "c") + ".jpg"  # CUST0001 -> c0001.jpg

    cur.execute("""
        UPDATE customers
        SET ProfileImage = ?
        WHERE CustomerID = ?
    """, (img_filename, cust_id))

conn.commit()
conn.close()

print("✅ Profile images linked to all customers.")

