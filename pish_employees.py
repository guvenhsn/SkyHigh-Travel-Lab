import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION ---
DB_PATH = "users.db"  # Path to your database
SMTP_SERVER = "127.0.0.1" # Sending to local MailCatcher
SMTP_PORT = 1025          # MailCatcher's port
ATTACKER_LINK = "http://10.0.0.218:5000" # Your Kali IP (The Trap)

def send_phishing_email(target_email, employee_name):
    # 1. Create the Email
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "URGENT: Flight UA992 Canceled - Action Required"
    msg['From'] = "alerts@skyhigh-travel.com" # Spoofed Sender
    msg['To'] = target_email

    # 2. The Phishing Message (HTML)
    html_content = f"""
    <html>
      <body>
        <h2>⚠️ Flight Cancellation Alert</h2>
        <p>Dear {employee_name},</p>
        <p>Your upcoming corporate travel flight <b>UA992</b> has been canceled due to unscheduled maintenance.</p>
        <p>Please log in to the Employee Portal immediately to approve your rebooking options:</p>
        <br>
        <a href="{ATTACKER_LINK}" style="background-color: #d9534f; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
           CLICK HERE TO REBOOK
        </a>
        <br><br>
        <p>Failure to rebook within 24 hours may result in loss of travel credits.</p>
        <p>IT Security Team</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    # 3. Send the Email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print(f"[+] Phishing email sent to: {target_email}")
    except Exception as e:
        print(f"[-] Failed to send to {target_email}: {e}")

# --- MAIN EXECUTION ---
print("--- STARTING PHISHING CAMPAIGN ---")

# Connect to DB and get employees
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT username, email FROM users") # Assuming username is the name
employees = cursor.fetchall()
conn.close()

# Loop through every employee and PHISH them
for name, email in employees:
    if email: # Make sure they have an email
        send_phishing_email(email, name)

print("--- CAMPAIGN FINISHED ---")
