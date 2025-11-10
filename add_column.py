import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    autocommit=False
)
cur = conn.cursor()
cur.execute("ALTER TABLE users ADD COLUMN membership_payment_status ENUM('paid','unpaid') DEFAULT 'unpaid' AFTER membership")
conn.commit()
cur.close()
conn.close()
print('Column added successfully')
