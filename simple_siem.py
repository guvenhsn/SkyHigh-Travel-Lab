import time
import os

LOG_FILE = "server.log"

print("--- 🛡️  SKYHIGH SIEM ACTIVATED 🛡️  ---")
print(f"[*] Monitoring {LOG_FILE} for suspicious activity...")

# 1. Open the file and go to the end (so we only see NEW attacks)
try:
    f = open(LOG_FILE, "r")
    f.seek(0, os.SEEK_END)
except FileNotFoundError:
    print("Error: server.log not found. Make sure app.py is running and you have tried to login!")
    exit()

# 2. Loop forever and watch for new lines
while True:
    line = f.readline()
    if not line:
        time.sleep(0.1) # Sleep briefly if no new data
        continue

    line = line.strip()

    # --- DEFENSE RULES ---
    
    # Rule 1: Detect Login Attempts (Credential Stuffing)
    if "LOGIN ATTEMPT" in line:
        print(f"\n[!] 🚨 CRITICAL ALERT: Suspicious Login Detected!")
        print(f"    Payload: {line}")
        print("    Action: ACCOUNT FLAGGED FOR REVIEW\n")

    # Rule 2: Detect Admin Access
    elif "admin" in line.lower():
         print(f"[!] ⚠️  ALERT: Admin Panel Access Detected: {line}")
