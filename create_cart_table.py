import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_cart_table():
    try:
        # Convert port to int if provided
        db_port = os.getenv("DB_PORT")
        if db_port:
            try:
                db_port = int(db_port)
            except ValueError:
                pass

        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=db_port,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cur = conn.cursor()

        # Create cart table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL DEFAULT 1,
                payment_method VARCHAR(50) NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        print("Cart table created successfully.")
    except mysql.connector.Error as err:
        print("Error creating cart table:", err)
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_cart_table()
