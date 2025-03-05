import sqlite3


# Функция для создания базы данных и таблицы
def create_database():
    conn = sqlite3.connect('org_db.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comp_name TEXT NOT NULL,
            programming_language TEXT NOT NULL,
            project TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


# Функция для добавления пользователя в базу данных
def add_user(comp_name, programming_language, project, login, password):
    conn = sqlite3.connect('org_db.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (comp_name, programming_language, project, login, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (comp_name, programming_language, project, login, password))
        conn.commit()
        print("Пользователь успешно добавлен!")
    except sqlite3.IntegrityError:
        print("Ошибка: Логин уже существует.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        cursor.close()
        conn.close()


# Основная программа
def main():
    create_database()  # Создаем базу данных и таблицу

    while True:
        print("\nВведите данные пользователя для регистрации:")
        comp_name = input("Имя компании: ")
        programming_language = input("Язык программирования: ")
        project = input("Достижения: ")
        login = input("Логин: ")
        password = input("Пароль: ")

        add_user(comp_name, programming_language, project, login, password)

        another = input("Хотите добавить еще одного пользователя? (да/нет): ").strip().lower()
        if another != 'да':
            break

if __name__ == "__main__":
    main()