from flask import Flask, render_template, request, redirect, url_for, session, flash
import logging
from DB import User, Company, create_database, get_user_by_email, get_company_by_email
import os
import bcrypt

app = Flask(__name__)
app.secret_key = f'{os.urandom(12).hex()}'  # Секретный ключ для управления сессиями

# Инициализация базы данных
create_database()

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def first_page():
    app.logger.debug("Accessed the first page")
    return render_template("index.html")

@app.route("/registration")
def index_page():
    app.logger.debug("Accessed the registration page")
    return render_template("registr.html")

@app.route("/profile_employer")
def profile_employer_page():
    if 'email' not in session:
        app.logger.warning("Unauthorized access attempt to employer profile")
        return redirect(url_for('first_page'))
    app.logger.debug(f"Employer profile accessed by {session['email']}")
    return render_template("profile_employer.html")

@app.route("/profile_trainee")
def profile_trainee_page():
    if 'email' not in session:
        app.logger.warning("Unauthorized access attempt to trainee profile")
        return redirect(url_for('first_page'))
    app.logger.debug(f"Trainee profile accessed by {session['email']}")
    return render_template("profile_trainee.html")

@app.route("/submit_registration", methods=['POST'])
def submit_registration():
    user_type = request.form.get('user_type')
    email = request.form.get('email')
    app.logger.debug(f"Registration attempt for {user_type} with email: {email}")

    # Проверка, существует ли уже email
    if user_type == 'employer':
        company = get_company_by_email(email)
        if company:
            flash('Email уже зарегистрирован как работодатель.')
            app.logger.warning(f"Email {email} already registered as employer.")
            return redirect(url_for('index_page'))

        comp_name = request.form.get('comp_name')
        password = request.form.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Хэшируем пароль
        company = Company(comp_name, email, hashed_password, 0, 0.0, None)
        company.add_comp()
        app.logger.info(f"Employer registered: {comp_name} with email: {email}")
    elif user_type == 'trainee':
        user = get_user_by_email(email)
        if user:
            flash('Email уже зарегистрирован как стажёр.')
            app.logger.warning(f"Email {email} already registered as trainee.")
            return redirect(url_for('index_page'))

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Хэшируем пароль
        user = User(first_name, last_name, email, hashed_password, "", None, None)
        user.add_user()
        app.logger.info(f"Trainee registered: {first_name} {last_name} with email: {email}")

    session['email'] = email
    return redirect(url_for('profile_employer_page' if user_type == 'employer' else 'profile_trainee_page'))

@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('login-email')
    password = request.form.get('login-password')
    app.logger.debug(f"Login attempt for email: {email}")
    app.logger.info(password.encode('utf-8'))
    user = get_user_by_email(email)
    app.logger.info(f"Searched user: {user}")
    app.logger.info(type(user[4]).__name__)
    app.logger.info(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
    company = get_company_by_email(email)

    if user and bcrypt.checkpw(password.encode('utf-8'), user[4]):  # user[4] is already in bytes
        session['email'] = email
        app.logger.info(f"Trainee logged in: {email}")
        return redirect(url_for('profile_trainee_page'))
    elif company and bcrypt.checkpw(password.encode('utf-8'), company[3]):  # company[3] is already in bytes
        session['email'] = email
        app.logger.info(f"Employer logged in: {email}")
        return redirect(url_for('profile_employer_page'))
    else:
        flash('Неверный email или пароль')
        app.logger.warning(f"Failed login attempt for email: {email}")
        return redirect(url_for('first_page'))


@app.route("/logout")
def logout():
    app.logger.debug(f"User  logged out: {session.get('email')}")
    session.pop('email', None)
    return redirect(url_for('first_page'))


if __name__ == "__main__":
    app.run(debug=True)
