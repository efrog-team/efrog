from dotenv import dotenv_values

config: dict[str, str | None] = dotenv_values('.env')

database_config: dict[str, str | None] = {
    'host': config['HOST'],
    'user': config['USERNAME'],
    'password': config['PASSWORD'],
    'database': config['DATABASE']
}