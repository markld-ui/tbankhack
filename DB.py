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
            password TEXT NOT NULL,
            project TEXT NOT NULL,
            hard_skills TEXT,
            soft_skills TEXT,
            description TEXT,
            location TEXT,
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
            hard_skills TEXT,
            soft_skills TEXT,
            description TEXT,
            location TEXT,
            hardskill_score INTEGER,  -- Баллы за hardskill
            softskill_score INTEGER,  -- Баллы за softskill
            location_score INTEGER,   -- Баллы за location
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

    # Добавляем пользователя
    user = User(
        first_name="Роман",
        last_name="Слиньков",
        email="user@gmail.com",
        password=bcrypt.hashpw("Qwerty355".encode('utf-8'), bcrypt.gensalt()),
        project="Python-backend разработка",
        hard_skills="Python, C#, C++, Java",
        soft_skills="Коммуникабельность, Тайм-менеджмент",
        location="Екатеринбург",
        description="Python-backend разработчик, учусь в IT-Academy",
        id_rating=1,
        id_request=1
    )
    user.add_user()

    # Добавляем компанию
    company = Company(
        comp_name='АО "Т-Банк"',
        email="company@gmail.com",
        password=bcrypt.hashpw("Qwerty355".encode('utf-8'), bcrypt.gensalt()),
        hard_skills="Python, C#, C++, Java",
        soft_skills="Коммуникабельность, Обучаемость",
        description="Российский коммерческий банк, сфокусированный полностью на дистанционном обслуживании, не имеющий розничных отделений.",
        location="Москва",
        hardskill_score=3,
        softskill_score=2,
        location_score=1,
        rating=4.5,
        id_request=1
    )
    company.add_comp()

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


def calculate_compatibility(user_id):
    conn = sqlite3.connect('people_db.db')
    cursor = conn.cursor()

    # Получаем данные пользователя
    cursor.execute('SELECT hard_skills, soft_skills, location FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        print(f"Пользователь с id {user_id} не найден.")
        return

    # Разделяем навыки пользователя на множества
    user_hardskills = set(user[0].split(', '))
    user_softskills = set(user[1].split(', '))
    user_location = user[2]

    # Получаем данные всех компаний
    cursor.execute('SELECT id, hard_skills, soft_skills, location, hardskill_score, softskill_score, location_score, comp_name FROM comp')
    companies = cursor.fetchall()

    results = []

    for company in companies:
        comp_id, comp_hardskills, comp_softskills, comp_location, hardskill_score, softskill_score, location_score, comp_name = company
        comp_hardskills = set(comp_hardskills.split(', '))
        comp_softskills = set(comp_softskills.split(', '))

        total_score = 0

        # Сравниваем hard skills
        common_hardskills = user_hardskills.intersection(comp_hardskills)
        total_score += len(common_hardskills) * hardskill_score

        # Сравниваем soft skills
        common_softskills = user_softskills.intersection(comp_softskills)
        total_score += len(common_softskills) * softskill_score

        # Сравниваем location
        if user_location == comp_location:
            total_score += location_score

        # Максимальное количество баллов
        max_score = (len(user_hardskills) * hardskill_score) + (len(user_softskills) * softskill_score) + int(location_score)

        # Процент совместимости
        compatibility_percentage = (total_score / max_score) * 100

        results.append({
            'company_id': comp_id,
            'compatibility': compatibility_percentage,
            'name_company': comp_name
        })

    cursor.close()
    conn.close()

    return results


class User:
    def __init__(self, first_name, last_name, email, password, project, hard_skills, soft_skills, description, location, id_rating, id_request):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.project = project
        self.hard_skills = hard_skills
        self.soft_skills = soft_skills
        self.description = description
        self.location = location
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
                INSERT INTO users (first_name, last_name, email, password, project, hard_skills, soft_skills, description, location, id_rating, id_request)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.first_name, self.last_name, self.email, self.password, self.project, self.hard_skills, self.soft_skills, self.description, self.location, self.id_rating, self.id_request))

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
    def __init__(self, comp_name, email, password, hard_skills, soft_skills, description,  location, hardskill_score, softskill_score, location_score, rating, id_request):
        self.comp_name = comp_name
        self.email = email
        self.password = password
        self.description = description
        self.hard_skills = hard_skills
        self.soft_skills = soft_skills
        self.location = location
        self.hardskill_score = hardskill_score
        self.softskill_score = softskill_score
        self.location_score = location_score
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
                INSERT INTO comp (comp_name, email, password, hard_skills, soft_skills, description, location, hardskill_score, softskill_score, location_score, rating, id_request)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.comp_name, self.email, self.password, self.hard_skills, self.soft_skills, self.description, self.location, self.hardskill_score, self.softskill_score, self.location_score, self.rating, self.id_request))

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