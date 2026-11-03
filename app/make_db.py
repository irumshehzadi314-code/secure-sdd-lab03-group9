import sqlite3
from werkzeug.security import generate_password_hash

c = sqlite3.connect("medicare.db")
c.execute("CREATE TABLE staff (id INTEGER PRIMARY KEY, name TEXT, role TEXT, pw TEXT)")
c.execute("CREATE TABLE patients (id INTEGER PRIMARY KEY, name TEXT, diagnosis TEXT)")
c.execute("CREATE TABLE rx (id INTEGER PRIMARY KEY, dose TEXT)")

# Add users: doc (doctor), pharm (pharmacist), pat2 (patient)
c.execute("INSERT INTO staff VALUES (1, 'doc', 'doctor', ?)", (generate_password_hash("pass123"),))
c.execute("INSERT INTO staff VALUES (2, 'pharm', 'pharmacist', ?)", (generate_password_hash("pass123"),))
c.execute("INSERT INTO staff VALUES (3, 'pat2', 'patient', ?)", (generate_password_hash("pass123"),))

# Add patients
c.execute("INSERT INTO patients VALUES (1, 'Ali', 'Flu')")
c.execute("INSERT INTO patients VALUES (2, 'Sara', 'Cold')")
c.commit()
print("Database created successfully!")