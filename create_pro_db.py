import sqlite3
import os

# Reset the file so it's fresh
if os.path.exists("users.db"):
    os.remove("users.db")

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table with USERNAME column
cursor.execute("CREATE TABLE users (username TEXT, email TEXT)")

# Add the targets (Name, Email)
staff = [
    ("Robert", "ceo@skyhigh.com"),
    ("T-Rex", "trex@skyhigh.com"),
    ("Krysta", "krysta@skyhigh.com"),
    ("Milo", "milo@skyhigh.com"),
    ("Tuna", "tuna@skyhigh.com"),
    ("Nayla", "nayla@skyhigh.com"),
    ("Beans", "beans@skyhigh.com"),
    ("Hasso", "hasso@skyhigh.com")
]

cursor.executemany("INSERT INTO users VALUES (?,?)", staff)
conn.commit()
print("Success! users.db is ready.")
