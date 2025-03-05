import sqlite3
import bcrypt

# Функция для создания базы данных и таблицы
def create_database():
    conn = sqlite3.connect('people_db.db')
    cursor = conn.cursor()

    # Создаем таблицу rating
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rating (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hard_skill DOUBLE,
            soft_skill DOUBLE
        )
    ''')

    # Создаем таблицу users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password BLOB NOT NULL,
            project TEXT NOT NULL,
            languages TEXT,
            description TEXT,
            id_request INTEGER,
            id_rating INTEGER,
            FOREIGN KEY (id_rating) REFERENCES rating(id)
        )
    ''')

    # Создаем таблицу comp
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comp_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            description TEXT,
            min_rating INTEGER NOT NULL,
            rating DOUBLE,
            id_request INTEGER,
            FOREIGN KEY (id_request) REFERENCES request(id)
        )
    ''')

    # Создаем таблицу request
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS request (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL,
            id_users INTEGER,
            id_comp INTEGER,
            FOREIGN KEY (id_users) REFERENCES users(id),
            FOREIGN KEY (id_comp) REFERENCES comp(id)
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()


def get_user_by_email(email):
    conn = sqlite3.connect('people_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def get_company_by_email(email):
    conn = sqlite3.connect('people_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comp WHERE email = ?', (email,))
    company = cursor.fetchone()
    cursor.close()
    conn.close()
    return company


class User:
    def __init__(self, first_name, last_name, email, password, project, languages, description, id_rating, id_request):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.project = project
        self.languages = languages
        self.description = description
        self.id_rating = id_rating
        self.id_request = id_request

    def hash_password(self, password):
        print(f"Password encode: {password.encode('utf-8')}")
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Return bytes

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def add_user(self):
        conn = sqlite3.connect('people_db.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (first_name, last_name, email, password, project, languages, description, id_rating, id_request)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.first_name, self.last_name, self.email, self.password, self.project, self.languages, self.description, self.id_rating, self.id_request))

            conn.commit()
            print("Пользователь успешно добавлен!")
        except sqlite3.IntegrityError:
            print("Ошибка: Логин уже существует.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            cursor.close()
            conn.close()

class Company:
    def __init__(self, comp_name, email, password, description, min_rating, rating, id_request):
        self.comp_name = comp_name
        self.email = email
        self.password = password
        self.description = description
        self.min_rating = min_rating
        self.rating = rating
        self.id_request = id_request

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Return bytes

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def add_comp(self):
        conn = sqlite3.connect('people_db.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO comp (comp_name, email, password, description, min_rating, rating, id_request)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.comp_name, self.email, self.password, self.description, self.min_rating, self.rating, self.id_request))

            conn.commit()
            print("Компания успешно добавлена!")
        except sqlite3.IntegrityError:
            print("Ошибка: Логин уже существует.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            cursor.close()
            conn.close()

# Создаем базу данных и таблицы при импорте модуля
create_database()