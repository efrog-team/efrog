import sys
import os
sys.path.insert(0, os.path.dirname(__file__).replace('\\', '/') + '/../')

from dotenv import dotenv_values
config: dict[str, str | None] = dotenv_values('.env')

from create_database import create_database
from create_tables import create_tables
from security.hash import hash_hex
from mysql.connector import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract

def init_database() -> None:
    create_database()
    create_tables()
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
            cursor.execute(f"INSERT INTO users (username, email, name, password) VALUES ('{config['USERNAME']}', '{config['EMAIL']}', '{config['USERNAME']}', '{hash_hex(config['PASSWORD'])}')")

if __name__ == '__main__':
    if input("Password: ") == config['PASSWORD']:
        init_database()