from db import execute

# Create the otps table if it does not exist
execute("""CREATE TABLE IF NOT EXISTS otps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    otp_code VARCHAR(10),
    type VARCHAR(20),
    expires_at DATETIME
)""")

print("Otps table created or already exists.")
