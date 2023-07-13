from dotenv import dotenv_values

config: dict[str, str | None] = dotenv_values('.env')

database_config: dict[str, str | int | None] = {
    'host': config['DB_HOST'],
    'user': config['DB_USERNAME'],
    'password': config['DB_PASSWORD'],
    'database': config['DB_DATABASE'],
    'port': int(config['DB_PORT'] if config['DB_PORT'] != None else '0')
}