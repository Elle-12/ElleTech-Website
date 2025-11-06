import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='UI', static_folder='CSS')
app.secret_key = os.getenv('SECRET_KEY')

# DATABASE CONNECTION
def get_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        raise

# DATABASE HELPERS

def query_all(query, params=()):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def query_one(query, params=()):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def execute(query, params=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

# ROUTES

@app.route('/')
def index():
    # Redirect based on login status
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_one("SELECT * FROM users WHERE username=%s OR email=%s", (username, username))
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user.get('role', 'user')  
            return redirect(url_for('home'))
        else:
            msg = 'Invalid username or password.'
    return render_template('login.html', message=msg)

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        data = {
            'full_name': request.form['full_name'],
            'email': request.form['email'],
            'username': request.form['username'],
            'password': generate_password_hash(request.form['password']),
            'contact_no': request.form['contact_no'],
            'address': request.form['address']
        }
        existing = query_one("SELECT * FROM users WHERE username=%s OR email=%s",
                             (data['username'], data['email']))
        if existing:
            msg = 'Username or email already exists.'
        else:
            execute("""INSERT INTO users (full_name, email, username, password_hash, contact_no, address, role)
                       VALUES (%s,%s,%s,%s,%s,%s,'user')""",
                    (data['full_name'], data['email'], data['username'], data['password'],
                     data['contact_no'], data['address']))
            msg = 'Registered successfully! You can log in now.'
            return redirect(url_for('login'))
    return render_template('register.html', message=msg)


# LOGOUT

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# HOME

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    products = query_all("SELECT * FROM products ORDER BY created_at DESC LIMIT 4")
    return render_template('home.html', featured=products)


# GLOBAL SHOP PAGE (USER)

@app.route('/shop')
def shop():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Fetch all products
    products = query_all("SELECT * FROM products ORDER BY created_at DESC")

    # Fetch unique categories (if category column exists)
    try:
        categories = query_all("SELECT DISTINCT category FROM products WHERE category IS NOT NULL")
    except:
        categories = []

    return render_template('shop.html', products=products, categories=categories)

# ABOUT
@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

# PROFILE
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    if request.method == 'POST':
        execute("UPDATE users SET full_name=%s, contact_no=%s, address=%s WHERE id=%s",
                (request.form['full_name'], request.form['contact_no'],
                 request.form['address'], session['user_id']))
        flash('Profile updated successfully.')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)

# MEMBERSHIP
@app.route('/membership', methods=['GET', 'POST'])
def membership():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    if request.method == 'POST':
        membership = request.form['membership']
        execute("UPDATE users SET membership=%s WHERE id=%s", (membership, session['user_id']))
        flash('Membership updated.')
        return redirect(url_for('membership'))
    return render_template('membership.html', user=user)

# PRODUCTS (ADMIN CRUD)
@app.route('/products', methods=['GET', 'POST'])
@app.route('/products/<int:id>', methods=['GET', 'POST'])
def products(id=None):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # --- CREATE ---
    if request.method == 'POST' and id is None:
        execute("INSERT INTO products (name, description, price, stock_qty) VALUES (%s, %s, %s, %s)",
                (request.form['name'], request.form['description'], request.form['price'], request.form['stock_qty']))
        flash("Product added successfully.")
        return redirect(url_for('products'))

    # --- UPDATE ---
    if request.method == 'POST' and id:
        execute("UPDATE products SET name=%s, description=%s, price=%s, stock_qty=%s WHERE id=%s",
                (request.form['name'], request.form['description'], request.form['price'], request.form['stock_qty'], id))
        flash("Product updated successfully.")
        return redirect(url_for('products'))

    # --- DELETE ---
    if request.method == 'GET' and id:
        execute("DELETE FROM products WHERE id=%s", (id,))
        flash("Product deleted successfully.")
        return redirect(url_for('products'))

    # --- READ ---
    items = query_all("SELECT * FROM products ORDER BY created_at DESC")
    return render_template('products.html', products=items)

# ADD ORDER
@app.route('/order_add/<int:product_id>', methods=['POST'])
def order_add(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    product = query_one("SELECT * FROM products WHERE id=%s", (product_id,))
    if not product:
        flash("Product not found.")
        return redirect(url_for('home'))

    quantity = int(request.form.get('quantity', 1))
    total_price = float(product['price']) * quantity

    execute("""INSERT INTO orders (user_id, product_id, quantity, total_price)
               VALUES (%s, %s, %s, %s)""",
            (session['user_id'], product_id, quantity, total_price))

    flash("Order placed successfully.")
    return redirect(url_for('orders'))

# ORDERS PAGE
@app.route('/orders', methods=['GET'])
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    orders = query_all("""SELECT o.*, p.name AS product_name, p.price
                          FROM orders o
                          JOIN products p ON o.product_id = p.id
                          WHERE o.user_id=%s
                          ORDER BY o.order_date DESC""",
                       (session['user_id'],))
    return render_template('orders.html', orders=orders)

# ADMIN DASHBOARD
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    #Admin
    if session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('home'))

    # Get all products and orders
    products = query_all("SELECT * FROM products ORDER BY created_at DESC")
    orders = query_all("""SELECT o.id, u.username, p.name AS product_name, 
                                 o.quantity, o.total_price, o.order_date
                          FROM orders o
                          JOIN users u ON o.user_id = u.id
                          JOIN products p ON o.product_id = p.id
                          ORDER BY o.order_date DESC""")
    return render_template('admin_dashboard.html', products=products, orders=orders)


if __name__ == '__main__':
    app.run(debug=True)