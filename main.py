from flask import Flask, render_template, request, redirect, url_for, session, flash
import logging
from DB import User, Company, create_database, get_user_by_email, get_company_by_email
import os
import bcrypt
import sqlite3
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') # Секретный ключ для управления сессиями


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

    email = session['email']
    company = get_company_by_email(email)

    app.logger.debug(f"Employer profile accessed by {session['email']}")

    if not company:
        flash('Компания не найден.')
        return redirect(url_for('first_page'))
    return render_template("profile_employer.html", company=company)


@app.route("/profile_trainee")
def profile_trainee_page():
    if 'email' not in session:
        app.logger.warning("Unauthorized access attempt to trainee profile")
        return redirect(url_for('first_page'))
    app.logger.debug(f"Trainee profile accessed by {session['email']}")
    email = session['email']
    user = get_user_by_email(email)

    app.logger.debug(f"Employer profile accessed by {session['email']}")

    if not user:
        flash('Пользователь не найден.')
        return redirect(url_for('first_page'))

    return render_template("profile_trainee.html", user=user)


@app.route("/calculate_compatibility/<int:user_id>")
def calculate_compatibility(user_id):
    from DB import calculate_compatibility as calc_comp
    results = calc_comp(user_id)
    return render_template("compatibility_results.html", results=results)


@app.route("/update_description", methods=['POST'])
def update_description():
    if 'email' not in session:
        app.logger.warning("Unauthorized access attempt to update description")
        return redirect(url_for('first_page'))

    email = session['email']
    description = request.form.get('description')  # Получаем новое описание из формы
    app.logger.debug(f"Received description: {description}")

    conn = sqlite3.connect('people_db.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE users
            SET description = ?
            WHERE email = ?
        ''', (description, email))

        conn.commit()
        app.logger.info(f"Description updated for user: {email}")
        flash('Описание успешно обновлено!')
    except Exception as e:
        app.logger.error(f"Error updating description: {e}")
        flash('Ошибка при обновлении описания.')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('profile_trainee_page'))


@app.route("/submit_registration", methods=['POST'])
def submit_registration():
    user_type = request.form.get('user_type')
    email = request.form.get('email')
    app.logger.debug(f"Registration attempt for {user_type} with email: {email}")

    # Проверка корректности email
    if not email or "@" not in email:
        flash("Некорректный email. Пожалуйста, введите действительный email.", "error")
        return redirect(url_for('index_page'))

    # Проверка, существует ли уже email
    if user_type == 'employer':
        company = get_company_by_email(email)
        if company:
            flash('Email уже зарегистрирован как работодатель.', "error")
            app.logger.warning(f"Email {email} already registered as employer.")
            return redirect(url_for('index_page'))

        comp_name = request.form.get('comp_name')
        password = request.form.get('password')
        if not comp_name or not password:
            flash("Все поля обязательны для заполнения.", "error")
            return redirect(url_for('index_page'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Хэшируем пароль
        company = Company(comp_name, email, hashed_password, "", "", "", 0, 0.0, None)
        company.add_comp()
        app.logger.info(f"Employer registered: {comp_name} with email: {email}")
        flash("Регистрация прошла успешно!", "success")

    elif user_type == 'trainee':
        user = get_user_by_email(email)
        if user:
            flash('Email уже зарегистрирован как стажёр.', "error")
            app.logger.warning(f"Email {email} already registered as trainee.")
            return redirect(url_for('index_page'))

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        if not first_name or not last_name or not password:
            flash("Все поля обязательны для заполнения.", "error")
            return redirect(url_for('index_page'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Хэшируем пароль
        user = User(first_name, last_name, email, hashed_password, "", "", "", "", None, None)
        user.add_user()
        app.logger.info(f"Trainee registered: {first_name} {last_name} with email: {email}")
        flash("Регистрация прошла успешно!", "success")

    session['email'] = email
    return redirect(url_for('profile_employer_page' if user_type == 'employer' else 'profile_trainee_page'))


@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('login-email')
    password = request.form.get('login-password')
    app.logger.debug(f"Login attempt for email: {email}")

    if not email or not password:
        flash("Пожалуйста, заполните все поля.", "error")
        return redirect(url_for('first_page'))

    user = get_user_by_email(email)
    company = get_company_by_email(email)

    if user and bcrypt.checkpw(password.encode('utf-8'), user[4]):  # user[4] is already in bytes
        session['email'] = email
        session['user_type'] = 'trainee'
        app.logger.info(f"Trainee logged in: {email}")
        flash("Вход выполнен успешно!", "success")
        return redirect(url_for('profile_trainee_page'))  # Перенаправление на страницу профиля стажера
    elif company and bcrypt.checkpw(password.encode('utf-8'), company[3]):  # company[3] is already in bytes
        session['email'] = email
        session['user_type'] = 'employer'
        app.logger.info(f"Employer logged in: {email}")
        flash("Вход выполнен успешно!", "success")
        return redirect(url_for('profile_employer_page'))  # Перенаправление на страницу профиля работодателя
    else:
        flash('Неверный email или пароль', "error")
        app.logger.warning(f"Failed login attempt for email: {email}")
        return redirect(url_for('first_page'))


@app.route("/logout")
def logout():
    app.logger.debug(f"User  logged out: {session.get('email')}")
    session.clear()
    return redirect(url_for('first_page'))


@app.after_request
def add_no_cache_headers(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
    return response


@app.route("/save_skills", methods=['POST'])
def save_skills():
    if 'email' not in session:
        app.logger.warning("Unauthorized access attempt to save skills")
        return redirect(url_for('first_page'))

    email = session['email']
    user_type = session['user_type']
    hard_skills = request.form.get('hard_skills', '')
    soft_skills = request.form.get('soft_skills', '')

    conn = sqlite3.connect('people_db.db')
    cursor = conn.cursor()

    try:
        if user_type == 'trainee':
            cursor.execute('''
                UPDATE users
                SET hard_skills = ?, soft_skills = ?
                WHERE email = ?
            ''', (hard_skills, soft_skills, email))
        elif user_type == 'employer':
            cursor.execute('''
                UPDATE comp
                SET hard_skills = ?, soft_skills = ?
                WHERE email = ?
            ''', (hard_skills, soft_skills, email))

        conn.commit()
        app.logger.info(f"Skills updated for user: {email}")
        flash('Навыки успешно обновлены!', 'success')
    except Exception as e:
        app.logger.error(f"Error updating skills: {e}")
        flash('Ошибка при обновлении навыков.', 'error')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('profile_trainee_page' if user_type == 'trainee' else 'profile_employer_page'))


if __name__ == "__main__":
    app.run(debug=True)