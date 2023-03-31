import sqlite3
from sqlite3 import Error
import os
from datetime import datetime

# создаем соединение с бд через путь (будем задавать относительный)
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")



create_roles_table = """
CREATE TABLE IF NOT EXISTS roles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rolename TEXT NOT NULL
);
"""

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  login TEXT NOT NULL,
  password TEXT NOT NULL,
  role_id INTEGER NOT NULL,
  FOREIGN KEY (role_id) REFERENCES roles (id)
);
"""

create_items_table = """
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_comment TEXT,
  image BLOB,
  prediction TEXT,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

create_roles = """
INSERT INTO
  roles (rolename)
VALUES
  ('user'),
  ('admin');
"""

#execute_query(connection, create_roles_table)
#execute_query(connection, create_users_table)
#execute_query(connection, create_items_table)
#execute_query(connection, create_roles)

# select_roles = "SELECT * from roles"
# roles = execute_read_query(connection, select_roles)
#
# for role in roles:
#     print(role)

# 2 Запрос на создание пользователя (работает, проверено)
def execute_query_create_user(connection, login, password):
    query = """
    INSERT INTO
      users (login, password, role_id)
    VALUES
      (?, ?, 1);
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, (login, password))
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


#execute_query_create_user(connection, "igor", "123456")

# select_users = "SELECT * from users"
# users = execute_read_query(connection, select_users)
#
# for user in users:
#     print(user)

# 1 Запрос на проверку существования имени пользователя (Проверено, работает)
def execute_query_check_user_exists(connection, login):
    query = """
    SELECT COUNT(*) FROM users WHERE login=?
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, (login,))
        result = cursor.fetchone()[0]
        return True if result > 0 else False
    except Error as e:
        print(f"The error '{e}' occurred")

#print(execute_query_check_user_exists(connection, "igor"))

# 3 Запрос на id юзера (используется в следующем запросе)
def execute_query_get_user_id(connection, login):
    query = """
    SELECT id FROM users WHERE login=?
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, (login,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"The error '{e}' occurred")

# 4 Запрос на создание item (отправляется, когда пользователь отправляет картинку на распознавание) - проверено, работает
def execute_query_create_item(connection, user_comment, image, prediction, login):
    user_id =  execute_query_get_user_id(connection, login)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """
    INSERT INTO
      items (user_comment, image, prediction, user_id, creation_date)
    VALUES
      (?, ?, ?, ?, ?);
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, (user_comment, image, prediction, user_id, current_time))
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# user_comment = 'My comment'
# image_data = b'\x00\x01\x02\x03'
# login = 'igor'
#
# execute_query_create_item(connection, user_comment, image_data, login)

# 5 Запрос на вытягивание item-ов по пользователю (Проверено, работает)
def execute_query_get_items_by_user_id(connection, login):
    user_id = execute_query_get_user_id(connection, login)
    query = """
    SELECT * FROM items WHERE user_id = ?
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

#print(execute_query_get_items_by_user_id(connection, "igor"))

def execute_query_get_users_role_id(connection, login, password):
    query = """
    SELECT role_id FROM users WHERE login=? AND password = ?
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, (login, password))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"The error '{e}' ocurred")


# current_dir = os.getcwd()
# path = os.path.join(current_dir, 'database\\sm_app.sqlite')
# connection = create_connection(path)
#
#
# def execute_query_create_user2(connection, login, password):
#     query = """
#     INSERT INTO
#       users (login, password, role_id)
#     VALUES
#       (?, ?, 2);
#     """
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query, (login, password))
#         connection.commit()
#         print("Query executed successfully")
#     except Error as e:
#         print(f"The error '{e}' occurred")
#
#
# execute_query_create_user2(connection, "stanislav", "123")





