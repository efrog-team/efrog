from dotenv import dotenv_values
config: dict[str, str | None] = dotenv_values('.env')

from mysql.connector import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract

languages: list[tuple[str, str]] = [
    ('Python 3', '3.10'),
    ('C++ 17', 'g++ 11.2')
]

def create_languages() -> None:
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
            for language in languages:
                cursor.execute(f"INSERT INTO languages (name, version, supported) VALUES ('{language[0]}', '{language[1]}', 1)")

if __name__ == '__main__':
    create_languages()