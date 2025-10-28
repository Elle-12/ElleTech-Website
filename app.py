# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

# app config
app = Flask(__name__, template_folder='UI', static_folder='CSS')
app.secret_key = os.getenv('SECRET_KEY', 'devsecret')

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'elletech'),
    'charset': 'utf8mb4'
}

# simple DB helper
def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("DB connection error:", e)
        return None

# login required decorator
from functools import wraps
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# ---------- AUTH ----------
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        conn = get_db()
        if conn:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, username))
            user = cur.fetchone()
            cur.close()
            conn.close()
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Logged in successfully', 'success')
                return redirect(url_for('home'))
        flash('Invalid username/email or password', 'danger')
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
