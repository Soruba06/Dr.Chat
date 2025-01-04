from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from pymongo import MongoClient
import random
import string
import re

# Create Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load email configuration from config.py
app.config.from_pyfile('config.py')

# Setup Flask-Mail
mail = Mail(app)

# Setup MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['user_database']
users_collection = db['users']

# Email OTP storage (for simplicity, use a more secure option in production)
otp_storage = {}

# Password validation
def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        contact = request.form['contact']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # Validate password strength
        if not validate_password(password):
            flash('Password must contain at least 8 characters, 1 capital letter, and 1 special character.')
            return redirect(url_for('register'))

        # Check if user already exists
        if users_collection.find_one({'email': email}):
            flash('Email already registered!')
            return redirect(url_for('register'))

        # Hash the password and store the user in MongoDB
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            'email': email,
            'username': username,
            'contact': contact,
            'password': hashed_password
        })

        # Send welcome email
        msg = Message('Welcome to DR.Chat – Your Trusted First Aid Assistant!', sender='your_email@gmail.com', recipients=[email])
        msg.body = (f'Dear {username},\n\nWe are thrilled to welcome you to DR.Chat, your reliable companion for first aid\n assistance! Our AI-driven platform is designed to provide you with instant and\n accurate guidance on health-related concerns, ensuring you have the right support\n when you need it most.\n\n'
                    f'What You Can Expect:\n Instant First Aid Guidance: Get step-by-step instructions for various medical situations.\nSymptom Analysis: Receive insights based on your symptoms for better understanding.\nImage Recognition: Use our advanced technology to identify injuries and get relevant advice.\nNearby Hospitals: Easily find the nearest healthcare facilities when urgent care is needed.\n\n'
                    f'To get started, simply log in to your account and explore the features we offer. Your\nhealth and safety are our top priorities, and we are here to support you every step of\nthe way.\n\nThank you for choosing DR.Chat. Together, we can make a difference in health awareness and safety!\n\nWarm regards,\n\n The DR.Chat Team')
        mail.send(msg)

        flash('Registration successful! A welcome email has been sent to you. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from MongoDB
        user = users_collection.find_one({'email': email})

        # Validate user credentials
        if user and check_password_hash(user['password'], password):
            session['user'] = email
            return redirect('http://127.0.0.1:5001/')  # Redirect to main content API
        else:
            flash('Invalid credentials!')
            return redirect(url_for('login'))

    return render_template('login.html')

# Forgot password route
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # Check if the user exists
        user = users_collection.find_one({'email': email})
        if not user:
            flash('Email not found!')
            return redirect(url_for('forgot_password'))

        # Generate OTP
        otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        otp_storage[email] = otp

        # Send OTP via email
        msg = Message('Password Reset OTP Verification', sender='your_email@gmail.com', recipients=[email])
        msg.body = (f'Dear user,\n\n'
                    f'We received a request to reset your password for your account. To proceed, please use\nthe One-Time Password (OTP) provided below\n\nYour OTP for resetting the password is {otp}.\n\n'
                    f'This OTP is valid for [2 HOURS]. Please enter it in the required field to continue with\nthe password reset process. If you did not request this change, you can safely ignore this email.\n\nor your security, do not share this OTP with anyone.\n\nThank you for your attention.\n\nBest regards')
        mail.send(msg)

        flash('OTP sent to your email!')
        return redirect(url_for('reset_password', email=email))

    return render_template('forgot_password.html')

# Reset password route (with OTP verification)
@app.route('/reset-password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    if request.method == 'POST':
        otp = request.form['otp']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Validate OTP
        if otp != otp_storage.get(email):
            flash('Invalid OTP!')
            return redirect(url_for('reset_password', email=email))

        # Check if passwords match
        if new_password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('reset_password', email=email))

        # Validate password strength
        if not validate_password(new_password):
            flash('Password must contain at least 8 characters, 1 capital letter, and 1 special character.')
            return redirect(url_for('reset_password', email=email))

        # Update the password in MongoDB
        hashed_password = generate_password_hash(new_password)
        users_collection.update_one({'email': email}, {'$set': {'password': hashed_password}})
        del otp_storage[email]  # Remove OTP after use

        # Send reset confirmation email
        msg = Message('Password Reset Confirmation', sender='your_email@gmail.com', recipients=[email])
        msg.body = (f'Hello,\n\nWe are pleased to inform you that your password has been successfully reset. You can now log in to your account using your new password.\n\nIf you did not initiate this change or believe this was done in error, please contact our\nsupport team immediately. Your security is our top priority, and we want to ensure\nyour account remains protected.\n\nFor any assistance, feel free to reach out to us through the following contact\n'
                    f'information:\n\n'
                    f'Email: sorubarajoffical06@gmail.com\nPhone: +94763771635\n\nThank you for being a valued member of our community!\n\nBest Regards,\nYour Service Team')
        mail.send(msg)

        flash('Password reset successful! A confirmation email has been sent. Please log in.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', email=email)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
