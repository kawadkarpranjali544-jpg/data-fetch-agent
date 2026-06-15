```python
import pandas as pd

# -------------------------------
# Customer Details
# -------------------------------
customers = pd.DataFrame({
    "Customer_ID": [101, 102, 103],
    "Customer_Name": ["Alice", "Bob", "Charlie"],
    "City": ["New York", "Chicago", "Los Angeles"],
    "Phone": ["9876543210", "9876543211", "9876543212"]
})

# -------------------------------
# Product Details
# -------------------------------
products = pd.DataFrame({
    "Product_ID": [1, 2, 3],
    "Product_Name": ["Laptop", "Mobile", "Headphones"],
    "Category": ["Electronics", "Electronics", "Accessories"],
    "Price": [50000, 25000, 2000]
})

# -------------------------------
# Sales Transactions
# -------------------------------
sales = pd.DataFrame({
    "Sale_ID": [1, 2, 3, 4, 5, 6, 7],
    "Customer_ID": [101, 102, 101, 103, 102, 101, 103],
    "Product_ID": [1, 2, 3, 1, 3, 2, 2],
    "Quantity": [2, 1, 5, 1, 3, 2, 1],
    "Sale_Date": [
        "2025-01-10",
        "2025-01-15",
        "2025-02-05",
        "2025-02-18",
        "2025-03-01",
        "2025-03-20",
        "2025-03-25"
    ]
})

# -------------------------------
# Convert Date
# -------------------------------
sales["Sale_Date"] = pd.to_datetime(sales["Sale_Date"])

# Extract Month
sales["Month"] = sales["Sale_Date"].dt.strftime("%B")

# -------------------------------
# Merge Customer and Product Details
# -------------------------------
merged = sales.merge(customers, on="Customer_ID")
merged = merged.merge(products, on="Product_ID")

# -------------------------------
# Calculate Total Sales
# -------------------------------
merged["Total_Sales"] = merged["Quantity"] * merged["Price"]

# -------------------------------
# Monthly Sales Report
# -------------------------------
monthly_sales = merged.groupby(
    [
        "Month",
        "Customer_Name",
        "Product_Name"
    ]
)["Total_Sales"].sum().reset_index()

print("MONTHLY SALES OF EACH PRODUCT FOR EACH CUSTOMER")
print(monthly_sales)

# -------------------------------
# Detailed Report
# -------------------------------
print("\n")
print("DETAILED SALES REPORT")

print(
    merged[
        [
            "Sale_Date",
            "Customer_Name",
            "City",
            "Phone",
            "Product_Name",
            "Category",
            "Price",
            "Quantity",
            "Total_Sales"
        ]
    ]
)

# -------------------------------
# Monthly Total Sales
# -------------------------------
print("\n)
print("MONTHLY TOTAL SALES")

month_total = merged.groupby("Month")["Total_Sales"].sum().reset_index()

print(month_total)

# -------------------------------
# Customer-wise Sales
# -------------------------------
print("\n")
print("CUSTOMER-WISE SALES")

customer_sales = merged.groupby("Customer_Name")["Total_Sales"].sum().reset_index()

print(customer_sales)

# -------------------------------
# Product-wise Sales
# -------------------------------
print("\n")
print("PRODUCT-WISE SALES")

product_sales = merged.groupby("Product_Name")["Total_Sales"].sum().reset_index()

print(product_sales)
```
