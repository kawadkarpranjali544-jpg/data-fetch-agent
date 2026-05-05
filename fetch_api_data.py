import requests
import sqlite3
import pandas as pd
from datetime import datetime

# ── your personal API URL ─────────────────────────────────
USERS_API    = "http://localhost:8000/users"
PRODUCTS_API = "http://localhost:8000/products"
DATABASE     = "fetched_data.db"

# ────────────────────────────────────────────────────────
# STEP 1 — Create local database
# ────────────────────────────────────────────────────────
def create_database():
    conn   = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            name        TEXT,
            email       TEXT,
            phone       TEXT,
            age         INTEGER,
            gender      TEXT,
            address     TEXT,
            city        TEXT,
            state       TEXT,
            country     TEXT,
            pincode     TEXT,
            occupation  TEXT,
            company     TEXT,
            fetched_at  TEXT
        )
    """)

    # products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id  INTEGER,
            name        TEXT,
            price       REAL,
            category    TEXT,
            stock       INTEGER,
            description TEXT,
            brand       TEXT,
            rating      REAL,
            fetched_at  TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Local database ready!")

# ────────────────────────────────────────────────────────
# STEP 2 — Fetch users from YOUR personal API
# ────────────────────────────────────────────────────────
def fetch_users():
    print(f"\nFetching users from YOUR personal API...")
    print(f"URL: {USERS_API}")
    try:
        response = requests.get(USERS_API, timeout=10)
        if response.status_code == 200:
            data  = response.json()
            users = data["users"]
            print(f"Successfully fetched {len(users)} users!")
            return users
        else:
            print(f"API Error: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        print("Cannot connect to your personal API!")
        print("Make sure it is running: uvicorn my_api:app --reload")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# ────────────────────────────────────────────────────────
# STEP 3 — Fetch products from YOUR personal API
# ────────────────────────────────────────────────────────
def fetch_products():
    print(f"\nFetching products from YOUR personal API...")
    print(f"URL: {PRODUCTS_API}")
    try:
        response = requests.get(PRODUCTS_API, timeout=10)
        if response.status_code == 200:
            data     = response.json()
            products = data["products"]
            print(f"Successfully fetched {len(products)} products!")
            return products
        else:
            print(f"API Error: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        print("Cannot connect to your personal API!")
        print("Make sure it is running: uvicorn my_api:app --reload")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# ────────────────────────────────────────────────────────
# STEP 4 — Save users to local database
# ────────────────────────────────────────────────────────
def save_users(users):
    conn   = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    inserted = 0
    skipped  = 0

    print("\nSaving users to local database...")
    for u in users:
        try:
            cursor.execute("""
                INSERT INTO users
                (user_id, name, email, phone, age, gender,
                 address, city, state, country, pincode,
                 occupation, company, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                u["id"],
                u["name"],
                u["email"],
                u["phone"],
                u["age"],
                u["gender"],
                u["address"],
                u["city"],
                u["state"],
                u["country"],
                u["pincode"],
                u["occupation"],
                u["company"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            inserted += 1
            print(f"  Saved user: {u['name']} ({u['email']})")
        except Exception as e:
            skipped += 1
            print(f"  Skipped: {e}")

    conn.commit()
    conn.close()
    return inserted, skipped

# ────────────────────────────────────────────────────────
# STEP 5 — Save products to local database
# ────────────────────────────────────────────────────────
def save_products(products):
    conn   = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    inserted = 0
    skipped  = 0

    print("\nSaving products to local database...")
    for p in products:
        try:
            cursor.execute("""
                INSERT INTO products
                (product_id, name, price, category, stock,
                 description, brand, rating, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["id"],
                p["name"],
                p["price"],
                p["category"],
                p["stock"],
                p.get("description", ""),
                p.get("brand", ""),
                p.get("rating", 0),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            inserted += 1
            print(f"  Saved product: {p['name']} — Rs.{p['price']}")
        except Exception as e:
            skipped += 1
            print(f"  Skipped: {e}")

    conn.commit()
    conn.close()
    return inserted, skipped

# ────────────────────────────────────────────────────────
# STEP 6 — Show all stored data
# ────────────────────────────────────────────────────────
def show_stored_data():
    conn = sqlite3.connect(DATABASE)

    # show users
    df_users = pd.read_sql_query(
        "SELECT * FROM users",
        conn
    )
    print(f"\nTotal users stored: {len(df_users)}")
    print("\nStored Users:")
    print("-" * 60)
    for _, row in df_users.iterrows():
        print(f"  Name:       {row['name']}")
        print(f"  Email:      {row['email']}")
        print(f"  Phone:      {row['phone']}")
        print(f"  Age:        {row['age']}")
        print(f"  City:       {row['city']}, {row['state']}")
        print(f"  Occupation: {row['occupation']}")
        print(f"  Company:    {row['company']}")
        print("-" * 60)

    # show products
    df_products = pd.read_sql_query(
        "SELECT * FROM products",
        conn
    )
    print(f"\nTotal products stored: {len(df_products)}")
    print("\nStored Products:")
    print("-" * 60)
    for _, row in df_products.iterrows():
        print(f"  Name:     {row['name']}")
        print(f"  Price:    Rs. {row['price']}")
        print(f"  Category: {row['category']}")
        print(f"  Stock:    {row['stock']}")
        print("-" * 60)

    conn.close()
    return df_users, df_products

# ────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("   FETCH FROM MY PERSONAL API")
    print("   Data source: MySQL Workbench → my_api.py → here")
    print("=" * 60)

    # setup local database
    create_database()

    # fetch and save users
    users = fetch_users()
    if users:
        u_inserted, u_skipped = save_users(users)
        print(f"\n  Users  — Fetched: {len(users)} | Saved: {u_inserted} | Skipped: {u_skipped}")

    # fetch and save products
    products = fetch_products()
    if products:
        p_inserted, p_skipped = save_products(products)
        print(f"  Products — Fetched: {len(products)} | Saved: {p_inserted} | Skipped: {p_skipped}")

    # show all stored data
    show_stored_data()

    print("\nAll done!")
    print("Data flow: MySQL Workbench → my_api.py → fetch_api_data.py → fetched_data.db")
