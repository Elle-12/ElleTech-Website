import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='UI', static_folder='static')

# --- Image upload config ---
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------------------
# Ensure SECRET_KEY exists (fallback to random but warn in logs)
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    print("Warning: SECRET_KEY not set in environment; using random key for this run.")
    SECRET_KEY = os.urandom(24)
app.secret_key = SECRET_KEY

login_content = {
    'title': 'Login to ElleTech',
    'username_placeholder': 'Username or Email',
    'password_placeholder': 'Password',
    'login_button': 'Login',
    'register_link_text': 'Don\'t have an account? Register here',
    'invalid_credentials': 'Invalid username or password.'
}

register_content = {
    'title': 'Register for ElleTech',
    'full_name_placeholder': 'Full Name',
    'email_placeholder': 'Email',
    'username_placeholder': 'Username',
    'password_placeholder': 'Password',
    'contact_no_placeholder': 'Contact Number',
    'address_placeholder': 'Address',
    'register_button': 'Register',
    'login_link_text': 'Already have an account? Login here',
    'success_message': 'Registered successfully! You can log in now.'
}

home_content = {
    'title': 'Welcome to ElleTech',
    'featured_products_title': 'Featured Products',
    'shop_now_button': 'Shop Now',
    'view_details_button': 'View Details'
}

shop_content = {
    'title': 'Shop - ElleTech',
    'all_products_title': 'All Products',
    'add_to_cart_button': 'Add to Cart',
    'view_details_button': 'View Details'
}

about_content = {
    'title': 'About Us - ElleTech',
    'about_title': 'About ElleTech',
    'about_text': 'ElleTech is a leading technology company providing innovative solutions...'
}

profile_content = {
    'title': 'Profile - ElleTech',
    'profile_title': 'Your Profile',
    'full_name_label': 'Full Name',
    'contact_no_label': 'Contact Number',
    'address_label': 'Address',
    'update_button': 'Update Profile',
    'update_success': 'Profile updated successfully.'
}

membership_content = {
    'title': 'Membership - ElleTech',
    'membership_title': 'Membership Options',
    'select_membership_label': 'Select Membership',
    'update_button': 'Update Membership',
    'update_success': 'Membership updated.'
}

products_content = {
    'title': 'Products Management - ElleTech',
    'products_title': 'Manage Products',
    'add_product_title': 'Add New Product',
    'name_label': 'Name',
    'description_label': 'Description',
    'price_label': 'Price',
    'stock_qty_label': 'Stock Quantity',
    'add_button': 'Add Product',
    'edit_button': 'Edit',
    'delete_button': 'Delete',
    'update_button': 'Update Product',
    'product_added': 'Product added successfully.',
    'product_updated': 'Product updated successfully.',
    'product_deleted': 'Product deleted successfully.'
}

orders_content = {
    'title': 'Your Orders - ElleTech',
    'orders_title': 'Your Orders',
    'product_name_label': 'Product Name',
    'quantity_label': 'Quantity',
    'total_price_label': 'Total Price',
    'order_date_label': 'Order Date',
    'order_placed': 'Order placed successfully.'
}

admin_dashboard_content = {
    'title': 'Admin Dashboard - ElleTech',
    'dashboard_title': 'Admin Dashboard',
    'products_section_title': 'Products',
    'orders_section_title': 'Orders',
    'username_label': 'Username',
    'product_name_label': 'Product Name',
    'quantity_label': 'Quantity',
    'total_price_label': 'Total Price',
    'order_date_label': 'Order Date',
    'access_denied': 'Access denied. Admins only.'
}

# DATABASE CONNECTION
def get_db():
    try:
        # Convert port to int if provided
        db_port = os.getenv("DB_PORT")
        if db_port:
            try:
                db_port = int(db_port)
            except ValueError:
                # keep as string and let connector decide
                pass

        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=db_port,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            autocommit=False  # control commits explicitly
        )
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        raise


# DATABASE HELPERS
def query_all(query, params=()):
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)
        data = cur.fetchall()
        return data
    finally:
        cur.close()
        conn.close()


def query_one(query, params=()):
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)
        row = cur.fetchone()
        return row
    finally:
        cur.close()
        conn.close()


def execute(query, params=()):
    """Execute a write query and return lastrowid (if available)."""
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        lastrowid = getattr(cur, 'lastrowid', None)
        return lastrowid
    except Exception as e:
        conn.rollback()
        print("Database execute error:", e)
        raise
    finally:
        cur.close()
        conn.close()


# UTIL: login required decorator-like check (simple)
def require_login():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return None


def require_admin():
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))
    return None


# ROUTES

@app.route('/')
def index():
    # Redirect based on login status
    if 'user_id' not in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = query_one("SELECT * FROM users WHERE username=%s OR email=%s", (username, username))
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user.get('role', 'user')
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            msg = login_content['invalid_credentials']
    return render_template('login.html', message=msg, content=login_content)


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password_raw = request.form.get('password', '')
        contact_no = request.form.get('contact_no', '').strip()
        address = request.form.get('address', '').strip()

        if not all([full_name, email, username, password_raw]):
            msg = 'Please fill in required fields.'
            return render_template('register.html', message=msg, content=register_content)

        password_hash = generate_password_hash(password_raw)

        existing = query_one("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
        if existing:
            msg = 'Username or email already exists.'
            return render_template('register.html', message=msg, content=register_content)

        execute("""INSERT INTO users (full_name, email, username, password_hash, contact_no, address, role)
                   VALUES (%s,%s,%s,%s,%s,%s,'user')""",
                (full_name, email, username, password_hash, contact_no, address))
        flash(register_content['success_message'])
        return redirect(url_for('login'))
    return render_template('register.html', message=msg, content=register_content)


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# HOME
@app.route('/home')
def home():
    r = require_login()
    if r:
        return r
    products = query_all("SELECT * FROM products ORDER BY created_at DESC LIMIT 4")
    return render_template('home.html', featured=products, content=home_content)


# GLOBAL SHOP PAGE (USER)
@app.route('/shop')
def shop():
    r = require_login()
    if r:
        return r

    category_filter = request.args.get('category', '')

    # Fetch products based on category filter
    if category_filter:
        products = query_all("SELECT * FROM products WHERE category=%s ORDER BY created_at DESC", (category_filter,))
    else:
        products = query_all("SELECT * FROM products ORDER BY created_at DESC")

    # Fetch unique categories (if category column exists)
    try:
        categories = [row['category'] for row in query_all("SELECT DISTINCT category FROM products WHERE category IS NOT NULL")]
    except Exception:
        categories = []

    return render_template('shop.html', products=products, categories=categories, selected_category=category_filter, content=shop_content)


# ABOUT
@app.route('/about')
def about():
    r = require_login()
    if r:
        return r
    return render_template('about.html', content=about_content)


# PROFILE DISPLAY AND EDIT
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    r = require_login()
    if r:
        return r
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    if request.method == 'POST':
        profile_pic_filename = user.get('profile_pic')  # Keep existing
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_pic_filename = filename

        execute("UPDATE users SET full_name=%s, contact_no=%s, address=%s, profile_pic=%s WHERE id=%s",
                (request.form.get('full_name'), request.form.get('contact_no'),
                 request.form.get('address'), profile_pic_filename, session['user_id']))
        flash(profile_content['update_success'])
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user, content=profile_content)

# MEMBERSHIP
@app.route('/membership', methods=['GET', 'POST'])
def membership():
    r = require_login()
    if r:
        return r
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    if request.method == 'POST':
        membership_val = request.form.get('membership')
        execute("UPDATE users SET membership=%s WHERE id=%s", (membership_val, session['user_id']))
        flash(membership_content['update_success'])
        return redirect(url_for('membership'))
    return render_template('membership.html', user=user, content=membership_content)

# ORDERS PAGE
@app.route('/orders', methods=['GET'])
def orders():
    r = require_login()
    if r:
        return r
    orders = query_all("""SELECT o.*, p.name AS product_name, p.price, p.image
                          FROM orders o
                          JOIN products p ON o.product_id = p.id
                          WHERE o.user_id=%s
                          ORDER BY o.order_date DESC""",
                       (session['user_id'],))
    return render_template('orders.html', orders=orders, content=orders_content)
                
# PLACE ORDER
@app.route('/place_order/<int:product_id>', methods=['POST'])
def place_order(product_id):
    r = require_login()
    if r:
        return r
    product = query_one("SELECT * FROM products WHERE id=%s", (product_id,))
    if not product:
        flash("Product not found.")
        return redirect(url_for('shop'))

    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1

    payment_method = request.form.get('payment_method', 'Cash on Delivery')

    # ensure price numeric
    try:
        price = float(product.get('price', 0))
    except Exception:
        price = 0.0

    total_price = price * quantity

    execute("""INSERT INTO orders (user_id, product_id, quantity, total_price, payment_method, payment_status, order_date)
               VALUES (%s, %s, %s, %s, %s, 'unpaid', NOW())""",
            (session['user_id'], product_id, quantity, total_price, payment_method))

    flash(orders_content['order_placed'])
    return redirect(url_for('orders'))

# PRODUCTS (ADMIN CRUD)
@app.route('/admin_products', methods=['GET', 'POST'])
@app.route('/admin_products/<int:id>', methods=['GET', 'POST'])
def admin_products(id=None):
    r = require_login()
    if r:
        return r

    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))

    # --- CREATE NEW PRODUCT ---
    if request.method == 'POST' and id is None:
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '0').strip()
        stock_qty = request.form.get('stock_qty', '0').strip()
        category = request.form.get('category')

        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename

        if not name:
            flash("Name is required.")
            return redirect(url_for('admin_products'))

        execute("""INSERT INTO products (name, description, price, stock_qty, category, image, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, NOW())""",
                (name, description, price, stock_qty, category, image_filename))
        flash(products_content['product_added'])
        return redirect(url_for('admin_products'))

    # --- EDIT / VIEW A SINGLE PRODUCT ---
    if id is not None:
        product = query_one("SELECT * FROM products WHERE id=%s", (id,))
        if not product:
            flash("Product not found.")
            return redirect(url_for('admin_products'))

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            price = request.form.get('price', '0').strip()
            stock_qty = request.form.get('stock_qty', '0').strip()
            category = request.form.get('category')

            # Handle image update
            image_filename = product['image']  # Keep existing image
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename

            execute("""UPDATE products SET name=%s, description=%s, price=%s, stock_qty=%s, category=%s, image=%s
                       WHERE id=%s""",
                    (name, description, price, stock_qty, category, image_filename, id))
            flash(products_content['product_updated'])
            return redirect(url_for('admin_products'))

        # GET single product -> show edit form
        return render_template('admin/product_edit.html', product=product, content=products_content)

    # --- LIST ALL PRODUCTS ---
    products_list = query_all("SELECT * FROM products ORDER BY created_at DESC")
    return render_template('admin/admin_products.html', products=products_list, content=products_content)


@app.route('/admin_products/delete/<int:id>', methods=['POST'])
def admin_products_delete(id):
    r = require_login()
    if r:
        return r

    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))

    # Delete product
    execute("DELETE FROM products WHERE id=%s", (id,))
    flash(products_content['product_deleted'])
    return redirect(url_for('admin_products'))


# UPDATE ORDER PAYMENT METHOD
@app.route('/update_order_payment/<int:order_id>', methods=['POST'])
def update_order_payment(order_id):
    r = require_login()
    if r:
        return r

    # Ensure the order belongs to the user
    order = query_one("SELECT * FROM orders WHERE id=%s AND user_id=%s", (order_id, session['user_id']))
    if not order:
        flash("Order not found.")
        return redirect(url_for('orders'))

    payment_method = request.form.get('payment_method')
    if payment_method not in ['Cash on Delivery', 'GCash', 'PayMaya']:
        flash("Invalid payment method.")
        return redirect(url_for('orders'))

    execute("UPDATE orders SET payment_method=%s, payment_status='unpaid' WHERE id=%s", (payment_method, order_id))
    flash("Payment method updated successfully.")
    return redirect(url_for('orders'))


# CONFIRM PAYMENT
@app.route('/confirm_payment/<int:order_id>', methods=['POST'])
def confirm_payment(order_id):
    r = require_login()
    if r:
        return r

    # Ensure the order belongs to the user
    order = query_one("SELECT * FROM orders WHERE id=%s AND user_id=%s", (order_id, session['user_id']))
    if not order:
        flash("Order not found.")
        return redirect(url_for('orders'))

    reference = request.form.get('reference', '').strip()
    if not reference:
        flash("Reference/Transaction ID is required.")
        return redirect(url_for('orders'))

    # Update payment status to paid
    execute("UPDATE orders SET payment_status='paid' WHERE id=%s", (order_id,))
    flash("Payment confirmed successfully. Reference: " + reference)
    return redirect(url_for('orders'))


# ADMIN DASHBOARD
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    r = require_login()
    if r:
        return r

    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))

    # Get stats for dashboard - handle None cases
    total_products_row = query_one("SELECT COUNT(*) as count FROM products")
    total_orders_row = query_one("SELECT COUNT(*) as count FROM orders")
    total_users_row = query_one("SELECT COUNT(*) as count FROM users")

    total_products = total_products_row['count'] if total_products_row else 0
    total_orders = total_orders_row['count'] if total_orders_row else 0
    total_users = total_users_row['count'] if total_users_row else 0

    return render_template('admin/dashboard.html',
                           total_products=total_products,
                           total_orders=total_orders,
                           total_users=total_users,
                           content=admin_dashboard_content)


@app.route('/admin_shop')
def admin_shop():
    r = require_login()
    if r:
        return r

    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))

    category_filter = request.args.get('category', '')

    # Fetch products based on category filter
    if category_filter:
        products = query_all("SELECT * FROM products WHERE category=%s ORDER BY created_at DESC", (category_filter,))
    else:
        products = query_all("SELECT * FROM products ORDER BY created_at DESC")

    # Fetch unique categories (if category column exists)
    try:
        categories = [row['category'] for row in query_all("SELECT DISTINCT category FROM products WHERE category IS NOT NULL")]
    except Exception:
        categories = []

    return render_template('admin/admin_shop.html', products=products, categories=categories, selected_category=category_filter, content=shop_content)


# ADMIN ORDERS
@app.route('/admin_orders', methods=['GET'])
def admin_orders():
    r = require_login()
    if r:
        return r

    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))

    # Fetch all orders with user and product info
    orders = query_all("""SELECT o.*, u.username AS user_name, u.full_name AS user_full_name, u.address AS user_address, p.name AS product_name, p.image AS image
                          FROM orders o
                          JOIN users u ON o.user_id = u.id
                          JOIN products p ON o.product_id = p.id
                          ORDER BY o.order_date DESC""")

    return render_template('admin/admin_orders.html', orders=orders, content=admin_dashboard_content)


# UPDATE ORDER STATUS (ADMIN)
@app.route('/admin_update_order_status/<int:order_id>', methods=['POST'])
def admin_update_order_status(order_id):
    r = require_login()
    if r:
        return r

    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))

    status = request.form.get('status')
    if status not in ['pending', 'shipped', 'delivered']:
        flash('Invalid status.')
        return redirect(url_for('admin_orders'))

    # If status is 'delivered', also mark payment as paid
    if status == 'delivered':
        execute("UPDATE orders SET status=%s, payment_status='paid' WHERE id=%s", (status, order_id))
        flash('Order status updated to delivered and payment marked as paid.')
    else:
        execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))
        flash('Order status updated successfully.')

    return redirect(url_for('admin_orders'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
