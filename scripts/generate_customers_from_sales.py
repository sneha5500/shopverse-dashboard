import sqlite3
import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker("en_IN")
db_path = str(Path.home() / "retail_pipeline_project/retail_data.db")
conn = sqlite3.connect(db_path)

# Load sales
sales_df = pd.read_sql("SELECT * FROM sales", conn)

# Aggregate spend per customer
agg = sales_df.groupby('CustomerID')['TotalAmount'].agg(['sum', 'count']).reset_index()
agg.columns = ['CustomerID', 'TotalSpend', 'TotalOrders']

# Generate realistic customer info
customers = []
for idx, row in agg.iterrows():
    customer_id = row['CustomerID']
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    join_date = fake.date_between(start_date='-2y', end_date='today')
    total_spend = round(row['TotalSpend'], 2)
    loyalty_points = int(total_spend * 0.05)
    
    # Tier based on spend
    if total_spend > 20000:
        tier = 'Platinum'
    elif total_spend > 10000:
        tier = 'Gold'
    elif total_spend > 5000:
        tier = 'Silver'
    else:
        tier = 'Bronze'
    
    img_path = f"profile_{customer_id}.jpg"
    
    customers.append([customer_id, name, email, phone, join_date, total_spend, loyalty_points, tier, img_path])

# Convert to DF and save to DB
customers_df = pd.DataFrame(customers, columns=[
    'CustomerID', 'CustomerName', 'Email', 'Phone',
    'JoinDate', 'TotalSpend', 'LoyaltyPoints', 'Tier', 'ProfileImagePath'
])

customers_df.to_sql('customers', conn, if_exists='replace', index=False)
conn.close()

print(f"✅ {len(customers_df)} customers generated and saved to DB.")
