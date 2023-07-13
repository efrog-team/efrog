import os
from dotenv import dotenv_values

config: dict[str, str | None] = dotenv_values('.env')

database_config: dict[str, str | int | None] = {
    'host': os.environ['DB_HOST'] if os.environ['DB_HOST'] is not None else config['DB_HOST'],
    'user': config['DB_USERNAME'],
    'password': config['DB_PASSWORD'],
    'database': config['DB_DATABASE'],
    'port': int(os.environ['DB_PORT']) if os.environ['DB_PORT'] is not None else int(config['DB_PORT']) if config['DB_PORT'] is not None else None
}