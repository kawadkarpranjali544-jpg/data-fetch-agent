import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import re

# ────────────────────────────────────────────────────────
# DATABASE SETUP
# ────────────────────────────────────────────────────────
def create_database():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name       TEXT NOT NULL,
            email           TEXT UNIQUE NOT NULL,
            phone           TEXT NOT NULL,
            age             INTEGER NOT NULL,
            gender          TEXT,
            address         TEXT,
            city            TEXT,
            state           TEXT,
            country         TEXT,
            pincode         TEXT,
            occupation      TEXT,
            company         TEXT,
            created_at      TEXT
        )
    """)
    conn.commit()
    conn.close()

# ────────────────────────────────────────────────────────
# SAVE USER TO DATABASE
# ────────────────────────────────────────────────────────
def save_user(data):
    try:
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users
            (full_name, email, phone, age, gender,
             address, city, state, country, pincode,
             occupation, company, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["full_name"],
            data["email"],
            data["phone"],
            data["age"],
            data["gender"],
            data["address"],
            data["city"],
            data["state"],
            data["country"],
            data["pincode"],
            data["occupation"],
            data["company"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        return True, None
    except sqlite3.IntegrityError:
        return False, "This email is already registered!"
    except Exception as e:
        return False, str(e)

# ────────────────────────────────────────────────────────
# FETCH ALL USERS FROM DATABASE
# ────────────────────────────────────────────────────────
def fetch_all_users():
    conn = sqlite3.connect("user_data.db")
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

# ────────────────────────────────────────────────────────
# VALIDATE INPUTS
# ────────────────────────────────────────────────────────
def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

def validate_pincode(pincode):
    return pincode.isdigit() and len(pincode) == 6

# ────────────────────────────────────────────────────────
# PAGE SETUP
# ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="User Data Collector",
    page_icon="👤",
    layout="wide"
)

create_database()

st.title("👤 User Personal Data Collector")
st.caption("Fill in your personal details — data is stored securely in database")

# ────────────────────────────────────────────────────────
# TABS
# ────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Register User", "View All Users"])

# ────────────────────────────────────────────────────────
# TAB 1 — REGISTER USER
# ────────────────────────────────────────────────────────
with tab1:
    st.subheader("Enter Personal Details")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Basic Information")
        full_name  = st.text_input("Full Name *",        placeholder="John Doe")
        email      = st.text_input("Email Address *",    placeholder="john@example.com")
        phone      = st.text_input("Phone Number *",     placeholder="9876543210 (10 digits)")
        age        = st.number_input("Age *",            min_value=1, max_value=120, value=25)
        gender     = st.selectbox("Gender",              ["Male", "Female", "Other", "Prefer not to say"])

    with col2:
        st.markdown("#### Address Information")
        address  = st.text_area("Street Address",        placeholder="123 Main Street, Apt 4B")
        city     = st.text_input("City",                 placeholder="Mumbai")
        state    = st.text_input("State",                placeholder="Maharashtra")
        country  = st.text_input("Country",              placeholder="India", value="India")
        pincode  = st.text_input("Pincode",              placeholder="400001")

    st.markdown("#### Professional Information")
    col3, col4 = st.columns(2)
    with col3:
        occupation = st.text_input("Occupation",         placeholder="Software Engineer")
    with col4:
        company    = st.text_input("Company / Organization", placeholder="Tech Solutions Pvt Ltd")

    st.markdown("---")

    # submit button
    if st.button("Submit & Save to Database",
                 type="primary",
                 use_container_width=True):

        # validate required fields
        errors = []
        if not full_name.strip():
            errors.append("Full Name is required!")
        if not email.strip():
            errors.append("Email is required!")
        elif not validate_email(email):
            errors.append("Invalid email format!")
        if not phone.strip():
            errors.append("Phone number is required!")
        elif not validate_phone(phone):
            errors.append("Phone must be 10 digits!")
        if pincode and not validate_pincode(pincode):
            errors.append("Pincode must be 6 digits!")

        if errors:
            for error in errors:
                st.error(error)
        else:
            # save to database
            data = {
                "full_name":  full_name.strip(),
                "email":      email.strip().lower(),
                "phone":      phone.strip(),
                "age":        int(age),
                "gender":     gender,
                "address":    address.strip(),
                "city":       city.strip(),
                "state":      state.strip(),
                "country":    country.strip(),
                "pincode":    pincode.strip(),
                "occupation": occupation.strip(),
                "company":    company.strip()
            }

            success, error = save_user(data)

            if success:
                st.success(f"User '{full_name}' saved to database successfully!")
                st.balloons()

                # show saved data summary
                st.subheader("Saved Data Summary")
                summary_col1, summary_col2 = st.columns(2)
                with summary_col1:
                    st.info(f"""
                    **Basic Info**
                    - Name: {full_name}
                    - Email: {email}
                    - Phone: {phone}
                    - Age: {age}
                    - Gender: {gender}
                    """)
                with summary_col2:
                    st.info(f"""
                    **Address & Professional**
                    - City: {city}
                    - State: {state}
                    - Country: {country}
                    - Occupation: {occupation}
                    - Company: {company}
                    """)
            else:
                st.error(f"Error: {error}")

# ────────────────────────────────────────────────────────
# TAB 2 — VIEW ALL USERS
# ────────────────────────────────────────────────────────
with tab2:
    st.subheader("All Registered Users")

    df = fetch_all_users()

    if df.empty:
        st.info("No users registered yet. Go to Register User tab to add users!")
    else:
        # summary metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Users",    len(df))
        m2.metric("Cities",         df["city"].nunique())
        m3.metric("Avg Age",        f"{df['age'].mean():.0f} yrs")
        m4.metric("Latest Signup",  df["created_at"].iloc[-1][:10] if len(df) > 0 else "N/A")

        st.markdown("---")

        # search filter
        search = st.text_input("Search by name, email or city")
        if search:
            df = df[
                df["full_name"].str.contains(search, case=False, na=False) |
                df["email"].str.contains(search, case=False, na=False) |
                df["city"].str.contains(search, case=False, na=False)
            ]

        # show table
        st.dataframe(df, use_container_width=True)

        # download button
        csv = df.to_csv(index=False)
        st.download_button(
            "Download All Users as CSV",
            data=csv,
            file_name="all_users.csv",
            mime="text/csv",
            use_container_width=True
        )