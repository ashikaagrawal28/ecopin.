from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from .utils.mongo import MongoFunc
from .utils.recaptcha import RecaptchaFunc

auth = Blueprint('auth', __name__)
views = Blueprint('views', __name__)

recaptcha_site_key = os.getenv('RECAPTCHA_SITE_KEY')
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check if email already exists and password hash is correct
        user = MongoFunc.get_data('users', {'email': email})
        if user is not None:
            if check_password_hash(user["password"], password):
                flash('Logged in successfully!', category='success')
                session['name'] = user['name']
                session['email'] = email
                return redirect(url_for('views.sendreport'))
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Email does not exist.', category='error')
        return redirect(url_for('auth.login'))

    if session.get('email', None) is not None:
        return redirect(url_for('views.home'))
    return render_template("login.html", title="Login | EcoPin")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        recaptcha_response = request.form['g-recaptcha-response']

        # check if email already exists
        user = MongoFunc.get_data('users', {'email': email})
        if user is not None:
            flash('Email already exists.', category='error')
        elif len(name) < 1:
            flash('Name must be greater than 1 character.', category='error')
        elif len(email) < 1:
            flash('Email must be greater than 1 character.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password != confirm_password:
            flash('Passwords do not match.', category='error')
        elif not RecaptchaFunc.validate_recaptcha(recaptcha_response):
            flash('reCAPTCHA validation failed. Please try again.', category='error')
        else:
            user_password = generate_password_hash(password, method='scrypt')
            MongoFunc.insert_data('users', {'type': 'user', 'name': name, 'email': email, 'password': user_password, 'points': 0})

            session['name'] = name
            session['email'] = email
            flash('Sign up successful!', category='success')

            return redirect(url_for('views.sendreport'))
        return redirect(url_for('auth.signup'))
    
    if session.get('email', None) is not None:
        return redirect(url_for('views.home'))
    return render_template('signup.html', title="Sign Up | EcoPin", site_key=recaptcha_site_key)

@auth.route('/logout')
def logout():
    session["name"] = None
    session["email"] = None
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))