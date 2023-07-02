from dotenv import dotenv_values
config: dict[str, str | None] = dotenv_values('.env')

import jwt
import datetime

def generate_token(username: str, password: str) -> str:
    if config['JWT_SECRET'] is None:
        return ''
    else:
        return jwt.encode({'username': username, 'password': password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)}, config['JWT_SECRET'], algorithm='HS256')