import requests
import sqlite3
import pandas as pd
from datetime import datetime

# ── your own API URL ──────────────────────────────────────
API_URL  = "http://localhost:8000/users"
DATABASE = "fetched_users.db"
TABLE    = "users"

# ────────────────────────────────────────────────────────
# STEP 1 — Create database
# ────────────────────────────────────────────────────────
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
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
    conn.commit()
    conn.close()
    print("Database ready!")

# ────────────────────────────────────────────────────────
# STEP 2 — Fetch users from YOUR OWN API
# ────────────────────────────────────────────────────────
def fetch_users_from_my_api():
    print(f"\nFetching users from YOUR API: {API_URL}")
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            data  = response.json()
            users = data["users"]
            print(f"Successfully fetched {len(users)} users!")
            return users
        else:
            print(f"API Error: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        print("Cannot connect to your API!")
        print("Make sure it is running: uvicorn my_api:app --reload")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# ────────────────────────────────────────────────────────
# STEP 3 — Save users to database
# ────────────────────────────────────────────────────────
def save_to_database(users):
    conn   = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    inserted = 0
    skipped  = 0

    print("\nSaving users to database...")
    for u in users:
        try:
            cursor.execute(f"""
                INSERT INTO {TABLE}
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
            print(f"  Saved: {u['name']} ({u['email']})")
        except Exception as e:
            skipped += 1
            print(f"  Skipped: {e}")

    conn.commit()
    conn.close()
    return inserted, skipped

# ────────────────────────────────────────────────────────
# STEP 4 — Show stored users
# ────────────────────────────────────────────────────────
def show_stored_users():
    conn = sqlite3.connect(DATABASE)
    df   = pd.read_sql_query(
        f"SELECT * FROM {TABLE}",
        conn
    )
    conn.close()

    print(f"\nTotal users stored: {len(df)}")
    print("\nStored Users:")
    print("-" * 60)
    for _, row in df.iterrows():
        print(f"  Name:       {row['name']}")
        print(f"  Email:      {row['email']}")
        print(f"  Phone:      {row['phone']}")
        print(f"  Age:        {row['age']}")
        print(f"  City:       {row['city']}, {row['state']}")
        print(f"  Country:    {row['country']}")
        print(f"  Occupation: {row['occupation']}")
        print(f"  Company:    {row['company']}")
        print("-" * 60)
    return df

# ────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("   FETCH USERS FROM MY OWN API AND STORE")
    print("=" * 55)

    create_database()
    users = fetch_users_from_my_api()

    if users:
        inserted, skipped = save_to_database(users)

        print(f"\n{'='*55}")
        print(f"  Total Fetched : {len(users)}")
        print(f"  Saved to DB   : {inserted}")
        print(f"  Skipped       : {skipped}")
        print(f"  Time          : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*55}")

        show_stored_users()
    else:
        print("\nNo users fetched!")
        print("Make sure your API is running: uvicorn my_api:app --reload")

    print("\nAll done!")
