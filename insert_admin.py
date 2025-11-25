from db import query_one, execute
from werkzeug.security import generate_password_hash

# Check if admin exists
admin_exists = query_one("SELECT id FROM users WHERE role='admin' LIMIT 1")
if not admin_exists:
    password_hash = generate_password_hash('admin123')  # Default password
    execute("INSERT INTO users (full_name, email, username, password_hash, role) VALUES (%s, %s, %s, %s, %s)",
            ('Admin User', 'admin@elletech.com', 'admin', password_hash, 'admin'))
    print("Admin user created. Username: admin, Password: admin123")
else:
    print("Admin user already exists.")

