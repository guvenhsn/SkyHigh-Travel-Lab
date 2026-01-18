import sqlite3
import os
import bcrypt  # Import the hashing tool

# Reset the file so it's fresh
if os.path.exists("users.db"):
    os.remove("users.db")

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table with USERNAME, EMAIL, and PASSWORD
cursor.execute("CREATE TABLE users (username TEXT, email TEXT, password TEXT)")

# The raw data (passwords to be hashed)
staff_data = [
    ("Robert", "ceo@skyhigh.com", "Summer2025!"),
    ("T-Rex", "trex@skyhigh.com", "DinoRulez"),
    ("Krysta", "krysta@skyhigh.com", "AdminPass123"),
    ("Milo", "milo@skyhigh.com", "Treats4Life"),
    ("Tuna", "tuna@skyhigh.com", "FishyBusiness"),
    ("Nayla", "nayla@skyhigh.com", "BarkBark99"),
    ("Beans", "beans@skyhigh.com", "MeowMix2024"),
    ("Hasso", "hasso@skyhigh.com", "GoodBoy1")
]

print("--- 🔒 HASHING PASSWORDS & POPULATING DB 🔒 ---")

for name, email, plain_password in staff_data:
    # 1. Convert password to bytes
    bytes = plain_password.encode('utf-8')
    
    # 2. Generate Salt and Hash
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    
    # 3. Store the HASH, not the password
    cursor.execute("INSERT INTO users VALUES (?,?,?)", (name, email, hash))
    print(f"[*] Secured user: {name}")

conn.commit()
print("--- SUCCESS: Database is now Encrypted ---")
