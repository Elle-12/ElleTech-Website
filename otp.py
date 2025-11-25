import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import random
import json


# JSON file for storing OTPs
OTP_JSON_FILE = 'otp_storage.json'

def load_otp_data():
    """Load OTP data from JSON file"""
    try:
        if os.path.exists(OTP_JSON_FILE):
            with open(OTP_JSON_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading OTP data: {e}")
        return {}

def save_otp_data(data):
    """Save OTP data to JSON file"""
    try:
        with open(OTP_JSON_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving OTP data: {e}")
        return False

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
    """Store OTP in JSON file with expiration"""
    try:
        expires_at = (datetime.now() + timedelta(minutes=5)).isoformat()
        
        # Load existing data
        otp_data = load_otp_data()
        
        # Remove any existing OTPs for this user and type
        user_key = str(user_id)
        if user_key in otp_data:
            otp_data[user_key] = [otp for otp in otp_data[user_key] if otp.get('otp_type') != otp_type]
        else:
            otp_data[user_key] = []
        
        # Store new OTP
        otp_record = {
            'otp_code': otp_code,
            'otp_type': otp_type,
            'meta_info': meta_info,
            'expires_at': expires_at,
            'created_at': datetime.now().isoformat()
        }
        
        otp_data[user_key].append(otp_record)
        
        # Save back to JSON file
        if save_otp_data(otp_data):
            print(f"OTP stored for user {user_id}, type: {otp_type}")
            return True
        else:
            print("Failed to save OTP data")
            return False
            
    except Exception as e:
        print(f"Error storing OTP: {e}")
        return False

def verify_otp(user_id, otp_code, otp_type='general'):
    """Verify OTP from JSON file"""
    try:
        otp_data = load_otp_data()
        user_key = str(user_id)
        
        if user_key not in otp_data:
            print(f"No OTP found for user {user_id}")
            return False
        
        current_time = datetime.now()
        
        # Find matching OTP
        for otp_record in otp_data[user_key][:]:
            if (otp_record.get('otp_code') == otp_code and 
                otp_record.get('otp_type') == otp_type and
                datetime.fromisoformat(otp_record['expires_at']) > current_time):
                
                # Remove the used OTP
                otp_data[user_key].remove(otp_record)
                save_otp_data(otp_data)
                
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

def cleanup_expired_otps():
    """Clean up expired OTPs from JSON file"""
    try:
        otp_data = load_otp_data()
        current_time = datetime.now()
        cleaned_count = 0
        
        for user_key in list(otp_data.keys()):
            original_count = len(otp_data[user_key])
            otp_data[user_key] = [
                otp for otp in otp_data[user_key] 
                if datetime.fromisoformat(otp['expires_at']) > current_time
            ]
            cleaned_count += (original_count - len(otp_data[user_key]))
            
            # Remove user entry if no OTPs left
            if not otp_data[user_key]:
                del otp_data[user_key]
        
        if cleaned_count > 0:
            save_otp_data(otp_data)
            print(f"Cleaned up {cleaned_count} expired OTPs")
        
        return cleaned_count
    except Exception as e:
        print(f"Error cleaning up expired OTPs: {e}")
        return 0