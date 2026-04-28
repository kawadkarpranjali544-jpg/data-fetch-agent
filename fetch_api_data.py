import requests
import sqlite3
import pandas as pd
from datetime import datetime

# ────────────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────────────
API_URL   = "https://randomuser.me/api/"  # free public API
DATABASE  = "fetched_users.db"            # SQLite database
TABLE     = "users"

# ────────────────────────────────────────────────────────
# STEP 1 — Create database and table
# ────────────────────────────────────────────────────────
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name   TEXT NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            phone       TEXT,
            gender      TEXT,
            age         INTEGER,
            city        TEXT,
            state       TEXT,
            country     TEXT,
            postcode    TEXT,
            picture     TEXT,
            fetched_at  TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database ready!")

# ────────────────────────────────────────────────────────
# STEP 2 — Fetch user data from free public API
# ────────────────────────────────────────────────────────
def fetch_users_from_api(count=10):
    print(f"\nFetching {count} users from API...")
    try:
        response = requests.get(
            API_URL,
            params={"results": count},
            timeout=10
        )
        if response.status_code == 200:
            data  = response.json()
            users = data["results"]
            print(f"Successfully fetched {len(users)} users!")
            return users
        else:
            print(f"API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# ────────────────────────────────────────────────────────
# STEP 3 — Parse user data from API response
# ────────────────────────────────────────────────────────
def parse_user(user):
    return {
        "full_name": f"{user['name']['first']} {user['name']['last']}",
        "email":     user["email"],
        "phone":     user["phone"],
        "gender":    user["gender"],
        "age":       user["dob"]["age"],
        "city":      user["location"]["city"],
        "state":     user["location"]["state"],
        "country":   user["location"]["country"],
        "postcode":  str(user["location"]["postcode"]),
        "picture":   user["picture"]["medium"],
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# ────────────────────────────────────────────────────────
# STEP 4 — Save users to SQLite database
# ────────────────────────────────────────────────────────
def save_to_database(users):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    inserted = 0
    skipped  = 0

    print("\nSaving users to database...")
    for user in users:
        data = parse_user(user)
        try:
            cursor.execute(f"""
                INSERT INTO {TABLE}
                (full_name, email, phone, gender, age,
                 city, state, country, postcode, picture, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                    full_name  = excluded.full_name,
                    phone      = excluded.phone,
                    gender     = excluded.gender,
                    age        = excluded.age,
                    city       = excluded.city,
                    state      = excluded.state,
                    country    = excluded.country,
                    postcode   = excluded.postcode,
                    picture    = excluded.picture,
                    fetched_at = excluded.fetched_at
            """, (
                data["full_name"],
                data["email"],
                data["phone"],
                data["gender"],
                data["age"],
                data["city"],
                data["state"],
                data["country"],
                data["postcode"],
                data["picture"],
                data["fetched_at"]
            ))
            inserted += 1
            print(f"  Saved: {data['full_name']} ({data['email']})")
        except Exception as e:
            skipped += 1
            print(f"  Skipped: {e}")

    conn.commit()
    conn.close()
    return inserted, skipped

# ────────────────────────────────────────────────────────
# STEP 5 — Show all stored users
# ────────────────────────────────────────────────────────
def show_stored_users():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE}", conn)
    conn.close()

    print(f"\nTotal users in database: {len(df)}")
    print("\nStored Users:")
    print("-" * 80)
    for _, row in df.iterrows():
        print(f"  Name:    {row['full_name']}")
        print(f"  Email:   {row['email']}")
        print(f"  Phone:   {row['phone']}")
        print(f"  Age:     {row['age']}")
        print(f"  City:    {row['city']}, {row['state']}, {row['country']}")
        print(f"  Fetched: {row['fetched_at']}")
        print("-" * 80)
    return df

# ────────────────────────────────────────────────────────
# STEP 6 — Save to CSV as backup
# ────────────────────────────────────────────────────────
def save_to_csv(df):
    filename = f"users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    print(f"\nBackup saved to: {filename}")

# ────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("   FETCH DATA FROM API AND STORE AGENT")
    print("=" * 55)

    # step 1 — setup database
    create_database()

    # step 2 — fetch users from API
    users = fetch_users_from_api(count=10)

    if users:
        # step 3 — save to database
        inserted, skipped = save_to_database(users)

        # step 4 — show results
        print(f"\n{'='*55}")
        print(f"  Total Fetched : {len(users)}")
        print(f"  Saved to DB   : {inserted}")
        print(f"  Skipped       : {skipped}")
        print(f"  Time          : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*55}")

        # step 5 — show stored users
        df = show_stored_users()

        # step 6 — save CSV backup
        save_to_csv(df)

    print("\nAll done!")