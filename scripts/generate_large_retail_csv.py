import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path

fake = Faker()
Faker.seed(42)
random.seed(42)

rows = 10000  # you can make this 100000 later if needed
categories = ["Electronics", "Clothing", "Grocery", "Home Decor", "Sports", "Beauty"]
payment_methods = ["Credit Card", "Cash", "UPI", "Debit Card", "Net Banking"]
stores = ["S001", "S002", "S003", "S004"]

data = []

start_date = datetime(2024, 1, 1)

for i in range(1, rows + 1):
    order_date = start_date + timedelta(days=random.randint(0, 365))
    store_id = random.choice(stores)
    product_id = f"P{random.randint(100, 199)}"
    customer_id = f"C{random.randint(1000, 1999)}"
    category = random.choice(categories)
    quantity = random.randint(1, 10)
    unit_price = round(random.uniform(5, 1500), 2)
    total_amount = round(quantity * unit_price, 2)
    payment = random.choice(payment_methods)
    
    data.append([
        i, order_date.strftime("%Y-%m-%d"), store_id, product_id, customer_id,
        category, quantity, unit_price, total_amount, payment
    ])

df = pd.DataFrame(data, columns=[
    "OrderID", "OrderDate", "StoreID", "ProductID", "CustomerID", "ProductCategory",
    "Quantity", "UnitPrice", "TotalAmount", "PaymentMethod"
])

# Save CSV file
output_path = f"{str(Path.home())}/retail_pipeline_project/raw_data/sales_data.csv"
df.to_csv(output_path, index=False)
print(f"✅ Generated {rows} rows of sample retail data at {output_path}")
