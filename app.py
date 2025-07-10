import streamlit as st
import pandas as pd
import sqlite3
import base64
from datetime import datetime
from pathlib import Path

# === CONFIG ===
DB_PATH = str(Path.home() / "retail_pipeline_project" / "retail_data.db")
LOGO_PATH = str(Path.home() / "retail_pipeline_project" / "assets" / "logo.png")

# === UTILS ===
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64_image(LOGO_PATH)

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    sales_df = pd.read_sql("SELECT * FROM sales", conn)
    inventory_df = pd.read_sql("SELECT * FROM inventory", conn)
    customers_df = pd.read_sql("SELECT * FROM customers", conn)
    conn.close()
    
    sales_df["OrderDate"] = pd.to_datetime(sales_df["OrderDate"])
    return sales_df, inventory_df, customers_df

sales_df, inv_df, cust_df = load_data()

# === SIDEBAR ===
st.sidebar.image(f"data:image/png;base64,{logo_base64}", width=120)
st.sidebar.title("🛒 ShopVerse™")
section = st.sidebar.radio("Navigate", [
    "Welcome",
    "Home", 
    "Store Analytics", 
    "Product Tracker", 
    "Inventory Overview", 
    "Customer CRM",
    "Gold Members",
    "Silver Members",
    "Platinum Members",
    "Product Returns"
])

# === SECTION: WELCOME PAGE ===
if section == "Welcome":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 46px;'>Welcome to <span style='color:#1DB954;'>ShopVerse™</span></h1>", unsafe_allow_html=True)
    st.markdown("<h4>Your all-in-one platform for retail data insights,<br>customer tracking, inventory intelligence, and more.</h4>", unsafe_allow_html=True)

# === SECTION: HOME ===
elif section == "Home":
    st.header("✨ Executive Summary")
    total_sales = sales_df["TotalAmount"].sum()
    total_orders = sales_df["OrderID"].nunique()
    top_store = sales_df.groupby("StoreID")["TotalAmount"].sum().idxmax()
    top_product = sales_df.groupby("ProductID")["TotalAmount"].sum().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    col2.metric("📦 Orders", total_orders)
    col3.metric("🏪 Top Store", top_store)
    col4.metric("⭐ Top Product", top_product)

    st.markdown("---")
    st.subheader("📈 Monthly Sales Trend")
    monthly_sales = sales_df.groupby(pd.Grouper(key="OrderDate", freq="M"))["TotalAmount"].sum()
    st.line_chart(monthly_sales)

# === SECTION: STORE ANALYTICS ===
elif section == "Store Analytics":
    st.header("🏪 Store-wise Analytics")
    selected_store = st.selectbox("Choose a Store", sales_df["StoreID"].unique())
    filtered_df = sales_df[sales_df["StoreID"] == selected_store]

    st.subheader(f"📈 Monthly Sales - {selected_store}")
    monthly = filtered_df.groupby(pd.Grouper(key="OrderDate", freq="M"))["TotalAmount"].sum()
    st.line_chart(monthly)

    st.subheader("💳 Payment Method Breakdown")
    st.bar_chart(filtered_df["PaymentMethod"].value_counts())

    st.subheader("🔥 Top 5 Products by Revenue")
    top5 = filtered_df.groupby("ProductID")["TotalAmount"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top5)

# === SECTION: PRODUCT TRACKER ===
elif section == "Product Tracker":
    st.header("🔍 Product Sales Tracker")
    product_id = st.selectbox("Search Product ID", sales_df["ProductID"].unique())
    product_sales = sales_df[sales_df["ProductID"] == product_id]

    st.write(f"💰 Total Sales: ${product_sales['TotalAmount'].sum():,.2f}")
    st.write(f"📦 Total Orders: {product_sales.shape[0]}")

    st.subheader("📈 Monthly Sales Trend")
    product_monthly = product_sales.groupby(pd.Grouper(key="OrderDate", freq="M"))["TotalAmount"].sum()
    st.line_chart(product_monthly)

    st.subheader("🏬 Store-wise Sales")
    st.bar_chart(product_sales.groupby("StoreID")["TotalAmount"].sum())

# === SECTION: INVENTORY ===
elif section == "Inventory Overview":
    st.header("📦 Inventory Monitoring")
    st.dataframe(inv_df)

    st.subheader("⚠️ Low Stock Items (Below 10)")
    low_stock = inv_df[inv_df["StockQuantity"] < 10]
    st.dataframe(low_stock)

    if not low_stock.empty:
        st.download_button(
            label="📥 Download Low Stock Report",
            data=low_stock.to_csv(index=False),
            file_name="low_stock.csv",
            mime="text/csv"
        )

    st.subheader("📊 Inventory Levels by Product")
    st.bar_chart(inv_df.set_index("ProductID")["StockQuantity"])

# === SECTION: CUSTOMER CRM ===
elif section == "Customer CRM":
    st.header("🧑‍💼 Customer Profiles & Loyalty Insights")
    customer_ids = cust_df["CustomerID"].unique()
    selected_customer = st.selectbox("Choose a Customer ID", customer_ids)
    cust_data = cust_df[cust_df["CustomerID"] == selected_customer].iloc[0]

    st.subheader(f"🧾 Profile: {selected_customer}")
    profile_col1, profile_col2 = st.columns([1, 3])
    img_path = f"./assets/profiles/{cust_data['ProfileImage']}"
    profile_col1.image(img_path, width=100)
    profile_col2.markdown(f"""
        **Name:** {cust_data['CustomerName']}  
        **Email:** {cust_data['Email']}  
        **Loyalty Level:** {cust_data['Tier']}  
        **Total Spend:** ${cust_data['TotalSpend']:,.2f}
    """)

    st.subheader("🛍️ Purchase History")
    purchase_history = sales_df[sales_df["CustomerID"] == selected_customer]
    st.dataframe(purchase_history.sort_values("OrderDate", ascending=False))

    st.subheader("📈 Purchase Trend")
    trend = purchase_history.groupby(pd.Grouper(key="OrderDate", freq="M"))["TotalAmount"].sum()
    st.line_chart(trend)

    st.markdown("---")
    st.subheader("🏆 Loyalty Rewards Dashboard")

    tier_filter = st.selectbox("Select Loyalty Tier", ["All", "Gold", "Silver", "Platinum"])
    filtered_cust = cust_df if tier_filter == "All" else cust_df[cust_df["Tier"] == tier_filter]

    st.write(f"Showing **{filtered_cust.shape[0]}** customers in tier: **{tier_filter}**")

    rewards_cols = st.columns([2, 2, 2, 2])
    rewards_cols[0].metric("Gold Members", cust_df[cust_df["Tier"] == "Gold"].shape[0])
    rewards_cols[1].metric("Silver Members", cust_df[cust_df["Tier"] == "Silver"].shape[0])
    rewards_cols[2].metric("Platinum Members", cust_df[cust_df["Tier"] == "Platinum"].shape[0])
    rewards_cols[3].metric("Total Customers", cust_df.shape[0])

    st.dataframe(
        filtered_cust[["CustomerID", "CustomerName", "Email", "Tier", "TotalSpend", "LoyaltyPoints"]]
        .sort_values("TotalSpend", ascending=False)
    )

# === LOYALTY FILTERS ===
elif section in ["Gold Members", "Silver Members", "Platinum Members"]:
    tier = section.split()[0]
    st.header(f"🏷️ {tier} Loyalty Customers")
    tier_customers = cust_df[cust_df["Tier"].str.lower() == tier.lower()]

    if tier_customers.empty:
        st.warning(f"No {tier} customers found.")
    else:
        for _, row in tier_customers.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 5])
                img_path = f"./assets/profiles/{row['ProfileImage']}"
                col1.image(img_path, width=60)
                col2.markdown(f"""
                    **{row['CustomerName']}**  
                    📧 {row['Email']}  
                    💰 Total Spend: ${row['TotalSpend']:,.2f}
                """)
                st.markdown("---")

# === SECTION: PRODUCT RETURNS ===
elif section == "Product Returns":
    st.header("↩️ Product Returns & Refunds")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables if they don't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            ReturnID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID TEXT,
            OrderID TEXT,
            ProductID TEXT,
            Reason TEXT,
            ReturnDate TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS refunds (
            RefundID INTEGER PRIMARY KEY AUTOINCREMENT,
            ReturnID INTEGER,
            Amount REAL,
            Method TEXT,
            RefundDate TEXT,
            FOREIGN KEY (ReturnID) REFERENCES returns(ReturnID)
        )
    """)
    conn.commit()

    st.subheader("📋 Log a Product Return")
    with st.form("return_form"):
        customer_id = st.selectbox("Customer ID", cust_df["CustomerID"].unique())
        order_id = st.text_input("Order ID")
        product_id = st.text_input("Product ID")
        reason = st.text_area("Reason for Return")
        submitted = st.form_submit_button("Submit Return")

        if submitted:
            return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("INSERT INTO returns (CustomerID, OrderID, ProductID, Reason, ReturnDate) VALUES (?, ?, ?, ?, ?)",
                        (customer_id, order_id, product_id, reason, return_date))
            conn.commit()
            st.success("✅ Return logged successfully!")

    st.markdown("---")
    st.subheader("💸 Process a Refund")
    returns_df = pd.read_sql("SELECT * FROM returns", conn)

    with st.form("refund_form"):
        return_ids = returns_df["ReturnID"].unique() if not returns_df.empty else []
        return_id = st.selectbox("Select Return ID", return_ids)
        amount = st.number_input("Refund Amount", min_value=0.0, step=1.0)
        method = st.selectbox("Refund Method", ["Original Payment", "Store Credit", "Cash"])
        refund_btn = st.form_submit_button("Process Refund")

        if refund_btn:
            refund_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("INSERT INTO refunds (ReturnID, Amount, Method, RefundDate) VALUES (?, ?, ?, ?)",
                        (return_id, amount, method, refund_date))
            conn.commit()
            st.success("✅ Refund processed!")

    st.markdown("---")
    st.subheader("📊 Return & Refund History")
    refund_df = pd.read_sql("""
        SELECT r.ReturnID, r.CustomerID, r.OrderID, r.ProductID, r.Reason, r.ReturnDate,
               f.RefundID, f.Amount, f.Method, f.RefundDate
        FROM returns r LEFT JOIN refunds f ON r.ReturnID = f.ReturnID
        ORDER BY r.ReturnDate DESC
    """, conn)
    st.dataframe(refund_df)

    conn.close()
