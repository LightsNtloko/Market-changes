#!/usr/bin/env python3

import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)


# Set the secrete key for the app
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initializing the extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Route for sign-up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Add new user to the database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('landing_page'))
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')

    return render_template('login.html')


# Route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/landing-page')
def landing_page():
    return render_template('landing_page-index.html')


# Route for the form page
@app.route('/form-page')
def form_page():
    return render_template('index.html')

@app.route('/submit-data', methods=['POST'])
def submit_data():
    # Retrieve form data
    company_name = request.form.get('company_name')
    company_email = request.form.get('company_email')
    company_socials = request.form.get('company_socials')
    day_to_day_operations = request.form.get('day_to_day_operations')
    product_name = request.form.get('product_name')
    research_type = request.form.get('research_type')


    # Based on research type, get selected techniques
    primary_techniques = []
    secondary_techniques = []

    if research_type == "primary":
        primary_techniques = request.form.getlist('primary_techniques')
    elif research_type == "secondary":
        secondary_techniques = request.form.getlist('secondary_techniques')

    # Logging or further processing of form data
    print(f"Company Name: {company_name}")
    print(f"Company Email: {company_email}")
    print(f"Company Socials: {company_socials}")
    print(f"Day-to-Day Operations: {day_to_day_operations}")
    print(f"Product Name: {product_name}")
    print(f"Research Type: {research_type}")
    if primary_techniques:
        print(f"Primary Research Techniques: {primary_techniques}")
    if secondary_techniques:
        print(f"Secondary Research Techniques: {secondary_techniques}")

    # Saving the submitted data on Database
    with open('submitted_data.txt', 'a') as file:
        file.write(f"Company Name: {company_name}\n")
        file.write(f"Company Email: {company_email}\n")
        file.write(f"Company Socials: {company_socials}\n")
        file.write(f"Day-to-Day Operations: {day_to_day_operations}\n")
        file.write(f"Product Name: {product_name}\n")
        file.write(f"Research Type: {research_type}\n")
    
        if primary_techniques:
            file.write(f"Primary Research Techniques: {primary_techniques}\n")
        if secondary_techniques:
            file.write(f"Secondary Research Techniques: {secondary_techniques}\n")
        file.write("\n")

    # Flash a success message
    flash('Data submited successfully!')

    # Redirect or process the data as required
    return redirect(url_for('index'))

@app.route('/view-data')
def view_data():
    try:
        with open('submitted_data.txt', 'r') as file:
            data = file.read()
    except FileNotFoundError:
        data = 'No data found.'
    return render_template('view_data.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
