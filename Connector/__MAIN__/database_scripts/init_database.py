import sys
import os
sys.path.insert(0, os.path.dirname(__file__).replace("\\", "/") + "/../")

from dotenv import dotenv_values
config = dotenv_values(".env")

from create_database import create_database
from create_tables import create_tables
from security.hash import hash
import mysql.connector

def init_database():
    create_database()
    create_tables()
    with mysql.connector.connect(
        host=config["HOST"],
        user=config["USERNAME"],
        password=config["PASSWORD"],
        database=config["DATABASE"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO users (username, email, name, password) VALUES ('{config['USERNAME']}', '{config['EMAIL']}', '{config['USERNAME']}', '{hash(config['PASSWORD'])}')")
            connection.commit()

if __name__ == "__main__":
    if input("Password: ") == config["PASSWORD"]:
        init_database()