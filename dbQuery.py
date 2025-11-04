import sqlite3

conn = sqlite3.connect("ehr.db")
cursor = conn.cursor()

# Fetch all visits for a given patient
patient_name = "Zachary Johnson"
cursor.execute("""
SELECT v.date_of_visit, v.description, v.specialist
FROM visits v
JOIN patients p ON v.patient_id = p.patient_id
WHERE p.name = ?
""", (patient_name,))

for visit in cursor.fetchall():
    print(visit)

conn.close()
