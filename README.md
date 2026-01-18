# 🛡️ SkyHigh Travel: Red vs. Blue Team Simulation

**A full-cycle cybersecurity assessment demonstrating the Cyber Kill Chain, from vulnerability discovery to remediation.**

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Security](https://img.shields.io/badge/Focus-Network%20Security%20%26%20AppSec-red)
![Tools](https://img.shields.io/badge/Tools-Python%20%7C%20Wireshark%20%7C%20Bcrypt-blue)

## 📌 Executive Summary
This project simulates a real-world security assessment of "SkyHigh Travel," a corporate web application I architected with intentional vulnerabilities (OWASP Top 10). The goal was to perform a **Red Team** engagement (Phishing, Credential Harvesting, Network Sniffing) followed by a **Blue Team** response (Log Analysis, SIEM Alerting, and Patching).

## 🛠️ Tech Stack & Tools
* **Target Environment:** Python (Flask), SQLite3, Ubuntu Linux.
* **Attack Tools:** Wireshark, TCPdump, Custom Python SMTP Phishing Scripts, SEToolkit.
* **Defense Tools:** Python (Custom SIEM Script), Bcrypt (Hashing), Log Analysis.

---

## ⚔️ Phase 1: Red Team Operations (The Attack)

### 1. Network Traffic Forensics
**Objective:** Intercept authentication traffic to identify valid credentials.
* Performed a Man-in-the-Middle (MitM) simulation.
* Analyzed raw HTTP packets using **Wireshark** and **TCPdump**.
* **Key Discovery:** Differentiated between login states via HTTP Response Codes:
    * `HTTP 200 OK` = Failed Login (Error page loaded).
    * `HTTP 302 FOUND` = Successful Login (Redirect to dashboard).
* **Result:** Captured plaintext passwords in the `POST` body (e.g., `password=Summer2025!`).

### 2. Phishing Campaign & Credential Harvesting
**Objective:** Execute a Social Engineering attack.
* **Weaponization:** Wrote `pish_employees.py` to automate email delivery using SMTP.
* **Delivery:** Sent targeted "Flight Cancellation" emails to employees in the database.
* **Exploitation:** Users were redirected to a cloned login portal hosted on a local Flask server.
* **Impact:** Successfully intercepted CEO credentials in real-time.

---

## 🛡️ Phase 2: Blue Team Operations (The Defense)

### 1. Detection (Custom SIEM)
**Objective:** Detect the active attack in real-time.
* Developed `simple_siem.py`, a log-monitoring script.
* The script tails `server.log` and parses for signatures like `"LOGIN ATTEMPT"`.
* **Outcome:** The system successfully triggered a **CRITICAL ALERT** in the console immediately upon the attacker's first login attempt.

### 2. Remediation (Hardening)
**Objective:** Fix the "Plaintext Password" vulnerability.
* **Vulnerability:** Passwords were stored as raw text in the SQLite database.
* **The Fix:** Wrote `create_secure_db.py` to implement **Bcrypt** hashing.
* **Implementation:**
    * Added **Salting** to prevent Rainbow Table attacks.
    * Replaced plaintext with secure hashes (e.g., `$2b$12$...`).

---

## 🚨 Security Playbook: Incident Response
**PLAYBOOK ID:** PB-042 | **ALERT:** Suspicious Login / Credential Stuffing

### **1. Trigger**
SIEM detects 1+ failed login attempts or unauthorized access patterns (Signature: `LOGIN ATTEMPT`).

### **2. Investigation**
* Analyze Source IP and Timestamp.
* Check for multiple rapid attempts (Brute Force indicators).
* Cross-reference with employee geolocation.

### **3. Containment**
* **Lock the Account:** Temporarily disable the compromised user.
* **Terminate Session:** Revoke active tokens immediately.

### **4. Remediation**
* Force a Password Reset for the victim.
* Enforce Multi-Factor Authentication (MFA).
* **Long Term:** Deploy `create_secure_db.py` to encrypt the database.

---

## 📂 Project Structure
```text
├── app.py                # The Vulnerable Web Application (Flask)
├── users.db              # The SQLite Database (Employees)
├── pish_employees.py     # Red Team: Automated Phishing Script
├── simple_siem.py        # Blue Team: Intrusion Detection Script
├── create_secure_db.py   # Remediation: Database Hardening Script
├── images/               # Screenshots of Wireshark & Phishing Campaign
└── server.log            # Server Logs (Monitored by SIEM)


---

---

# 🧠 Chapter 2: The AI Upgrade (Jan 2026)
*Goal: Automate threat detection with an Intelligent, Real-Time SOC Analyst.*

In this chapter, I modernized the security stack by replacing the manual keyword-search tool with an AI Agent powered by **OpenAI (GPT-4o)**. This upgrade occurred in two phases:

### 🔹 Phase 2.1: The "Brain" Upgrade (Context Awareness)
I refactored the detection logic to solve the "Alert Fatigue" problem.
* **Old Way (Legacy):** Flagged *any* log containing "failed" or "error." (High False Positives).
* **New Way (AI):** The agent analyzes the *context* of the log line.
    * **SAFE:** User mistyped a password.
    * **SUSPICIOUS:** Accessing sensitive endpoints (`/admin`) from unknown IPs.
    * **MALICIOUS:** Recognizes attack syntax like SQL Injection (`' OR 1=1`).

### 🔹 Phase 2.2: The "Eyes" Upgrade (Real-Time Monitoring)
I upgraded the architecture from a static log reader to an "Always-On" Sentinel.
* **Implementation:** Modified `ai_siem.py` to use file pointer manipulation (`f.seek(0, 2)`) and an infinite loop.
* **Result:** The system now detects and analyzes threats milliseconds after they hit the server logs.

### 🛠️ How to Run the Sentinel
1.  **Activate the Environment:**
    ```bash
    source venv/bin/activate
    ```
2.  **Start the Analyst:**
    ```bash
    python3 ai_siem.py
    ```
    *(The script will now hang and watch the logs indefinitely. Use `Ctrl+C` to stop.)*

### 📸 Success Evidence: Defense in Depth
*Test: Live SQL Injection Attack*
* **Attack Vector:** User input `' OR 1=1 --` into the login field.
* **Layer 1 (Application):** **BLOCKED**. The app (hardened in Chapter 1) correctly identified invalid credentials, neutralizing the exploit.
* **Layer 2 (AI Analyst):** **DETECTED**. Despite the attack failing, the AI immediately flagged the log entry as **MALICIOUS** based on the SQL syntax pattern.
