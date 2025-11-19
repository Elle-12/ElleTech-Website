import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import random
from db import execute, query_one

def generate_otp(length=8):
    """Generate a numeric OTP of specified length"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp_email(recipient_email, otp_code, subject="ElleTech - OTP Verification"):
    """
    Send OTP email to recipient
    Returns True if successful, False otherwise
    """
    try:
        # Email configuration - using your actual environment variable names
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        sender_email = os.getenv('SMTP_USERNAME')
        sender_password = os.getenv('SMTP_PASSWORD')
        
        print(f"Attempting to send email via {smtp_server}:{smtp_port}")
        print(f"From: {sender_email}")
        print(f"To: {recipient_email}")
        
        if not all([smtp_server, sender_email, sender_password]):
            print("Email configuration missing")
            print(f"SMTP_SERVER: {smtp_server}")
            print(f"SMTP_USERNAME: {sender_email}")
            print(f"SMTP_PASSWORD: {'*' * len(sender_password) if sender_password else 'MISSING'}")
            return False

        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Email body
        body = f"""
        <html>
        <body>
            <h2>ElleTech OTP Verification</h2>
            <p>Your OTP code is: <strong>{otp_code}</strong></p>
            <p>This code will expire in 5 minutes.</p>
            <p>If you didn't request this OTP, please ignore this email.</p>
            <br>
            <p>Best regards,<br>ElleTech Team</p>
        </body>
        </html>
        """

        message.attach(MIMEText(body, 'html'))

        # Send email
        print("Connecting to SMTP server...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            print("Starting TLS...")
            server.starttls()
            print("Logging in...")
            server.login(sender_email, sender_password)
            print("Sending email...")
            server.send_message(message)
        
        print(f"OTP email sent successfully to {recipient_email}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
        print("Please check your SMTP username and password (App Password for Gmail)")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
        return False
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False

def store_otp(user_id, otp_code, otp_type='general', meta_info=''):
    """Store OTP in database with expiration"""
    try:
        expires_at = datetime.now() + timedelta(minutes=5)
        
        # Delete any existing OTPs for this user and type
        execute("DELETE FROM otp WHERE user_id=%s AND otp_type=%s", 
                (user_id, otp_type))
        
        # Store new OTP
        execute("""
            INSERT INTO otp (user_id, otp_code, otp_type, meta_info, expires_at, created_at) 
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (user_id, otp_code, otp_type, meta_info, expires_at))
        
        print(f"OTP stored for user {user_id}, type: {otp_type}")
        return True
    except Exception as e:
        print(f"Error storing OTP: {e}")
        return False

def verify_otp(user_id, otp_code, otp_type='general'):
    """Verify OTP from database"""
    try:
        otp_record = query_one("""
            SELECT * FROM otp 
            WHERE user_id=%s AND otp_code=%s AND otp_type=%s AND expires_at > NOW()
        """, (user_id, otp_code, otp_type))
        
        if otp_record:
            # Delete the used OTP
            execute("DELETE FROM otp WHERE id=%s", (otp_record['id'],))
            print(f"OTP verified successfully for user {user_id}")
            return True
        
        print(f"OTP verification failed for user {user_id}")
        return False
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return False

def send_and_store_otp(user_id, email, otp_type='general', meta_info=''):
    """Generate, send and store OTP - returns OTP code if successful"""
    try:
        otp_code = generate_otp(8)
        print(f"Generated OTP: {otp_code} for {email}")
        
        if send_otp_email(email, otp_code):
            if store_otp(user_id, otp_code, otp_type, meta_info):
                return otp_code
            else:
                print("Failed to store OTP")
                return None
        else:
            print("Failed to send OTP email")
            return None
    except Exception as e:
        print(f"Error in send_and_store_otp: {e}")
        return None