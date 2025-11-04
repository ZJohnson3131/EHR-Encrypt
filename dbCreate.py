import sqlite3
import json

# --- Step 1: Create database connection ---
conn = sqlite3.connect("ehr.db")
cursor = conn.cursor()

# --- Step 2: Create tables ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS visits (
    visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    date_of_visit TEXT,
    description TEXT,
    specialist TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
)
""")

conn.commit()

# --- Step 3: Load JSON data ---
with open("records.json", "r") as f:
    data = json.load(f)

print(data)

records = data["record"]

# --- Step 4: Insert data ---
for record in records:
    name = record["name"].strip()
    date = record["DateOfVisit"]
    desc = record["Description"]
    specialist = record["Specialist"]

    # Insert patient if not already in the DB
    cursor.execute("INSERT OR IGNORE INTO patients (name) VALUES (?)", (name,))
    conn.commit()

    # Retrieve the patient's ID
    cursor.execute("SELECT patient_id FROM patients WHERE name = ?", (name,))
    patient_id = cursor.fetchone()[0]

    # Insert the visit record
    cursor.execute("""
        INSERT INTO visits (patient_id, date_of_visit, description, specialist)
        VALUES (?, ?, ?, ?)
    """, (patient_id, date, desc, specialist))

conn.commit()
conn.close()
