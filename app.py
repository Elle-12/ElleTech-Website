import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from otp import send_otp_email, generate_otp, verify_otp, store_otp, send_and_store_otp
from db import get_db, query_all, query_one, execute

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
                # Generate OTP and send it for login verification
                otp_code = generate_otp()
                if send_otp_email(user['email'], otp_code, "Your OTP for ElleTech Login"):
                    # Store pending login data in session
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

        # Generate OTP and send it
        otp_code = generate_otp()
        if send_otp_email(email, otp_code, "Your OTP for ElleTech Registration"):
            # Store OTP temporarily in session (since user not created yet)
            session['pending_registration'] = {
                'full_name': full_name,
                'email': email,
                'username': username,
                'password_hash': password_hash,
                'contact_no': contact_no,
                'address': address,
                'otp_code': otp_code
            }
            return redirect(url_for('otp_verify'))
        else:
            msg = 'Failed to send OTP. Please try again.'
            return render_template('register.html', message=msg, content=register_content)

    return render_template('register.html', message=msg, content=register_content)

# OTP VERIFICATION
@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    msg = ''
    if request.method == 'POST':
        otp_code = request.form.get('otp', '').strip()

        # Check for pending registration
        pending_reg = session.get('pending_registration')
        if pending_reg and pending_reg['otp_code'] == otp_code:
            # Check if email already exists
            existing = query_one("SELECT * FROM users WHERE email=%s", (pending_reg['email'],))
            if existing:
                msg = 'Email already exists.'
                session.pop('pending_registration', None)
                return render_template('otp_verify.html', message=msg, content=otp_verify_content)
            # Create the user
            user_id = execute("""INSERT INTO users (full_name, email, username, password_hash, contact_no, address, role)
                                 VALUES (%s,%s,%s,%s,%s,%s,'user')""",
                              (pending_reg['full_name'], pending_reg['email'], pending_reg['username'],
                               pending_reg['password_hash'], pending_reg['contact_no'], pending_reg['address']))
            if user_id:
                user = query_one("SELECT * FROM users WHERE id=%s", (user_id,))
                if user:
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user.get('role', 'user')
                    session.pop('pending_registration', None)
                    flash(register_content['success_message'])
                    if session['role'] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    else:
                        return redirect(url_for('home'))
                else:
                    msg = 'Registration failed. Please try again.'
            else:
                msg = 'Registration failed. Please try again.'
        # Check for pending login
        elif session.get('pending_login') and session['pending_login']['otp_code'] == otp_code:
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
        else:
            msg = otp_verify_content['invalid_otp']
    return render_template('otp_verify.html', message=msg, content=otp_verify_content)

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

@app.route('/membership', methods=['GET', 'POST'])
def membership():
    r = require_login()
    if r:
        return r
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    if request.method == 'POST':
        membership_val = request.form.get('membership')
        payment_method = request.form.get('payment_method')

        # If upgrading to paid membership, set payment status to unpaid
        if membership_val in ['Silver', 'Gold', 'Platinum']:
            execute("UPDATE users SET membership=%s, membership_payment_status='unpaid' WHERE id=%s",
                    (membership_val, session['user_id']))
            flash("Membership upgrade initiated. Please complete payment.")
        else:
            execute("UPDATE users SET membership=%s WHERE id=%s",
                    (membership_val, session['user_id']))
            flash(membership_content['update_success'])
        return redirect(url_for('membership'))
    return render_template('membership.html', user=user, content=membership_content)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    r = require_login()
    if r:
        return r
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        contact_no = request.form.get('contact_no', '').strip()
        address = request.form.get('address', '').strip()

        profile_pic_filename = user['profile_pic']  # Default to existing
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_pic_filename = filename

        execute("UPDATE users SET full_name=%s, contact_no=%s, address=%s, profile_pic=%s WHERE id=%s",
                (full_name, contact_no, address, profile_pic_filename, session['user_id']))
        flash(profile_content['update_success'])
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user, content=profile_content)

@app.route('/confirm_membership_payment', methods=['POST'])
def confirm_membership_payment():
    r = require_login()
    if r:
        return r

    reference = request.form.get('reference', '').strip()
    if not reference:
        flash("Reference/Transaction ID is required.")
        return redirect(url_for('membership'))

    execute("UPDATE users SET membership_payment_status='paid' WHERE id=%s", (session['user_id'],))
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    flash("Membership payment confirmed. Welcome to " + user['membership'] + "!")
    return redirect(url_for('membership'))

# ORDERS PAGE
@app.route('/orders', methods=['GET'])
def orders():
    r = require_login()
    if r:
        return r
    orders = query_all("""SELECT o.*, p.name AS product_name, p.price, p.image, p.category
                          FROM orders o
                          JOIN products p ON o.product_id = p.id
                          WHERE o.user_id=%s
                          ORDER BY o.order_date DESC""",
                       (session['user_id'],))
    return render_template('orders.html', orders=orders, content=orders_content)

# ADD TO CART
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    r = require_login()
    if r:
        return r

    product = query_one("SELECT * FROM products WHERE id=%s", (product_id,))
    if not product:
        flash("Product not found.")
        return redirect(url_for('shop'))

    # Check stock availability
    stock_qty = int(product.get('stock_qty', 0))
    if stock_qty <= 0:
        flash("This product is out of stock.")
        return redirect(url_for('shop'))

    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1

    if quantity > stock_qty:
        flash(f"Only {stock_qty} items available in stock.")
        return redirect(url_for('shop'))

    payment_method = request.form.get('payment_method', 'Cash on Delivery')

    # Check if item already in cart
    existing = query_one("SELECT * FROM cart WHERE user_id=%s AND product_id=%s", (session['user_id'], product_id))
    if existing:
        # Update quantity
        new_quantity = existing['quantity'] + quantity
        if new_quantity > stock_qty:
            flash(f"Only {stock_qty} items available in stock.")
            return redirect(url_for('shop'))
        execute("UPDATE cart SET quantity=%s WHERE id=%s", (new_quantity, existing['id']))
    else:
        # Add new item to cart
        execute("INSERT INTO cart (user_id, product_id, quantity, payment_method) VALUES (%s, %s, %s, %s)",
                (session['user_id'], product_id, quantity, payment_method))

    flash("Item added to cart.")
    return redirect(url_for('cart'))

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

    grand_total = sum(item['total_price'] for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, grand_total=grand_total)

# REMOVE FROM CART
@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    r = require_login()
    if r:
        return r

    # Ensure the cart item belongs to the user
    cart_item = query_one("SELECT * FROM cart WHERE id=%s AND user_id=%s", (cart_id, session['user_id']))
    if not cart_item:
        flash("Cart item not found.")
        return redirect(url_for('cart'))

    execute("DELETE FROM cart WHERE id=%s", (cart_id,))
    flash("Item removed from cart.")
    return redirect(url_for('cart'))

# CHECKOUT
@app.route('/checkout', methods=['POST'])
def checkout():
    r = require_login()
    if r:
        return r

    cart_items = query_all("SELECT * FROM cart WHERE user_id=%s", (session['user_id'],))
    if not cart_items:
        return redirect(url_for('cart'))

    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))

    # Step 1: Validate all stock availability first
    for item in cart_items:
        product = query_one("SELECT * FROM products WHERE id=%s", (item['product_id'],))
        if not product:
            flash("Product not found.")
            return redirect(url_for('cart'))

        stock_qty = int(product.get('stock_qty', 0))
        if item['quantity'] > stock_qty:
            flash("Insufficient stock for some items.")
            return redirect(url_for('cart'))

    # Step 2: Process all orders and update stock
    created_orders = []
    try:
        for item in cart_items:
            product = query_one("SELECT * FROM products WHERE id=%s", (item['product_id'],))

            # Calculate prices
            price = float(product.get('price', 0))
            total_price = price * item['quantity']

            discount = 0.0
            if user and user['membership']:
                if user['membership'] == 'Silver':
                    discount = 0.05
                elif user['membership'] == 'Gold':
                    discount = 0.10
                elif user['membership'] == 'Platinum':
                    discount = 0.15

            discounted_price = total_price * (1 - discount)

            # Insert order first
            order_id = execute("""INSERT INTO orders (user_id, product_id, quantity, original_price, discount_applied, total_price, payment_method, payment_status, status, order_date)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, 'unpaid', 'pending', NOW())""",
                               (session['user_id'], item['product_id'], item['quantity'], total_price, discount, discounted_price, item['payment_method']))

            if order_id:
                created_orders.append(order_id)

                # Decrement stock only after successful order creation
                new_stock = int(product.get('stock_qty', 0)) - item['quantity']
                execute("UPDATE products SET stock_qty=%s WHERE id=%s", (new_stock, item['product_id']))
            else:
                raise Exception("Failed to create order")

        # Step 3: Clear the cart after successful checkout
        execute("DELETE FROM cart WHERE user_id=%s", (session['user_id'],))

        flash("Order placed successfully!")
        return redirect(url_for('orders'))

    except Exception as e:
        # Rollback: Restore stock for created orders
        for order_id in created_orders:
            order = query_one("SELECT * FROM orders WHERE id=%s", (order_id,))
            if order:
                product = query_one("SELECT * FROM products WHERE id=%s", (order['product_id'],))
                if product:
                    restored_stock = int(product.get('stock_qty', 0)) + order['quantity']
                    execute("UPDATE products SET stock_qty=%s WHERE id=%s", (restored_stock, order['product_id']))

                # Delete the order
                execute("DELETE FROM orders WHERE id=%s", (order_id,))

        flash("Checkout failed. Please try again.")
        return redirect(url_for('cart'))

# PLACE ORDER (direct order from shop)
@app.route('/place_order/<int:product_id>', methods=['POST'])
def place_order(product_id):
    r = require_login()
    if r:
        return r

    product = query_one("SELECT * FROM products WHERE id=%s", (product_id,))
    if not product:
        flash("Product not found.")
        return redirect(url_for('shop'))

    # Check stock availability
    stock_qty = int(product.get('stock_qty', 0))
    if stock_qty <= 0:
        flash("This product is out of stock.")
        return redirect(url_for('shop'))

    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1

    if quantity > stock_qty:
        flash(f"Only {stock_qty} items available in stock.")
        return redirect(url_for('shop'))

    payment_method = request.form.get('payment_method', 'Cash on Delivery')

    # ensure price numeric
    try:
        price = float(product.get('price', 0))
    except Exception:
        price = 0.0

    total_price = price * quantity

    # Apply membership discounts
    user = query_one("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    discount = 0.0
    if user and user['membership']:
        if user['membership'] == 'Silver':
            discount = 0.05
        elif user['membership'] == 'Gold':
            discount = 0.10
        elif user['membership'] == 'Platinum':
            discount = 0.15

    discounted_price = total_price * (1 - discount)

    # Decrement stock quantity
    new_stock = stock_qty - quantity
    execute("UPDATE products SET stock_qty=%s WHERE id=%s", (new_stock, product_id))

    execute("""INSERT INTO orders (user_id, product_id, quantity, original_price, discount_applied, total_price, payment_method, payment_status, status, order_date)
               VALUES (%s, %s, %s, %s, %s, %s, %s, 'unpaid', 'pending', NOW())""",
            (session['user_id'], product_id, quantity, total_price, discount, discounted_price, payment_method))

    flash(orders_content['order_placed'])
    return redirect(url_for('orders'))

@app.route('/confirm_bulk_payment', methods=['POST'])
def confirm_bulk_payment():
    r = require_login()
    if r:
        return r

    selected_orders = request.form.getlist('selected_orders')
    payment_method = request.form.get('payment_method')
    reference = request.form.get('reference', '').strip()

    if not selected_orders:
        flash("No orders selected.")
        return redirect(url_for('orders'))

    if payment_method not in ['Cash on Delivery', 'GCash', 'PayMaya']:
        flash("Invalid payment method.")
        return redirect(url_for('orders'))

    if payment_method != 'Cash on Delivery' and not reference:
        flash("Reference/Transaction ID is required for this payment method.")
        return redirect(url_for('orders'))

    updated_count = 0
    for order_id_str in selected_orders:
        try:
            order_id = int(order_id_str)
        except ValueError:
            continue

        # Ensure the order belongs to the user and is pending
        order = query_one("SELECT * FROM orders WHERE id=%s AND user_id=%s AND status='pending'",
                         (order_id, session['user_id']))
        if not order:
            continue

        # Update payment method and status
        execute("UPDATE orders SET payment_method=%s, payment_status='paid' WHERE id=%s",
               (payment_method, order_id))
        updated_count += 1

    if updated_count > 0:
        flash(f"Payment method updated to {payment_method} for {updated_count} order(s).")
    else:
        flash("No orders were updated.")
    return redirect(url_for('orders'))

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

        # Ensure the order belongs to the user and is not delivered
        order = query_one("SELECT * FROM orders WHERE id=%s AND user_id=%s AND status != 'delivered'", (order_id, session['user_id']))
        if not order:
            continue

        # Restore stock quantity
        product = query_one("SELECT * FROM products WHERE id=%s", (order['product_id'],))
        if product:
            new_stock = int(product.get('stock_qty', 0)) + order['quantity']
            execute("UPDATE products SET stock_qty=%s WHERE id=%s", (new_stock, order['product_id']))

        # Delete the order
        execute("DELETE FROM orders WHERE id=%s", (order_id,))
        cancelled_count += 1

    if cancelled_count > 0:
        flash(f"{cancelled_count} order(s) cancelled successfully.")
    else:
        flash("No orders were cancelled.")
    return redirect(url_for('orders'))

@app.route('/admin_orders')
def admin_orders():
    r = require_login()
    if r:
        return r

    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))

    orders = query_all("""SELECT o.*, u.username, u.full_name, u.address, p.name AS product_name, p.price, p.image
                          FROM orders o
                          JOIN users u ON o.user_id = u.id
                          JOIN products p ON o.product_id = p.id
                          ORDER BY o.order_date DESC""")

    return render_template('admin/admin_orders.html', orders=orders, content=admin_dashboard_content)

@app.route('/admin_shop')
def admin_shop():
    r = require_login()
    if r:
        return r

    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))

    # Fetch all products for admin shop view
    products = query_all("SELECT * FROM products ORDER BY created_at DESC")
    return render_template('admin/admin_shop.html', products=products, content=admin_dashboard_content)

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

    # DELETE PRODUCT
    if request.method == 'POST' and request.form.get('_method') == 'DELETE':
        delete_id = request.form.get('delete_id')
        if delete_id:
            execute("DELETE FROM products WHERE id=%s", (delete_id,))
            flash(products_content['product_deleted'])
        return redirect(url_for('admin_products'))

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

@app.route('/admin_dashboard')
def admin_dashboard():
    r = require_login()
    if r:
        return r

    # Admin check
    if session.get('role') != 'admin':
        flash(admin_dashboard_content['access_denied'])
        return redirect(url_for('home'))

    # Calculate stats for display
    total_products_row = query_one("SELECT COUNT(*) as count FROM products")
    total_orders_row = query_one("SELECT COUNT(*) as count FROM orders")
    total_users_row = query_one("SELECT COUNT(*) as count FROM users")

    total_products = total_products_row['count'] if total_products_row else 0
    total_orders = total_orders_row['count'] if total_orders_row else 0
    total_users = total_users_row['count'] if total_users_row else 0

    # Get product stocks
    products_stocks = query_all("SELECT id, name, stock_qty FROM products ORDER BY stock_qty ASC")

    return render_template('admin/dashboard.html', total_products=total_products, total_orders=total_orders, total_users=total_users, products_stocks=products_stocks, content=admin_dashboard_content)

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

    # If status is 'delivered', also mark payment as paid if unpaid
    if status == 'delivered':
        order = query_one("SELECT payment_status FROM orders WHERE id=%s", (order_id,))
        if order and order['payment_status'] == 'unpaid':
            execute("UPDATE orders SET status=%s, payment_status='paid', payment_method='Cash on Delivery' WHERE id=%s", (status, order_id))
        else:
            execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))
        flash('Order status updated to delivered and payment marked as paid.')
    else:
        execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))
        flash('Order status updated successfully.')

    return redirect(url_for('admin_orders'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
