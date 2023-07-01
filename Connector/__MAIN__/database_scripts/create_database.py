from dotenv import dotenv_values
config: dict[str, str | None] = dotenv_values('.env')

from mysql.connector import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract

def create_database() -> None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(
        host=config['HOST'],
        user=config['USERNAME'],
        password=config['PASSWORD']
    ) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']}")
            cursor.execute(f"CREATE DATABASE {config['DATABASE']}")

if __name__ == '__main__':
    create_database()