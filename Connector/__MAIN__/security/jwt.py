from dotenv import dotenv_values
config: dict[str, str | None] = dotenv_values('.env')

import jwt
import datetime
from typing import Any

def encode_token(username: str, password: str) -> str:
    if config['JWT_SECRET'] is None:
        return ''
    else:
        return jwt.encode({'username': username, 'password': password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)}, config['JWT_SECRET'], algorithm='HS256')

def decode_token(token: str) -> dict[str, str | None]:
    if config['JWT_SECRET'] is None:
        return {'username': None, 'password': None}
    else:
        decoded: dict[str, Any] = jwt.decode(token, config['JWT_SECRET'], algorithms=['HS256'])
        return {'username': decoded['username'], 'password': decoded['password']}