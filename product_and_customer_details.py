# ────────────────────────────────────────────────────────
# CUSTOMER DETAILS
# ────────────────────────────────────────────────────────
customers = [
    {
        "id":    1,
        "name":  "Rahul Sharma",
        "email": "rahul@email.com",
        "phone": "9876543210",
        "city":  "Mumbai",
        "state": "Maharashtra",
        "country": "India"
    },
    {
        "id":    2,
        "name":  "Priya Singh",
        "email": "priya@email.com",
        "phone": "9876543211",
        "city":  "Delhi",
        "state": "Delhi",
        "country": "India"
    },
    {
        "id":    3,
        "name":  "Amit Kumar",
        "email": "amit@email.com",
        "phone": "9876543212",
        "city":  "Bangalore",
        "state": "Karnataka",
        "country": "India"
    }
]

# ────────────────────────────────────────────────────────
# PRODUCT DETAILS
# ────────────────────────────────────────────────────────
products = [
    {
        "id":       1,
        "name":     "iPhone 15",
        "price":    99999,
        "category": "Electronics",
        "brand":    "Apple",
        "rating":   4.8
    },
    {
        "id":       2,
        "name":     "Samsung TV",
        "price":    55000,
        "category": "Electronics",
        "brand":    "Samsung",
        "rating":   4.5
    },
    {
        "id":       3,
        "name":     "Nike Shoes",
        "price":    8999,
        "category": "Footwear",
        "brand":    "Nike",
        "rating":   4.6
    },
    {
        "id":       4,
        "name":     "Levi Jeans",
        "price":    3999,
        "category": "Clothing",
        "brand":    "Levi's",
        "rating":   4.3
    },
    {
        "id":       5,
        "name":     "Sony Headphones",
        "price":    15000,
        "category": "Electronics",
        "brand":    "Sony",
        "rating":   4.7
    }
]

# ────────────────────────────────────────────────────────
# MONTHLY SALES DATA
# each entry: customer_id, product_id, month, units_sold
# ────────────────────────────────────────────────────────
monthly_sales_data = [
    # Rahul Sharma (customer 1) — buys iPhone and Sony Headphones
    {"customer_id": 1, "product_id": 1, "month": "January",  "year": 2025, "units_sold": 10},
    {"customer_id": 1, "product_id": 1, "month": "February", "year": 2025, "units_sold": 15},
    {"customer_id": 1, "product_id": 1, "month": "March",    "year": 2025, "units_sold": 8},
    {"customer_id": 1, "product_id": 5, "month": "January",  "year": 2025, "units_sold": 20},
    {"customer_id": 1, "product_id": 5, "month": "February", "year": 2025, "units_sold": 25},
    {"customer_id": 1, "product_id": 5, "month": "March",    "year": 2025, "units_sold": 18},

    # Priya Singh (customer 2) — buys Samsung TV and Nike Shoes
    {"customer_id": 2, "product_id": 2, "month": "January",  "year": 2025, "units_sold": 5},
    {"customer_id": 2, "product_id": 2, "month": "February", "year": 2025, "units_sold": 8},
    {"customer_id": 2, "product_id": 2, "month": "March",    "year": 2025, "units_sold": 6},
    {"customer_id": 2, "product_id": 3, "month": "January",  "year": 2025, "units_sold": 30},
    {"customer_id": 2, "product_id": 3, "month": "February", "year": 2025, "units_sold": 45},
    {"customer_id": 2, "product_id": 3, "month": "March",    "year": 2025, "units_sold": 25},

    # Amit Kumar (customer 3) — buys Levi Jeans and Nike Shoes
    {"customer_id": 3, "product_id": 4, "month": "January",  "year": 2025, "units_sold": 50},
    {"customer_id": 3, "product_id": 4, "month": "February", "year": 2025, "units_sold": 60},
    {"customer_id": 3, "product_id": 4, "month": "March",    "year": 2025, "units_sold": 40},
    {"customer_id": 3, "product_id": 3, "month": "January",  "year": 2025, "units_sold": 15},
    {"customer_id": 3, "product_id": 3, "month": "February", "year": 2025, "units_sold": 20},
    {"customer_id": 3, "product_id": 3, "month": "March",    "year": 2025, "units_sold": 10},
]

# ────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ────────────────────────────────────────────────────────
def get_customer_by_id(customer_id):
    for c in customers:
        if c["id"] == customer_id:
            return c
    return None

def get_product_by_id(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None

# ────────────────────────────────────────────────────────
# CALCULATE MONTHLY SALES
# ────────────────────────────────────────────────────────
def calculate_monthly_sales():
    results = []
    for sale in monthly_sales_data:
        customer = get_customer_by_id(sale["customer_id"])
        product  = get_product_by_id(sale["product_id"])
        if customer and product:
            revenue = sale["units_sold"] * product["price"]
            results.append({
                "customer_name": customer["name"],
                "customer_city": customer["city"],
                "product_name":  product["name"],
                "product_price": product["price"],
                "category":      product["category"],
                "month":         sale["month"],
                "year":          sale["year"],
                "units_sold":    sale["units_sold"],
                "revenue":       revenue
            })
    return results

# ────────────────────────────────────────────────────────
# CALCULATE TOTAL SALES PER CUSTOMER
# ────────────────────────────────────────────────────────
def calculate_total_per_customer():
    totals = {}
    sales  = calculate_monthly_sales()
    for s in sales:
        name = s["customer_name"]
        if name not in totals:
            totals[name] = {
                "total_units":   0,
                "total_revenue": 0,
                "products":      set()
            }
        totals[name]["total_units"]   += s["units_sold"]
        totals[name]["total_revenue"] += s["revenue"]
        totals[name]["products"].add(s["product_name"])
    return totals

# ────────────────────────────────────────────────────────
# CALCULATE TOTAL SALES PER PRODUCT
# ────────────────────────────────────────────────────────
def calculate_total_per_product():
    totals = {}
    sales  = calculate_monthly_sales()
    for s in sales:
        name = s["product_name"]
        if name not in totals:
            totals[name] = {
                "total_units":   0,
                "total_revenue": 0,
                "customers":     set()
            }
        totals[name]["total_units"]   += s["units_sold"]
        totals[name]["total_revenue"] += s["revenue"]
        totals[name]["customers"].add(s["customer_name"])
    return totals

# ────────────────────────────────────────────────────────
# CALCULATE BEST MONTH
# ────────────────────────────────────────────────────────
def calculate_best_month():
    monthly = {}
    sales   = calculate_monthly_sales()
    for s in sales:
        month = s["month"]
        if month not in monthly:
            monthly[month] = {"units": 0, "revenue": 0}
        monthly[month]["units"]   += s["units_sold"]
        monthly[month]["revenue"] += s["revenue"]
    return monthly

# ────────────────────────────────────────────────────────
# MAIN — SHOW ALL RESULTS
# ────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 60)
    print("   MONTHLY SALES REPORT")
    print("=" * 60)

    # show all monthly sales
    print("\n1. MONTHLY SALES — EACH CUSTOMER EACH PRODUCT")
    print("-" * 60)
    sales = calculate_monthly_sales()
    for s in sales:
        print(f"Customer: {s['customer_name']:<15} | "
              f"Product: {s['product_name']:<18} | "
              f"Month: {s['month']:<10} | "
              f"Units: {s['units_sold']:>3} | "
              f"Revenue: Rs.{s['revenue']:>10,}")

    # show totals per customer
    print("\n2. TOTAL SALES PER CUSTOMER")
    print("-" * 60)
    customer_totals = calculate_total_per_customer()
    for name, data in customer_totals.items():
        print(f"Customer: {name}")
        print(f"  Total Units:   {data['total_units']}")
        print(f"  Total Revenue: Rs.{data['total_revenue']:,}")
        print(f"  Products:      {', '.join(data['products'])}")
        print()

    # show totals per product
    print("3. TOTAL SALES PER PRODUCT")
    print("-" * 60)
    product_totals = calculate_total_per_product()
    for name, data in product_totals.items():
        print(f"Product: {name}")
        print(f"  Total Units:   {data['total_units']}")
        print(f"  Total Revenue: Rs.{data['total_revenue']:,}")
        print(f"  Customers:     {', '.join(data['customers'])}")
        print()

    # show best month
    print("4. MONTHLY COMPARISON")
    print("-" * 60)
    monthly = calculate_best_month()
    for month, data in monthly.items():
        print(f"Month: {month:<12} | "
              f"Units: {data['units']:>4} | "
              f"Revenue: Rs.{data['revenue']:>12,}")

    # find best performers
    print("\n5. BEST PERFORMERS")
    print("-" * 60)
    best_customer = max(
        customer_totals.items(),
        key=lambda x: x[1]["total_revenue"]
    )
    best_product = max(
        product_totals.items(),
        key=lambda x: x[1]["total_revenue"]
    )
    best_month = max(
        monthly.items(),
        key=lambda x: x[1]["revenue"]
    )
    print(f"Best Customer: {best_customer[0]} — Rs.{best_customer[1]['total_revenue']:,}")
    print(f"Best Product:  {best_product[0]} — Rs.{best_product[1]['total_revenue']:,}")
    print(f"Best Month:    {best_month[0]} — Rs.{best_month[1]['revenue']:,}")
    print("=" * 60)
