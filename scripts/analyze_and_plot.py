import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Paths setup
db_path = "/Users/snehagurram/retail_pipeline_project/retail_data.db"
base_dir = os.path.dirname(os.path.abspath(__file__))            # script folder
output_dir = os.path.join(base_dir, '..', 'outputs')             # ../outputs relative to script

# Create outputs folder if missing
os.makedirs(output_dir, exist_ok=True)

# Load data from SQLite
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM sales", conn)
conn.close()

df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# 1. Total sales by StoreID
store_sales = df.groupby('StoreID')['TotalAmount'].sum().sort_values(ascending=False)
plt.figure()
store_sales.plot(kind='bar', title='Total Sales by Store')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'total_sales_by_store.png'))
plt.close()

# 2. Monthly Sales Trend
monthly_sales = df.groupby(pd.Grouper(key='OrderDate', freq='ME'))['TotalAmount'].sum()
plt.figure(figsize=(10,5))
monthly_sales.plot(marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'monthly_sales_trend.png'))
plt.close()

# 3. Payment Method Distribution
payment_counts = df['PaymentMethod'].value_counts()
plt.figure(figsize=(7,7))
payment_counts.plot.pie(autopct='%1.1f%%', startangle=90, shadow=True)
plt.title('Payment Method Distribution')
plt.ylabel('')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'payment_method_distribution.png'))
plt.close()

# 4. Top 10 Products by Sales Revenue
top_products = df.groupby('ProductID')['TotalAmount'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
top_products.plot(kind='bar', color='orange')
plt.title('Top 10 Products by Sales Revenue')
plt.xlabel('Product ID')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_products_sales.png'))
plt.close()

print("✅ All charts saved in outputs/ folder, no popups this time.")

# 5. Store-wise Monthly Sales Charts
print("📊 Generating monthly charts per store...")

stores = df['StoreID'].unique()
for store in stores:
    store_df = df[df['StoreID'] == store]
    monthly_store_sales = store_df.groupby(pd.Grouper(key='OrderDate', freq='ME'))['TotalAmount'].sum()
    
    plt.figure(figsize=(10,5))
    monthly_store_sales.plot(marker='o')
    plt.title(f'Monthly Sales Trend - {store}')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"monthly_sales_{store}.png"))
    plt.close()
