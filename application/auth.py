from flask import  Blueprint, render_template, request, flash, redirect, url_for
from helpers import apology
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again!", category='error')
        else:
            flash('Email does not exist!', category="error")
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'));

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists!", category="error")
            return redirect(url_for('auth.register'))  # Redirect back to registration page

        # Validate form inputs
        if not full_name or not email or not password or not confirm_password:
            flash("All fields are required", category="error")
            return redirect(url_for('auth.register'))  # Redirect back to registration page
        elif password != confirm_password:
            flash("Passwords do not match", category="error")
            return redirect(url_for('auth.register'))  # Redirect back to registration page

        new_user = User(email=email, full_name=full_name, password=generate_password_hash(password, method='scrypt'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)  # Logging in the newly registered user
        flash('Account created! You are now logged in.', category='success')

        return redirect(url_for('views.home'))  # Redirect to home page after successful registration and login
    else:
        return render_template("register.html", user=current_user)

