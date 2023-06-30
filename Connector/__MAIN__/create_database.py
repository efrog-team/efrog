from dotenv import dotenv_values
import mysql.connector

config = dotenv_values(".env")

mydb = mysql.connector.connect(
    host=config["HOST"],
    user=config["USERNAME"],
    password=config["PASSWORD"]
)

mydb.cursor().execute(f"DROP DATABASE IF EXISTS {config['DATABASE']}")

mydb.cursor().execute(f"CREATE DATABASE {config['DATABASE']}")