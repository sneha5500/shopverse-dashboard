import pandas as pd
from faker import Faker
import random

fake = Faker()

num_records = 10000

stores = ['S001', 'S002', 'S003']
payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'UPI']

data = []

for i in range(1, num_records + 1):
    order_date = fake.date_between(start_date='-1y', end_date='today')
    store = random.choice(stores)
    product_id = f"P{random.randint(100, 199)}"
    quantity = random.randint(1, 10)
    price = round(random.uniform(10, 1000), 2)
    total_amount = round(quantity * price, 2)
    payment_method = random.choice(payment_methods)

    data.append({
        'OrderID': i,
        'OrderDate': order_date,
        'StoreID': store,
        'ProductID': product_id,
        'Quantity': quantity,
        'Price': price,
        'TotalAmount': total_amount,
        'PaymentMethod': payment_method
    })

df = pd.DataFrame(data)
df.to_csv('raw_data/sales_data.csv', index=False)
print(f"✅ Generated {num_records} rows of raw retail sales data at ../raw_data/sales_data.csv")
