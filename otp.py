import random
from flask import current_app
from smtplib import SMTP
from email.mime.text import MIMEText
from config import Config


def generate_otp():
    return random.randint(100000, 999999)


def send_otp(email, otp):
    try:
        msg = MIMEText(f'Your OTP is: {otp}')
        msg['Subject'] = 'Your OTP Code'
        msg['From'] = Config.MAIL_USERNAME
        msg['To'] = email

        # Set up the server and send the email
        with SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.sendmail(Config.MAIL_USERNAME, email, msg.as_string())

        print(f"OTP sent to {email}.")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        return False
    return True
