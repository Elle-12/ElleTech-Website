import os
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from otp import send_otp_email, generate_otp, verify_otp, store_otp, send_and_store_otp
from db import get_db, query_all, query_one, execute
from datetime import datetime
import json
import random
from flask_socketio import SocketIO, emit, join_room

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='UI', static_folder='static')

# SocketIO configuration
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# --- Image upload config ---
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------------------
# Ensure SECRET_KEY exists
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    print("Warning: SECRET_KEY not set in environment; using random key for this run.")
    SECRET_KEY = os.urandom(24)
app.secret_key = SECRET_KEY

# Content dictionaries (unchanged)
login_content = {
    'title': 'Login to ElleTech',
    'username_placeholder': 'Username or Email',
    'password_placeholder': 'Password',
    'login_button': 'Login',
    'register_link_text': 'Don\'t have an account? Register here',
    'invalid_credentials': 'Invalid username or password.',
    'logo_alt': 'ElleTech Logo',
    'heading': 'Login to ElleTech',
    'no_account_text': 'Don\'t have an account?',
    'register_here': 'Register here'
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
    'orders_title': 'My Orders',
    'orders_subtitle': 'Track and manage all your purchases',
    'pending_orders_title': 'Pending Orders',
    'paid_orders_title': 'Paid Orders (Not Delivered Yet)',
    'delivered_orders_title': 'Delivered Orders',
    'uncategorized': 'Uncategorized',
    'quantity_label': 'Quantity:',
    'original_price_label': 'Original Price:',
    'discount_label': 'Discount:',
    'final_price_label': 'Final Price:',
    'payment_method_label': 'Payment Method:',
    'payment_status_label': 'Payment Status:',
    'order_date_label': 'Order Date:',
    'select_label': 'Select',
    'bulk_actions_title': 'Bulk Actions',
    'cancel_selected_button': 'Cancel Selected',
    'checkout_selected_button': 'Checkout Selected',
    'no_orders_title': 'No orders yet',
    'no_orders_text': 'You haven\'t placed any orders yet. Start shopping to see your orders here!',
    'start_shopping_button': 'Start Shopping',
    'complete_payment_title': 'Complete Payment',
    'payment_method_label_modal': 'Payment Method',
    'reference_label': 'Reference/Transaction ID',
    'payment_details_title': 'Payment Details',
    'gcash_label': 'GCash Number:',
    'paymaya_label': 'PayMaya Account:',
    'payment_instruction': 'Send the payment to the above account and enter the reference number to confirm.',
    'total_amount_label': 'Total Amount',
    'confirm_payment_button': 'Confirm Payment',
    'cash_on_delivery': 'Cash on Delivery',
    'gcash': 'GCash',
    'paymaya': 'PayMaya',
    'product_name_label': 'Product Name',
    'total_price_label': 'Total Price',
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
    'access_denied': 'Access denied. Admins only.',
    'total_products_label': 'Total Products',
    'total_orders_label': 'Total Orders',
    'total_users_label': 'Total Users'
}

landing_content = {
    'title': 'Welcome to ElleTech',
    'featured_products_title': 'Featured Products',
    'shop_now_button': 'Shop Now',
    'view_details_button': 'View Details',
    'login_button': 'Login',
    'register_button': 'Register',
    'welcome_message': 'Welcome to ElleTech - Your Tech Hub'
}

cart_content = {
    'title': 'Your Cart - ElleTech',
    'cart_title': 'Your Shopping Cart',
    'product_name_label': 'Product Name',
    'quantity_label': 'Quantity',
    'price_label': 'Price',
    'total_label': 'Total',
    'grand_total_label': 'Grand Total',
    'checkout_button': 'Checkout',
    'remove_button': 'Remove',
    'empty_cart_message': 'Your cart is empty.',
    'continue_shopping_button': 'Continue Shopping'
}

otp_verify_content = {
    'title': 'OTP Verification - ElleTech',
    'heading': 'Verify Your OTP',
    'otp_label': 'Enter OTP',
    'verify_button': 'Verify',
    'resend_button': 'Resend OTP',
    'invalid_otp': 'Invalid or expired OTP.',
    'otp_sent': 'OTP sent to your email.'
}

admin_products_content = {
    'title': 'Products Management - ElleTech',
    'products_title': 'Manage Products',
    'add_product_title': 'Add New Product',
    'name_label': 'Name',
    'description_label': 'Description',
    'price_label': 'Price',
    'stock_qty_label': 'Stock Quantity',
    'category_label': 'Category',
    'image_label': 'Image',
    'add_button': 'Add Product',
    'edit_button': 'Edit',
    'delete_button': 'Delete',
    'update_button': 'Update Product',
    'product_added': 'Product added successfully.',
    'product_updated': 'Product updated successfully.',
    'product_deleted': 'Product deleted successfully.',
    'name_required': 'Name is required.'
}

admin_orders_content = {
    'title': 'Orders Management - ElleTech',
    'orders_title': 'Manage Orders',
    'username_label': 'Username',
    'full_name_label': 'Full Name',
    'address_label': 'Address',
    'product_name_label': 'Product Name',
    'quantity_label': 'Quantity',
    'total_price_label': 'Total Price',
    'order_date_label': 'Order Date',
    'status_label': 'Status',
    'update_status_button': 'Update Status',
    'status_updated': 'Order status updated successfully.',
    'invalid_status': 'Invalid status.'
}

admin_shop_content = {
    'title': 'Admin Shop - ElleTech',
    'shop_title': 'All Products',
    'view_details_button': 'View Details'
}

layout_content = {
    'home_link': 'Home',
    'shop_link': 'Shop',
    'about_link': 'About',
    'profile_link': 'Profile',
    'orders_link': 'Orders',
    'cart_link': 'Cart',
    'membership_link': 'Membership',
    'logout_link': 'Logout',
    'admin_dashboard_link': 'Admin Dashboard',
    'admin_products_link': 'Manage Products',
    'admin_orders_link': 'Manage Orders',
    'admin_shop_link': 'Admin Shop'
}

ADMIN_ID = 1

# Store active users and their socket IDs
active_users = {}

# UTIL: login required decorator-like check
def require_login():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return None

def require_admin():
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))
    return None

# Initialize database tables (add is_read column to chats table)
def init_tables():
    """Initialize required database tables"""
    try:
        # Chat table with is_read column
        execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_id INT NOT NULL,
                receiver_id INT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (sender_id) REFERENCES users(id),
                FOREIGN KEY (receiver_id) REFERENCES users(id)
            )
        """)
        print("Chat table initialized successfully")
        
        # Ensure membership columns exist in users table
        try:
            execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS membership VARCHAR(50) DEFAULT 'Basic'")
            execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS membership_payment_status VARCHAR(50) DEFAULT 'paid'")
            print("Membership columns verified")
        except Exception as e:
            print(f"Membership columns already exist: {e}")
        
    except Exception as e:
        print(f"Error initializing tables: {e}")

# Initialize tables when app starts
init_tables()

# ROUTES (all routes remain exactly the same as in your original code)

@app.route('/')
def index():
    if 'user_id' not in session:
        products = query_all("SELECT * FROM products ORDER BY created_at DESC LIMIT 4")
        return render_template('landing.html', featured=products, content=landing_content)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        try:
            user = query_one("SELECT * FROM users WHERE username=%s OR email=%s", (username, username))
            if user and check_password_hash(user['password_hash'], password):
                # Send OTP for verification
                otp_code = send_and_store_otp(user['id'], user['email'], 'login')
                if otp_code:
                    session['pending_login'] = {
                        'user_id': user['id'],
                        'username': user['username'],
                        'role': user.get('role', 'user'),
                        'otp_code': otp_code
                    }
                    return redirect(url_for('otp_verify'))
                else:
                    msg = 'Failed to send OTP. Please try again.'
            else:
                msg = login_content['invalid_credentials']
        except Exception as e:
            msg = 'Database connection error. Please try again later.'
    return render_template('login.html', message=msg, content=login_content)

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

        # Create user directly
        user_id = execute("""INSERT INTO users (full_name, email, username, password_hash, contact_no, address, role)
                             VALUES (%s,%s,%s,%s,%s,%s,'user')""",
                          (full_name, email, username, password_hash, contact_no, address))
        if user_id:
            user = query_one("SELECT * FROM users WHERE id=%s", (user_id,))
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user.get('role', 'user')
                flash(register_content['success_message'])
                if session['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('home'))
            else:
                msg = 'Registration failed. Please try again.'
        else:
            msg = 'Registration failed. Please try again.'
    return render_template('register.html', message=msg, content=register_content)

@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    msg = ''
    if request.method == 'POST':
        otp_code = request.form.get('otp', '').strip()

        # Check for pending login
        if session.get('pending_login') and session['pending_login']['otp_code'] == otp_code:
            pending_login = session['pending_login']
            session['user_id'] = pending_login['user_id']
            session['username'] = pending_login['username']
            session['role'] = pending_login['role']
            session.pop('pending_login', None)
            flash('Login successful!')
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        # Check for pending forgot password
        elif session.get('pending_forgot_password') and session['pending_forgot_password']['otp_code'] == otp_code:
            pending_forgot = session['pending_forgot_password']
            session['reset_email'] = pending_forgot['email']
            session.pop('pending_forgot_password', None)
            return redirect(url_for('reset_password'))
    
    return render_template('otp_verify.html', message=msg, content=otp_verify_content)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    r = require_login()
    if r:
        return r
    products = query_all("SELECT * FROM products ORDER BY created_at DESC LIMIT 4")

    # Calculate stats for display
    total_products_row = query_one("SELECT COUNT(*) as count FROM products")
    if session.get('role') == 'admin':
        total_orders_row = query_one("SELECT COUNT(*) as count FROM orders")
    else:
        total_orders_row = query_one("SELECT COUNT(*) as count FROM orders WHERE user_id=%s", (session['user_id'],))
    total_users_row = query_one("SELECT COUNT(*) as count FROM users")

    total_products = total_products_row['count'] if total_products_row else 0
    total_orders = total_orders_row['count'] if total_orders_row else 0
    total_users = total_users_row['count'] if total_users_row else 0

    return render_template('home.html', featured=products, total_products=total_products, total_orders=total_orders, total_users=total_users, content=home_content)

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

    # Fetch unique categories
    try:
        categories = [row['category'] for row in query_all("SELECT DISTINCT category FROM products WHERE category IS NOT NULL")]
    except Exception:
        categories = []

    return render_template('shop.html', products=products, categories=categories, selected_category=category_filter, content=shop_content)

@app.route('/about')
def about():
    return render_template('about.html', content=about_content)

@app.route('/membership', methods=['GET', 'POST'])
def membership():
    r = require_login()
    if r:
        return r
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    
    if request.method == 'POST':
        membership_val = request.form.get('membership')
        payment_method = request.form.get('payment_method')
        
        if not membership_val:
            flash("Please select a membership level.")
            return redirect(url_for('membership'))
            
        # Update membership
        execute("UPDATE users SET membership=%s, membership_payment_status='unpaid' WHERE id=%s", 
                (membership_val, session['user_id']))
        
        if membership_val == 'Basic':
            # Basic is free, no payment needed
            execute("UPDATE users SET membership_payment_status='paid' WHERE id=%s", (session['user_id'],))
            flash("Membership updated to Basic. All basic benefits are now active!")
        else:
            flash(f"Membership updated to {membership_val}. Please complete payment to activate benefits.")
        
        return redirect(url_for('membership'))
    
    return render_template('membership.html', user=user, content=membership_content)

@app.route('/confirm_membership_payment', methods=['POST'])
def confirm_membership_payment():
    r = require_login()
    if r:
        return r
        
    payment_method = request.form.get('payment_method')
    reference = request.form.get('reference', '').strip()
    otp = request.form.get('otp', '').strip()
    
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    current_membership = user.get('membership')
    current_payment_status = user.get('membership_payment_status', 'unpaid')
    
    if not current_membership or current_payment_status != 'unpaid':
        flash("No unpaid membership to confirm.")
        return redirect(url_for('membership'))

    if payment_method == 'Cash on Delivery':
        # No OTP required for Cash on Delivery
        execute("UPDATE users SET membership_payment_status='paid' WHERE id=%s", (session['user_id'],))
        flash("Membership payment confirmed via Cash on Delivery. Your benefits are now active!")
        return redirect(url_for('membership'))
        
    elif payment_method in ['GCash', 'PayMaya']:
        if not reference:
            flash("Reference/Transaction ID is required for this payment method.")
            return redirect(url_for('membership'))
            
        if not otp:
            flash("OTP is required for digital payment verification.")
            return redirect(url_for('membership'))
            
        # Verify OTP
        if not verify_otp(session['user_id'], otp, otp_type='payment'):
            flash("Invalid or expired OTP. Please try again.")
            return redirect(url_for('membership'))
            
        # OTP verified, process payment
        execute("UPDATE users SET membership_payment_status='paid' WHERE id=%s", (session['user_id'],))
        flash(f"Membership payment confirmed! Your {current_membership} benefits are now active!")
        return redirect(url_for('membership'))
        
    else:
        flash("Invalid payment method.")
        return redirect(url_for('membership'))

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

# CART PAGE
@app.route('/cart')
def cart():
    r = require_login()
    if r:
        return r

    cart_items = query_all("""
        SELECT c.*, p.name AS product_name, p.price, p.image, (c.quantity * p.price) AS total_price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
        ORDER BY c.added_at DESC
    """, (session['user_id'],))

    # Convert total_price to Decimal for safety
    grand_total = sum(Decimal(item['total_price']) for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, grand_total=grand_total, content=cart_content)
                
# ADD TO CART
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    r = require_login()
    if r:
        return r

    product = query_one("SELECT * FROM products WHERE id=%s", (product_id,))
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('shop'))

    stock_qty = int(product.get('stock_qty', 0))
    if stock_qty <= 0:
        flash("Product out of stock.", "warning")
        return redirect(url_for('shop'))

    # Validate quantity
    try:
        quantity = int(request.form.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    if quantity > stock_qty:
        flash("Insufficient stock.", "warning")
        return redirect(url_for('shop'))

    payment_method = request.form.get('payment_method', 'Cash on Delivery')
    action = request.form.get('action')

    # BUY NOW LOGIC
    if action == 'buy_now':
        if session.get('role') == 'admin':
            flash("Admins cannot place orders.", "danger")
            return redirect(url_for('shop'))

        user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
        total_price = Decimal(product['price']) * Decimal(quantity)

        # Membership discount
        discount = Decimal('0')
        if user and user.get('membership') and user.get('membership_payment_status') == 'paid':
            if user['membership'] == 'Basic':
                discount = Decimal('0.05')
            elif user['membership'] == 'Gold':
                discount = Decimal('0.10')
            elif user['membership'] == 'Platinum':
                discount = Decimal('0.15')

        discounted_price = total_price * (Decimal('1') - discount)

        order_id = execute("""INSERT INTO orders
            (user_id, product_id, quantity, original_price, discount_applied, total_price, payment_method, payment_status, status, order_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'unpaid', 'pending', NOW())""",
            (session['user_id'], product_id, quantity, total_price, discount, discounted_price, payment_method)
        )

        if order_id:
            new_stock = stock_qty - quantity
            execute("UPDATE products SET stock_qty=%s WHERE id=%s", (new_stock, product_id))
            flash("Order placed successfully!", "success")
            return redirect(url_for('orders'))
        else:
            flash("Order failed.", "danger")
            return redirect(url_for('shop'))

    # ADD TO CART LOGIC
    existing = query_one("SELECT * FROM cart WHERE user_id=%s AND product_id=%s", (session['user_id'], product_id))
    if existing:
        new_quantity = existing['quantity'] + quantity
        if new_quantity > stock_qty:
            flash("Insufficient stock.", "warning")
            return redirect(url_for('shop'))
        execute("UPDATE cart SET quantity=%s WHERE id=%s", (new_quantity, existing['id']))
    else:
        execute("INSERT INTO cart (user_id, product_id, quantity, payment_method, added_at) VALUES (%s, %s, %s, %s, NOW())",
                (session['user_id'], product_id, quantity, payment_method))

    flash("Item added to cart.", "success")
    return redirect(url_for('cart'))

# REMOVE FROM CART
@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    r = require_login()
    if r:
        return r

    cart_item = query_one("SELECT * FROM cart WHERE id=%s AND user_id=%s", (cart_id, session['user_id']))
    if not cart_item:
        flash("Cart item not found.", "warning")
        return redirect(url_for('cart'))

    execute("DELETE FROM cart WHERE id=%s", (cart_id,))
    flash("Item removed from cart.", "success")
    return redirect(url_for('cart'))

# CHECKOUT
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    r = require_login()
    if r:
        return r

    if session.get('role') == 'admin':
        flash("Admins cannot place orders.", "danger")
        return redirect(url_for('home'))

    cart_items = query_all("""
        SELECT c.*, p.name AS product_name, p.price, p.stock_qty
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
        ORDER BY c.added_at DESC
    """, (session['user_id'],))

    if not cart_items:
        flash("Your cart is empty.", "info")
        return redirect(url_for('cart'))

    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))

    # Check stock for all items
    for item in cart_items:
        if item['quantity'] > item['stock_qty']:
            flash(f"Insufficient stock for {item['product_name']}.", "warning")
            return redirect(url_for('cart'))

    created_orders = []
    try:
        for item in cart_items:
            discount = Decimal('0')
            if user and user.get('membership') and user.get('membership_payment_status') == 'paid':
                if user['membership'] == 'Basic':
                    discount = Decimal('0.05')
                elif user['membership'] == 'Gold':
                    discount = Decimal('0.10')
                elif user['membership'] == 'Platinum':
                    discount = Decimal('0.15')

            total_price = Decimal(item['quantity']) * Decimal(item['price'])
            discounted_price = total_price * (Decimal('1') - discount)

            order_id = execute("""INSERT INTO orders
                (user_id, product_id, quantity, original_price, discount_applied, total_price, payment_method, payment_status, status, order_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'unpaid', 'pending', NOW())""",
                (session['user_id'], item['product_id'], item['quantity'], total_price, discount, discounted_price, item['payment_method'])
            )

            if order_id:
                created_orders.append(order_id)
                new_stock = int(item['stock_qty']) - item['quantity']
                execute("UPDATE products SET stock_qty=%s WHERE id=%s", (new_stock, item['product_id']))

        # Clear cart after success
        execute("DELETE FROM cart WHERE user_id=%s", (session['user_id'],))
        flash("Order placed successfully!", "success")
        return redirect(url_for('orders'))

    except Exception as e:
        # Rollback created orders
        for order_id in created_orders:
            order = query_one("SELECT * FROM orders WHERE id=%s", (order_id,))
            if order:
                product = query_one("SELECT * FROM products WHERE id=%s", (order['product_id'],))
                if product:
                    restored_stock = int(product['stock_qty']) + order['quantity']
                    execute("UPDATE products SET stock_qty=%s WHERE id=%s", (restored_stock, product['id']))
            execute("DELETE FROM orders WHERE id=%s", (order_id,))
        flash("Checkout failed. Please try again.", "danger")
        return redirect(url_for('cart'))

@app.route('/orders')
def orders():
    r = require_login()
    if r:
        return r
    orders = query_all("""
        SELECT o.*, p.name AS product_name, p.price, p.image, p.category
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.user_id=%s
        ORDER BY o.order_date DESC
    """, (session['user_id'],))
    return render_template('orders.html', orders=orders, content=orders_content)

@app.route('/cancel_selected_orders', methods=['POST'])
def cancel_selected_orders():
    r = require_login()
    if r:
        return r
    selected_orders = request.form.getlist('selected_orders')
    if not selected_orders:
        flash("No orders selected.")
        return redirect(url_for('orders'))
    cancelled_count = 0
    for order_id_str in selected_orders:
        try:
            order_id = int(order_id_str)
        except ValueError:
            continue
        order = query_one("SELECT * FROM orders WHERE id=%s AND user_id=%s AND status='pending'", (order_id, session['user_id']))
        if not order:
            continue
        # Restore stock quantity
        product = query_one("SELECT * FROM products WHERE id=%s", (order['product_id'],))
        if product:
            new_stock = int(product['stock_qty']) + order['quantity']
            execute("UPDATE products SET stock_qty=%s WHERE id=%s", (new_stock, order['product_id']))
        # Delete the order
        execute("DELETE FROM orders WHERE id=%s", (order_id,))
        cancelled_count += 1
    if cancelled_count > 0:
        flash(f"{cancelled_count} order(s) cancelled.")
    else:
        flash("No orders were cancelled.")
    return redirect(url_for('orders'))

@app.route('/complete_payment', methods=['POST'])
def complete_payment():
    r = require_login()
    if r:
        return r
    selected_orders = request.form.getlist('selected_orders')
    payment_method = request.form.get('payment_method')
    reference = request.form.get('reference', '').strip()
    if not selected_orders:
        flash("No orders selected.")
        return redirect(url_for('orders'))
    if not payment_method:
        flash("Payment method required.")
        return redirect(url_for('orders'))
    if payment_method in ['GCash', 'PayMaya'] and not reference:
        flash("Reference required for this payment method.")
        return redirect(url_for('orders'))
    updated_count = 0
    for order_id_str in selected_orders:
        try:
            order_id = int(order_id_str)
        except ValueError:
            continue
        order = query_one("SELECT * FROM orders WHERE id=%s AND user_id=%s AND payment_status='unpaid'", (order_id, session['user_id']))
        if order:
            execute("UPDATE orders SET payment_status='paid', payment_method=%s WHERE id=%s", (payment_method, order_id))
            updated_count += 1
    if updated_count > 0:
        flash(f"Payment confirmed for {updated_count} order(s).")
    else:
        flash("No orders updated.")
    return redirect(url_for('orders'))

@app.route('/admin_dashboard')
def admin_dashboard():
    r = require_login()
    if r:
        return r
    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))
    # Calculate stats
    total_products_row = query_one("SELECT COUNT(*) as count FROM products")
    total_orders_row = query_one("SELECT COUNT(*) as count FROM orders")
    total_users_row = query_one("SELECT COUNT(*) as count FROM users")
    total_products = total_products_row['count'] if total_products_row else 0
    total_orders = total_orders_row['count'] if total_orders_row else 0
    total_users = total_users_row['count'] if total_users_row else 0
    # Fetch product stocks (lowest first)
    products_stocks = query_all("SELECT id, name, stock_qty FROM products ORDER BY stock_qty ASC")
    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         products_stocks=products_stocks,
                         content=admin_dashboard_content)

@app.route('/admin_orders', methods=['GET', 'POST'])
def admin_orders():
    r = require_login()
    if r:
        return r
    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        status = request.form.get('status')
        if order_id and status:
            valid_statuses = ['pending', 'paid', 'delivered', 'cancelled']
            if status in valid_statuses:
                execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))
                flash(admin_orders_content['status_updated'])
            else:
                flash(admin_orders_content['invalid_status'])
        return redirect(url_for('admin_orders'))
    
    # Fetch all orders with user and product details - FIXED QUERY
    orders = query_all("""
        SELECT o.*, u.username, u.full_name as user_full_name, u.address as user_address, 
               p.name AS product_name, p.price, p.image
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN products p ON o.product_id = p.id
        ORDER BY o.order_date DESC
    """)
    return render_template('admin/admin_orders.html', orders=orders, content=admin_orders_content)

@app.route('/admin_products', methods=['GET', 'POST'], defaults={'product_id': None})
@app.route('/admin_products/<int:product_id>', methods=['GET', 'POST'])
def admin_products(product_id=None):
    r = require_login()
    if r:
        return r
    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))
    
    product = None
    if request.method == 'POST':
        # --- ADD PRODUCT ---
        if request.form.get('action') == 'add':
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
                flash(admin_products_content['name_required'])
                return redirect(url_for('admin_products'))
            try:
                product_id = execute("""INSERT INTO products (name, description, price, stock_qty, category, image, created_at)
                                       VALUES (%s, %s, %s, %s, %s, %s, NOW())""",
                                    (name, description, price, stock_qty, category, image_filename))
                if product_id:
                    flash(products_content['product_added'])
                else:
                    flash("Failed to add product. Please try again.")
            except Exception as e:
                flash("Database error: " + str(e))
            return redirect(url_for('admin_products'))
        
        # --- DELETE PRODUCT ---
        elif request.form.get('_method') == 'DELETE':
            delete_id = request.form.get('delete_id')
            if delete_id:
                execute("DELETE FROM products WHERE id=%s", (delete_id,))
                flash(products_content['product_deleted'])
            return redirect(url_for('admin_products'))
        
        # --- EDIT PRODUCT ---
        elif product_id is not None:
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            price = request.form.get('price', '0').strip()
            stock_qty = request.form.get('stock_qty', '0').strip()
            category = request.form.get('category')
            # Handle image upload
            image_filename = request.form.get('current_image')
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename
            execute("""UPDATE products SET name=%s, description=%s, price=%s, stock_qty=%s, category=%s, image=%s WHERE id=%s""",
                    (name, description, price, stock_qty, category, image_filename, product_id))
            flash(products_content['product_updated'])
            return redirect(url_for('admin_products'))
    
    # If editing a product, fetch its details
    if product_id is not None:
        product = query_one("SELECT * FROM products WHERE id=%s", (product_id,))
        if not product:
            flash("Product not found.")
            return redirect(url_for('admin_products'))
    
    # Fetch products for listing with search
    search_query = request.args.get('search', '').strip()
    if search_query:
        products = query_all("SELECT * FROM products WHERE name LIKE %s OR description LIKE %s ORDER BY created_at DESC",
                             ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        products = query_all("SELECT * FROM products ORDER BY created_at DESC")
    
    return render_template('admin/admin_products.html', 
                         products=products, 
                         product=product, 
                         content=admin_products_content, 
                         search_query=search_query)

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
    
    return render_template('admin/admin_shop.html', 
                         products=products, 
                         selected_category=category_filter,
                         content=admin_shop_content)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = query_one("SELECT * FROM users WHERE email=%s", (email,))
        if user:
            # Generate OTP
            otp_code = generate_otp()
            send_otp_email(email, otp_code)
            session['pending_forgot_password'] = {'email': email, 'otp_code': otp_code}
            flash('OTP sent to your email.')
            return redirect(url_for('otp_verify'))
        else:
            flash('Email not found.')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        if 'reset_email' not in session:
            flash("Unauthorized access. Please request password reset again.")
            return redirect(url_for('login'))
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        # 1. Empty fields
        if not password or not confirm_password:
            msg = "Password fields cannot be empty."
            return render_template('reset_password.html', message=msg)
        # 2. Password length
        if len(password) < 6:
            msg = "Password must be at least 6 characters long."
            return render_template('reset_password.html', message=msg)
        # 3. Passwords mismatch
        if password != confirm_password:
            msg = "Passwords do not match."
            return render_template('reset_password.html', message=msg)
        # --- UPDATE PASSWORD ---
        try:
            password_hash = generate_password_hash(password)
            execute("UPDATE users SET password_hash=%s WHERE email=%s",
                    (password_hash, session['reset_email']))
            session.pop('reset_email', None)
            flash("Password updated successfully! You can now login.")
            return redirect(url_for('login'))
        except Exception:
            msg = "Database error. Try again later."
            return render_template('reset_password.html', message=msg)
    return render_template('reset_password.html')

# -------------------------------------------------
#  PAYMENT OTP  (membership + orders)
# -------------------------------------------------

# ----------  AJAX: send OTP  ----------
@app.route('/request_order_payment_otp', methods=['POST'])
def request_order_payment_otp():
    try:
        if 'user_id' not in session: 
            return jsonify({'ok': False, 'msg': 'Login required'}), 403
        
        data = request.get_json(silent=True) or {}
        order_ids = data.get('order_ids', [])
        
        if not order_ids: 
            return jsonify({'ok': False, 'msg': 'No orders selected'}), 400
        
        # Verify orders belong to user and are unpaid
        placeholders = ','.join(['%s'] * len(order_ids))
        query = f"SELECT id FROM orders WHERE id IN ({placeholders}) AND user_id=%s AND payment_status='unpaid'"
        rows = query_all(query, (*order_ids, session['user_id']))
        
        if not rows: 
            return jsonify({'ok': False, 'msg': 'No eligible orders found'}), 400
        
        valid_order_ids = [r['id'] for r in rows]
        user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
        
        if not user or not user.get('email'):
            return jsonify({'ok': False, 'msg': 'User email not found'}), 400
        
        # Generate 8-digit OTP
        otp_code = str(random.randint(10000000, 99999999))  # 8-digit OTP
        
        meta = 'order-' + ','.join(map(str, valid_order_ids))
        
        # Try to send OTP email
        email_sent = send_otp_email(user['email'], otp_code, subject="ElleTech – Order Payment OTP (8-digit)")
        
        if email_sent:
            # Store OTP in JSON file
            store_otp(user['id'], otp_code, otp_type='payment', meta_info=meta)
            return jsonify({'ok': True, 'msg': '8-digit OTP sent to your email'})
        else:
            print(f"Failed to send OTP email to {user['email']}")
            return jsonify({'ok': False, 'msg': 'Failed to send OTP email. Please try again.'}), 500
            
    except Exception as e:
        print(f"Error in request_order_payment_otp: {str(e)}")
        return jsonify({'ok': False, 'msg': 'Internal server error. Please try again.'}), 500

@app.route('/request_membership_payment_otp', methods=['POST'])
def request_membership_payment_otp():
    try:
        if 'user_id' not in session: 
            return jsonify({'ok': False, 'msg': 'Login required'}), 403
        
        user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
        if not user or not user.get('membership') or user.get('membership_payment_status') != 'unpaid':
            return jsonify({'ok': False, 'msg': 'No unpaid membership found'}), 400
        
        if not user.get('email'):
            return jsonify({'ok': False, 'msg': 'User email not found'}), 400
        
        # Generate 8-digit OTP
        otp_code = str(random.randint(10000000, 99999999))  # 8-digit OTP
        
        # Try to send OTP email
        email_sent = send_otp_email(user['email'], otp_code, subject="ElleTech – Membership Payment OTP (8-digit)")
        
        if email_sent:
            store_otp(user['id'], otp_code, otp_type='payment', meta_info='membership')
            return jsonify({'ok': True, 'msg': '8-digit OTP sent to your email'})
        else:
            print(f"Failed to send OTP email to {user['email']}")
            return jsonify({'ok': False, 'msg': 'Failed to send OTP email. Please try again.'}), 500
    except Exception as e:
        print(f"Error in request_membership_payment_otp: {str(e)}")
        return jsonify({'ok': False, 'msg': 'Internal server error. Please try again.'}), 500

# ----------  AJAX: verify OTP  ----------
@app.route('/verify_payment_otp', methods=['POST'])
def verify_payment_otp():
    try:
        if 'user_id' not in session: 
            return jsonify({'ok': False, 'msg': 'Login required'}), 403
        
        data = request.get_json(silent=True) or {}
        otp = data.get('otp','').strip()
        purpose = data.get('purpose')
        order_ids = data.get('order_ids',[])

        # Validate 8-digit OTP format
        if not otp or len(otp) != 8 or not otp.isdigit():
            return jsonify({'ok': False, 'msg': 'Please enter a valid 8-digit OTP code'}), 400

        if not verify_otp(session['user_id'], otp, otp_type='payment'):
            return jsonify({'ok': False, 'msg': 'Invalid or expired OTP'}), 400

        if purpose == 'membership':
            execute("UPDATE users SET membership_payment_status='paid' WHERE id=%s", (session['user_id'],))
            return jsonify({'ok': True, 'msg': 'Membership payment confirmed!','redirect':url_for('membership')})

        if purpose == 'order' and order_ids:
            placeholders = ','.join(['%s'] * len(order_ids))
            execute(f"UPDATE orders SET payment_status='paid' WHERE id IN ({placeholders}) AND user_id=%s",
                    (*order_ids, session['user_id']))
            return jsonify({'ok': True, 'msg': 'Payment confirmed for selected orders!','redirect':url_for('orders')})

        return jsonify({'ok': False, 'msg': 'Unknown purpose'}), 400
    except Exception as e:
        print(f"Error in verify_payment_otp: {str(e)}")
        return jsonify({'ok': False, 'msg': 'Internal server error. Please try again.'}), 500

# -------------------------------------------------
#  REAL-TIME CHAT SYSTEM WITH SOCKETIO
# -------------------------------------------------

@socketio.on('connect')
def handle_connect():
    """Handle user connection"""
    if 'user_id' in session:
        user_id = session['user_id']
        active_users[user_id] = request.sid
        
        # Join user to their personal room
        join_room(f"user_{user_id}")
        
        # If admin, join admin room
        if session.get('role') == 'admin':
            join_room("admin_room")
        
        print(f"User {user_id} connected with SID: {request.sid}")
        
        # Notify admin about user online status
        if session.get('role') != 'admin':
            emit('user_online_status', {
                'user_id': user_id,
                'username': session.get('username'),
                'is_online': True
            }, room="admin_room", broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle user disconnection"""
    user_id = None
    for uid, sid in active_users.items():
        if sid == request.sid:
            user_id = uid
            break
    
    if user_id:
        del active_users[user_id]
        print(f"User {user_id} disconnected")
        
        # Notify admin about user offline status
        emit('user_online_status', {
            'user_id': user_id,
            'username': session.get('username'),
            'is_online': False
        }, room="admin_room", broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    """Handle sending messages in real-time"""
    try:
        if 'user_id' not in session:
            return
        
        sender_id = session['user_id']
        message = data.get('message', '').strip()
        receiver_id = data.get('receiver_id', ADMIN_ID)  # Default to admin for users
        
        # Validate message
        if not message:
            emit('error', {'message': 'Message cannot be empty'})
            return
        
        if len(message) > 1000:
            emit('error', {'message': 'Message too long'})
            return
        
        # Determine receiver based on who's sending
        if session.get('role') == 'admin':
            # Admin sending to user
            if not receiver_id or receiver_id == ADMIN_ID:
                emit('error', {'message': 'Invalid receiver'})
                return
        else:
            # User sending to admin
            receiver_id = ADMIN_ID
        
        # Save message to database
        message_id = execute("""
            INSERT INTO chats(sender_id, receiver_id, message, created_at, is_read) 
            VALUES (%s, %s, %s, %s, %s)
        """, (sender_id, receiver_id, message, datetime.now(), 0))
        
        if message_id:
            # Get message details with user info
            new_message = query_one("""
                SELECT c.*, u.username, u.full_name 
                FROM chats c 
                JOIN users u ON c.sender_id = u.id 
                WHERE c.id = %s
            """, (message_id,))
            
            if new_message:
                message_data = {
                    'id': new_message['id'],
                    'sender_id': new_message['sender_id'],
                    'sender_username': new_message['username'],
                    'sender_full_name': new_message['full_name'],
                    'message': new_message['message'],
                    'created_at': new_message['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                    'is_own': True
                }
                
                # Emit to sender (confirmation)
                emit('new_message', message_data, room=request.sid)
                
                # Emit to receiver
                if session.get('role') == 'admin':
                    # Admin sent to user - notify user
                    emit('new_message', {
                        **message_data,
                        'is_own': False
                    }, room=f"user_{receiver_id}")
                    
                    # Also notify admin room for other admin sessions
                    emit('new_message', message_data, room="admin_room")
                else:
                    # User sent to admin - notify admin
                    emit('new_message', {
                        **message_data,
                        'is_own': False
                    }, room="admin_room")
                
                # Update unread counts
                update_unread_counts(receiver_id)
                
        else:
            emit('error', {'message': 'Failed to send message'})
            
    except Exception as e:
        print(f"Error in handle_send_message: {str(e)}")
        emit('error', {'message': 'Internal server error'})

@socketio.on('mark_messages_read')
def handle_mark_messages_read(data):
    """Mark messages as read in real-time"""
    try:
        if 'user_id' not in session:
            return
        
        user_id = session['user_id']
        other_user_id = data.get('other_user_id')
        
        if not other_user_id:
            return
        
        # Mark messages as read
        execute("""
            UPDATE chats 
            SET is_read = 1 
            WHERE receiver_id = %s AND sender_id = %s AND is_read = 0
        """, (user_id, other_user_id))
        
        # Update unread counts
        update_unread_counts(user_id)
        
    except Exception as e:
        print(f"Error in handle_mark_messages_read: {str(e)}")

def update_unread_counts(user_id=None):
    """Update unread message counts for users and admin"""
    try:
        if user_id:
            # Update specific user's unread count
            user_count = query_one("""
                SELECT COUNT(*) as count 
                FROM chats 
                WHERE receiver_id = %s AND sender_id = %s AND is_read = 0
            """, (user_id, ADMIN_ID))
            
            emit('unread_count_update', {
                'count': user_count['count'] if user_count else 0
            }, room=f"user_{user_id}")
        
        # Always update admin's total unread count
        admin_count = query_one("""
            SELECT COUNT(*) as count 
            FROM chats 
            WHERE receiver_id = %s AND is_read = 0
        """, (ADMIN_ID,))
        
        emit('admin_unread_count_update', {
            'count': admin_count['count'] if admin_count else 0
        }, room="admin_room")
        
    except Exception as e:
        print(f"Error in update_unread_counts: {str(e)}")

# -------------------------------------------------
#  CHAT ROUTES (Updated for real-time)
# -------------------------------------------------

@app.route('/chat')
def chat():
    """User-side chat page."""
    r = require_login()
    if r:
        return r
    return render_template('chat.html')

@app.route('/get_messages')
def get_messages():
    """Return JSON of all messages between logged-in user and admin."""
    r = require_login()
    if r:
        return jsonify({'messages': []}), 403
    
    try:
        rows = query_all("""
            SELECT c.*, u.username AS sender_username, u.full_name AS sender_full_name
            FROM chats c
            JOIN users u ON c.sender_id = u.id
            WHERE (c.sender_id=%s AND c.receiver_id=%s)
               OR (c.sender_id=%s AND c.receiver_id=%s)
            ORDER BY c.created_at ASC
        """, (session['user_id'], ADMIN_ID, ADMIN_ID, session['user_id']))
        
        # Mark messages as read when user fetches them
        execute("""
            UPDATE chats 
            SET is_read = 1 
            WHERE receiver_id = %s AND sender_id = %s AND is_read = 0
        """, (session['user_id'], ADMIN_ID))
        
        # Update unread counts
        update_unread_counts(session['user_id'])
        
        # Format messages for frontend
        messages = []
        for row in rows:
            messages.append({
                'id': row['id'],
                'sender_id': row['sender_id'],
                'sender_username': row['sender_username'],
                'sender_full_name': row['sender_full_name'],
                'message': row['message'],
                'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                'is_own': row['sender_id'] == session['user_id'],
                'is_read': bool(row['is_read'])
            })
        
        return jsonify({'success': True, 'messages': messages})
    except Exception as e:
        print(f"Error in get_messages: {str(e)}")
        return jsonify({'success': False, 'messages': [], 'error': 'Failed to load messages'})

@app.route('/get_unread_count')
def get_unread_count():
    """Get count of unread messages for user."""
    r = require_login()
    if r:
        return jsonify({'count': 0})
    
    try:
        result = query_one("""
            SELECT COUNT(*) as count 
            FROM chats 
            WHERE receiver_id = %s AND sender_id = %s AND is_read = 0
        """, (session['user_id'], ADMIN_ID))
        
        return jsonify({'count': result['count'] if result else 0})
    except Exception as e:
        return jsonify({'count': 0})

# -------------------------------------------------
#  ADMIN CHAT (Updated for real-time)
# -------------------------------------------------

@app.route('/admin/chat')
def admin_chat():
    r = require_admin()
    if r:
        return r
    return render_template('admin/admin_chat.html')

@app.route('/admin_get_users')
def admin_get_users():
    """Return list of ALL users sorted by latest chat activity."""
    r = require_admin()
    if r:
        return jsonify({'users': []}), 403

    try:
        # Get ALL users except admin
        users_rows = query_all("""
            SELECT id, username, full_name, email, created_at 
            FROM users 
            WHERE id != %s AND role = 'user'
            ORDER BY created_at DESC
        """, (ADMIN_ID,))

        users = []
        for user_row in users_rows:
            # Get the latest chat timestamp between admin and user
            latest_chat_result = query_one("""
                SELECT created_at 
                FROM chats 
                WHERE (sender_id = %s AND receiver_id = %s) 
                   OR (sender_id = %s AND receiver_id = %s)
                ORDER BY created_at DESC 
                LIMIT 1
            """, (user_row['id'], ADMIN_ID, ADMIN_ID, user_row['id']))
            
            # Check if user has any chats with admin
            chat_exists = bool(latest_chat_result)
            
            # Get unread count (messages from user to admin that are unread)
            unread_result = query_one("""
                SELECT COUNT(*) as count 
                FROM chats 
                WHERE receiver_id = %s AND sender_id = %s AND is_read = 0
            """, (ADMIN_ID, user_row['id']))
            
            # Get last message between user and admin
            last_message_result = query_one("""
                SELECT message, created_at, sender_id
                FROM chats 
                WHERE (sender_id = %s AND receiver_id = %s) 
                   OR (sender_id = %s AND receiver_id = %s)
                ORDER BY created_at DESC 
                LIMIT 1
            """, (user_row['id'], ADMIN_ID, ADMIN_ID, user_row['id']))

            # Check if user is currently online
            is_online = user_row['id'] in active_users

            users.append({
                'id': user_row['id'],
                'username': user_row['username'],
                'full_name': user_row['full_name'] or user_row['username'],
                'email': user_row['email'],
                'unread_count': unread_result['count'] if unread_result else 0,
                'last_message': last_message_result['message'] if last_message_result else 'No messages yet',
                'last_message_time': latest_chat_result['created_at'] if latest_chat_result else None,
                'last_message_timestamp': latest_chat_result['created_at'].timestamp() if latest_chat_result else 0,
                'has_chatted': chat_exists,
                'member_since': user_row['created_at'].strftime('%Y-%m-%d') if user_row['created_at'] else 'Unknown',
                'is_own_last_message': last_message_result and last_message_result['sender_id'] == ADMIN_ID if last_message_result else False,
                'is_online': is_online
            })

        # Sort users: those with chats first (by latest message time), then new users (by registration date)
        users_with_chats = [u for u in users if u['has_chatted']]
        users_without_chats = [u for u in users if not u['has_chatted']]
        
        # Sort users with chats by latest message time (newest first)
        users_with_chats.sort(key=lambda x: x['last_message_timestamp'], reverse=True)
        # Sort users without chats by registration date (newest first)
        users_without_chats.sort(key=lambda x: x['member_since'], reverse=True)
        
        # Combine the lists
        sorted_users = users_with_chats + users_without_chats

        return jsonify({'success': True, 'users': sorted_users})
    except Exception as e:
        print(f"Error in admin_get_users: {str(e)}")
        return jsonify({'success': False, 'users': [], 'error': str(e)})

@app.route('/admin_get_messages')
def admin_get_messages():
    """Messages between admin and selected user."""
    r = require_admin()
    if r:
        return jsonify({'messages': []}), 403

    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'success': False, 'messages': [], 'error': 'User ID required'})

        # Verify user exists
        user = query_one("SELECT id, username, full_name FROM users WHERE id=%s", (user_id,))
        if not user:
            return jsonify({'success': False, 'messages': [], 'error': 'User not found'})

        # Mark messages as read when admin fetches them
        execute("""
            UPDATE chats 
            SET is_read = 1 
            WHERE receiver_id = %s AND sender_id = %s AND is_read = 0
        """, (ADMIN_ID, user_id))

        # Update unread counts
        update_unread_counts()

        # Get messages between admin and user
        rows = query_all("""
            SELECT c.*, 
                   u.username AS sender_username, 
                   u.full_name AS sender_full_name
            FROM chats c
            JOIN users u ON c.sender_id = u.id
            WHERE (c.sender_id = %s AND c.receiver_id = %s)
               OR (c.sender_id = %s AND c.receiver_id = %s)
            ORDER BY c.created_at ASC
        """, (user_id, ADMIN_ID, ADMIN_ID, user_id))

        messages = []
        for row in rows:
            messages.append({
                'id': row['id'],
                'sender_id': row['sender_id'],
                'sender_username': row['sender_username'],
                'sender_full_name': row['sender_full_name'],
                'message': row['message'],
                'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                'is_own': row['sender_id'] == ADMIN_ID,
                'is_read': bool(row['is_read'])
            })

        return jsonify({'success': True, 'messages': messages, 'user_info': {
            'username': user['username'],
            'full_name': user['full_name'],
            'is_online': user_id in active_users
        }})
    except Exception as e:
        print(f"Error in admin_get_messages: {str(e)}")
        return jsonify({'success': False, 'messages': [], 'error': 'Failed to load messages'})

@app.route('/admin_send_message', methods=['POST'])
def admin_send_message():
    """Admin sends a message to a user."""
    r = require_admin()
    if r:
        return jsonify({'success': False, 'error': 'Admin access required'}), 403

    try:
        # Get JSON data properly
        if request.content_type != 'application/json':
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'})
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'})
        
        msg = data.get('message', '').strip()
        receiver_id = data.get('receiver_id')
        
        # Convert receiver_id to integer if it's not None
        if receiver_id is not None:
            try:
                receiver_id = int(receiver_id)
            except (ValueError, TypeError):
                return jsonify({'success': False, 'error': 'Invalid receiver ID'})

        print(f"Admin sending message: '{msg}' to user: {receiver_id}")

        if not msg:
            return jsonify({'success': False, 'error': 'Message cannot be empty'})

        if not receiver_id:
            return jsonify({'success': False, 'error': 'Receiver ID required'})

        if len(msg) > 1000:
            return jsonify({'success': False, 'error': 'Message too long (max 1000 characters)'})

        # Verify receiver exists
        receiver = query_one("SELECT id, username, full_name FROM users WHERE id=%s", (receiver_id,))
        if not receiver:
            return jsonify({'success': False, 'error': 'User not found'})

        # Insert message - admin sends to user
        message_id = execute("""
            INSERT INTO chats (sender_id, receiver_id, message, created_at, is_read) 
            VALUES (%s, %s, %s, %s, %s)
        """, (ADMIN_ID, receiver_id, msg, datetime.now(), 0))

        print(f"Message inserted with ID: {message_id}")

        if message_id:
            return jsonify({'success': True, 'message': 'Message sent successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to send message - database error'})

    except Exception as e:
        print(f"Error in admin_send_message: {str(e)}")
        return jsonify({'success': False, 'error': f'Internal server error: {str(e)}'})

@app.route('/admin_get_unread_count')
def admin_get_unread_count():
    """Get total unread messages for admin."""
    r = require_admin()
    if r:
        return jsonify({'count': 0})
    
    try:
        result = query_one("""
            SELECT COUNT(*) as count 
            FROM chats 
            WHERE receiver_id = %s AND is_read = 0
        """, (ADMIN_ID,))
        
        return jsonify({'count': result['count'] if result else 0})
    except Exception as e:
        return jsonify({'count': 0})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))