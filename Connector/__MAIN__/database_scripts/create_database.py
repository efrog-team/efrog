from dotenv import dotenv_values
config = dotenv_values(".env")

import mysql.connector


def create_database():
    with mysql.connector.connect(
        host=config["HOST"],
        user=config["USERNAME"],
        password=config["PASSWORD"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']}")
            cursor.execute(f"CREATE DATABASE {config['DATABASE']}")

if __name__ == "__main__":
    create_database()