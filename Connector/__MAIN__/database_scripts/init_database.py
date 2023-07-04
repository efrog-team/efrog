import sys
import os
sys.path.insert(0, os.path.dirname(__file__).replace('\\', '/') + '/../')

from dotenv import dotenv_values
config: dict[str, str | None] = dotenv_values('.env')

from create_database import create_database
from create_tables import create_tables
from add_languages import add_languages
from security.hash import hash_hex
from database.users_teams_members import add_user
from models import User

def init_database() -> None:
    create_database()
    create_tables()
    add_languages()
    if not (config['USERNAME'] is None or config['EMAIL'] is None or config['PASSWORD'] is None):
        add_user(User(id=None, username=config['USERNAME'], email=config['EMAIL'], name=config['USERNAME'], password=hash_hex(config['PASSWORD'])))

if __name__ == '__main__':
    if input("Password: ") == config['PASSWORD']:
        init_database()