import sys
import os
sys.path.insert(0, os.path.dirname(__file__).replace('\\', '/') + '/../')

from dotenv import dotenv_values
config: dict[str, str | None] = dotenv_values('.env')

from mysql.connector import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from security.hash import hash_hex
from models import User
from typing import Any

def register_user(user: User) -> None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(
        host=config['HOST'],
        user=config['USERNAME'],
        password=config['PASSWORD'],
        database=config['DATABASE']
    ) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(f"INSERT INTO users (username, email, name, password) VALUES ('{user.username}', '{user.email}', '{user.name}', '{hash_hex(user.password)}')")

def get_user(username: str, email: str = '') -> User | None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(
        host=config['HOST'],
        user=config['USERNAME'],
        password=config['PASSWORD'],
        database=config['DATABASE']
    ) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT username, email, name, password FROM users WHERE username = '{username}' OR email = '{email}'")
            res: Any = cursor.fetchone()
            if res is None:
                return None
            else:
                return User(username=res['username'], email=res['email'], name=res['name'], password=res['password'])
