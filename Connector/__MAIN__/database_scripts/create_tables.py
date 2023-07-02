from dotenv import dotenv_values
config: dict[str, str | None] = dotenv_values('.env')

import os
from mysql.connector import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from typing import TextIO

def create_tables() -> None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(
        host=config['HOST'],
        user=config['USERNAME'],
        password=config['PASSWORD'],
        database=config['DATABASE']
    ) as connection:
        connection.autocommit = True
        sql_file: TextIO
        with open(os.path.dirname(__file__).replace('\\', '/') + '/create_tables.sql', 'r') as sql_file:
            cursor: MySQLCursorAbstract
            with connection.cursor(dictionary=True) as cursor:
                statements: list[str] = sql_file.read().split(';')
                for statement in statements:
                    cursor.execute(statement)

if __name__ == '__main__':
    create_tables()