from dotenv import dotenv_values
config = dotenv_values(".env")

import os
import mysql.connector

def create_tables():
    with mysql.connector.connect(
        host=config["HOST"],
        user=config["USERNAME"],
        password=config["PASSWORD"],
        database=config["DATABASE"]
    ) as connection:
        with open(os.path.dirname(__file__).replace("\\", "/") + "/create_tables.sql", "r") as sql_file:
            with connection.cursor() as cursor:
                statements = sql_file.read().split(";")
                for statement in statements:
                    cursor.execute(statement)

if __name__ == "__main__":
    create_tables()