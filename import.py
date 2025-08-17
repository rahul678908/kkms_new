import json
import mysql.connector
from datetime import datetime
import django
import os

# Set up Django environment so we can use its auth system
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # <-- replace with your settings module
django.setup()

from django.contrib.auth.hashers import make_password

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwertyui@123",
    database="kkms"
)
cursor = conn.cursor()

# Load JSON file
with open(r"C:\Users\Sragh\Downloads\customer.json", "r", encoding="utf-8") as f:
    data = json.load(f)

customers = data[2]["data"]

# SQL for inserting into accounts_user
user_sql = """
INSERT INTO accounts_user (
    password, last_login, is_superuser, username,
    first_name, last_name, email, is_staff, is_active,
    date_joined, is_superadmin, is_customer
) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

# SQL for inserting into accounts_customer
customer_sql = """
INSERT INTO accounts_customer (
    id, customer_name, customer_email, father_name, age, gender, contact_no, description, profile_image,
    id_proof, address, star, married_sisters, married_brothers, no_sisters,
    no_brothers, mother_job, father_job, mother_name, landline_no, year, school,
    education, income, job_city, job_department, company, job, caste, marital_status,
    physical_condition, weight, complexion, height, time_birth, place_birth, dob,
    district, city, post, pin_code, street, house_name, status, is_active, created,
    updated, dosham, user_id
) VALUES (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s
)
"""

for row in customers:
    customer_name = row.get("customer_name") or ""
    first_name, *last_name_parts = customer_name.split(" ", 1)
    last_name = last_name_parts[0] if last_name_parts else ""

    email = row.get("customer_email")
    if not email:
        print(f"Skipping customer {customer_name}: no email")
        continue

    # Check if user exists
    cursor.execute("SELECT id FROM accounts_user WHERE username=%s", (email,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]  # existing user
    else:
        # Hash the password
        hashed_password = make_password("default_password123")  # You can change the default password
        # Insert new user
        user_values = (
            hashed_password,
            None,
            0,
            email,
            first_name,
            last_name,
            email,
            0,
            1,
            datetime.now(),
            0,
            1
        )
        cursor.execute(user_sql, user_values)
        user_id = cursor.lastrowid

    # Check if customer already exists
    cursor.execute("SELECT id FROM accounts_customer WHERE user_id=%s", (user_id,))
    if cursor.fetchone():
        print(f"Customer for {email} already exists, skipping")
        continue

    # Insert customer
    customer_values = (
        row.get("customer_id"),
        row.get("customer_name"),
        email,
        row.get("customer_father_name"),
        int(row["customer_age"]) if row.get("customer_age") and str(row["customer_age"]).isdigit() else None,
        row.get("customer_gender"),
        row.get("customer_contact_no"),
        row.get("customer_description"),
        row.get("customer_image"),
        row.get("customer_id_proof"),
        row.get("customer_address"),
        row.get("customer_star"),
        row.get("customer_married_sisters"),
        row.get("customer_married_brothers"),
        row.get("customer_no_sisters"),
        row.get("customer_no_brothers"),
        row.get("customer_mother_job"),
        row.get("customer_father_job"),
        row.get("customer_mother_name"),
        int(row.get("customer_landline_no", 0)) if str(row.get("customer_landline_no","0")).isdigit() else None,
        row.get("customer_year"),
        row.get("customer_school"),
        row.get("customer_education"),
        row.get("customer_income"),
        row.get("customer_job_city"),
        row.get("customer_job_department"),
        row.get("customer_company"),
        row.get("customer_job"),
        row.get("customer_caste"),
        row.get("customer_marital_status"),
        row.get("customer_physical_condition"),
        row.get("customer_weight"),
        row.get("customer_complexion"),
        row.get("customer_height"),
        row.get("customer_time_birth"),
        row.get("customer_place_birth"),
        row.get("customer_dob"),
        row.get("customer_district"),
        row.get("customer_city"),
        row.get("customer_post"),
        row.get("customer_pin_code"),
        row.get("customer_street"),
        row.get("customer_house_name"),
        int(row.get("rec_status", 0)),
        int(row.get("is_active", 0)),
        row.get("rec_created"),
        row.get("rec_updated"),
        row.get("customer_dosham"),
        user_id
    )
    cursor.execute(customer_sql, customer_values)

conn.commit()
cursor.close()
conn.close()
print("✅ Customers + Users imported successfully with hashed passwords!")
