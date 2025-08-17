import json
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwertyui@123",
    database="kkms"
)
cursor = conn.cursor()

# Load JSON file
with open(r"C:\Users\Sragh\Downloads\payment.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# phpMyAdmin JSON structure → table rows inside [2]["data"]
payments = data[2]["data"]

# SQL Insert (match your payment table)
sql = """
INSERT INTO accounts_payment (
    id, customer_id, payment_date, amount,is_active, created_at,updated_at
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for row in payments:
    customer_id = row.get("customer_id")

    # Check if customer exists
    cursor.execute("SELECT id FROM accounts_customer WHERE id = %s", (customer_id,))
    if cursor.fetchone() is None:
        print(f"⏭️ Skipping payment {row.get('payment_id')} - customer {customer_id} not found")
        continue

    values = (
        row.get("payment_id"),      # maps to id
        customer_id,     # maps to customer_id
        row.get("payment_date"),    # datetime(6)
        row.get("amount"),          # int
        True,  # is_active
        row.get("created_date"),
        row.get("created_date")      # maps to created_date
    )
    cursor.execute(sql, values)

conn.commit()
cursor.close()
conn.close()
print("✅ Payments imported successfully!")
