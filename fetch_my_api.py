import requests
import sqlite3
import pandas as pd
from datetime import datetime

# ── your API URL ──────────────────────────────────────────
API_URL  = "http://localhost:8000/products"
DATABASE = "my_products.db"
TABLE    = "products"

# ────────────────────────────────────────────────────────
# STEP 1 — Create database
# ────────────────────────────────────────────────────────
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id  INTEGER,
            name        TEXT NOT NULL,
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
    print("Database ready!")

# ────────────────────────────────────────────────────────
# STEP 2 — Fetch data from YOUR API
# ────────────────────────────────────────────────────────
def fetch_from_my_api():
    print(f"\nFetching products from your API: {API_URL}")
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            data     = response.json()
            products = data["products"]
            print(f"Successfully fetched {len(products)} products!")
            return products
        else:
            print(f"API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your API is running: uvicorn my_api:app --reload")
        return []

# ────────────────────────────────────────────────────────
# STEP 3 — Save to database
# ────────────────────────────────────────────────────────
def save_to_database(products):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    inserted = 0
    skipped  = 0

    print("\nSaving products to database...")
    for p in products:
        try:
            cursor.execute(f"""
                INSERT INTO {TABLE}
                (product_id, name, price, category, stock,
                 description, brand, rating, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["id"],
                p["name"],
                p["price"],
                p["category"],
                p["stock"],
                p["description"],
                p["brand"],
                p["rating"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            inserted += 1
            print(f"  Saved: {p['name']} - Rs.{p['price']}")
        except Exception as e:
            skipped += 1
            print(f"  Skipped: {e}")

    conn.commit()
    conn.close()
    return inserted, skipped

# ────────────────────────────────────────────────────────
# STEP 4 — Show stored data
# ────────────────────────────────────────────────────────
def show_stored_products():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE}", conn)
    conn.close()

    print(f"\nTotal products in database: {len(df)}")
    print("\nStored Products:")
    print("-" * 70)
    for _, row in df.iterrows():
        print(f"  Name:     {row['name']}")
        print(f"  Price:    Rs. {row['price']}")
        print(f"  Category: {row['category']}")
        print(f"  Stock:    {row['stock']} units")
        print(f"  Brand:    {row['brand']}")
        print(f"  Rating:   {row['rating']}/5")
        print("-" * 70)
    return df

# ────────────────────────────────────────────────────────
# STEP 5 — Save CSV backup
# ────────────────────────────────────────────────────────
def save_csv(df):
    filename = f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    print(f"\nCSV backup saved: {filename}")

# ────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("   FETCH FROM MY API AND STORE")
    print("=" * 55)

    create_database()
    products = fetch_from_my_api()

    if products:
        inserted, skipped = save_to_database(products)

        print(f"\n{'='*55}")
        print(f"  Total Fetched  : {len(products)}")
        print(f"  Saved to DB    : {inserted}")
        print(f"  Skipped        : {skipped}")
        print(f"  Time           : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*55}")

        df = show_stored_products()
        save_csv(df)

    print("\nAll done!")