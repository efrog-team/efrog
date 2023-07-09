import sys
import os
sys.path.insert(0, os.path.dirname(__file__).replace('\\', '/') + '/../')

from mysql.connector import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from config import database_config
from security.hash import hash_hex
from models import User, UserRequest, UserMember, Team, TeamRequest, TeamMember, TeamMemberRequest
from typing import Any
from fastapi import HTTPException
from security.jwt import decode_token

# Users -------------------------------------------------------------------------------------------------------------------------------------------------

BLOCKED_USERNAMES = [
    "me"
]

def create_user(user: User | UserRequest) -> None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            if user.username not in BLOCKED_USERNAMES:
                if get_user(username=user.username, email=user.email) is None:
                    if isinstance(user, User):
                        cursor.execute(f"INSERT INTO users (username, email, name, password) VALUES ('{user.username}', '{user.email}', '{user.name}', '{user.password}')")
                    else:
                        cursor.execute(f"INSERT INTO users (username, email, name, password) VALUES ('{user.username}', '{user.email}', '{user.name}', '{hash_hex(user.password)}')")
                    res_user_id: int | None = cursor.lastrowid
                    if res_user_id is not None:
                        create_team(Team(id=None, name=user.name, owner_user_id=res_user_id, individual=1))
                    else:
                        raise HTTPException(status_code=500, detail="Internal error")
                else:
                    raise HTTPException(status_code=409, detail="User already exists")
            else:
                raise HTTPException(status_code=409, detail="Username is blocked")

def get_user(id: int = -1, username: str = '', email: str = '') -> User | None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT id, username, email, name, password FROM users WHERE id = {id} OR username = '{username}' OR email = '{email}'")
            res: Any = cursor.fetchone()
            if res is None:
                return None
            else:
                return User(id=res['id'], username=res['username'], email=res['email'], name=res['name'], password=res['password'])

def get_and_check_user_by_token(token: str) -> User:
    try:
        decoded_toke: dict[str, str | None] = decode_token(token)
        username: str | None = decoded_toke['username']
        password: str | None = decoded_toke['password']
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    if username is not None:
        user: User | None = get_user(username=username)
        if user is not None:
            if user.password == password:
                return user
            else:
                raise HTTPException(status_code=401, detail="Invalid password in the token") 
        else:
            raise HTTPException(status_code=401, detail="User does not exist")
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

# Teams -------------------------------------------------------------------------------------------------------------------------------------------------

def create_team(team: Team | TeamRequest, token: str = '') -> None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
                if isinstance(team, Team):
                    if get_team(name=team.name, individual=team.individual) is None:
                        cursor.execute(f"INSERT INTO teams (name, owner_user_id, individual) VALUES ('{team.name}', {team.owner_user_id}, {team.individual})")
                        res_team_id: int | None = cursor.lastrowid
                        if res_team_id is not None:
                            create_team_memeber(TeamMember(id=None, member_user_id=team.owner_user_id, team_id=res_team_id, confirmed=1))
                        else:
                            raise HTTPException(status_code=500, detail="Internal error")
                    else:
                        raise HTTPException(status_code=409, detail="Team already exists")
                else:
                    owner_user_id: int | None = get_and_check_user_by_token(token).id
                    if owner_user_id is not None:
                        if get_team(name=team.name, individual=0) is None:
                            cursor.execute(f"INSERT INTO teams (name, owner_user_id, individual) VALUES ('{team.name}', {owner_user_id}, 0)")
                            res_team_id: int | None = cursor.lastrowid
                            if res_team_id is not None:
                                create_team_memeber(TeamMember(id=None, member_user_id=owner_user_id, team_id=res_team_id, confirmed=1))
                            else:
                                raise HTTPException(status_code=500, detail="Internal error")
                        else:
                            raise HTTPException(status_code=409, detail="Team already exists")
                    else:
                        raise HTTPException(status_code=500, detail="Internal error")
                
def get_team(id: int = -1, name: str = '', individual: int = -1) -> Team | None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT id, name, owner_user_id, individual FROM teams WHERE id = {id} OR (name = '{name}' AND individual = {individual})")
            res: Any = cursor.fetchone()
            if res is None:
                return None
            else:
                return Team(id=res['id'], name=res['name'], owner_user_id=res['owner_user_id'], individual=res['individual'])

# Team Members ------------------------------------------------------------------------------------------------------------------------------------------

def create_team_memeber(team_memeber: TeamMember | TeamMemberRequest, team_name: str = '', token: str = '') -> None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            if isinstance(team_memeber, TeamMember):
                if get_team_member_by_ids(team_member_id=team_memeber.member_user_id, team_id=team_memeber.team_id) is None:
                    cursor.execute(f"INSERT INTO team_members (member_user_id, team_id, confirmed) VALUES ({team_memeber.member_user_id}, {team_memeber.team_id}, {team_memeber.confirmed})")
                else:
                    raise HTTPException(status_code=409, detail="Member already exists")
            else:
                owner_user_id: int | None = get_and_check_user_by_token(token).id
                if owner_user_id is not None:
                    team_member: User | None = get_user(username=team_memeber.member_username)
                    if team_member is not None:
                        team_member_id: int | None = team_member.id
                        if team_member_id is not None:
                            team: Team | None = get_team(name=team_name, individual=0)
                            if team is not None:
                                team_id : int | None = team.id
                                if team_id is not None:
                                    if get_team_member_by_ids(team_member_id=team_member_id, team_id=team_id) is None:
                                        cursor.execute(f"INSERT INTO team_members (member_user_id, team_id, confirmed) VALUES ({team_member_id}, {team_id}, {0})")
                                    else:
                                        raise HTTPException(status_code=409, detail="Member already exists")
                                else:
                                    raise HTTPException(status_code=500, detail="Internal error")
                            else:
                                raise HTTPException(status_code=404, detail="Team does not exist")
                        else:
                            raise HTTPException(status_code=500, detail="Internal error")
                    else:
                        raise HTTPException(status_code=404, detail="Member does not exist")
                else:
                    raise HTTPException(status_code=500, detail="Internal error")

def get_team_member_by_ids(id: int = -1, team_member_id: int = -1, team_id: int = -1) -> TeamMember | None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT id, member_user_id, team_id, confirmed FROM team_members WHERE id = {id} OR (member_user_id = {team_member_id} AND team_id = {team_id})")
            res: Any = cursor.fetchone()
            if res is None:
                return None
            else:
                return TeamMember(id=res['id'], member_user_id=res['member_user_id'], team_id=res['team_id'], confirmed=res['confirmed'])

def get_team_member_by_names(team_member_username: str = '', team_name: str = '') -> TeamMember | None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            team_member: User | None = get_user(username=team_member_username)
            if team_member is not None:
                team_member_id: int | None = team_member.id
                if team_member_id is not None:
                    team: Team | None = get_team(name=team_name, individual=0)
                    if team is not None:
                        team_id : int | None = team.id
                        if team_id is not None:
                            cursor.execute(f"SELECT id, member_user_id, team_id, confirmed FROM team_members WHERE (member_user_id = {team_member_id} AND team_id = {team_id})")
                            res: Any = cursor.fetchone()
                            if res is None:
                                return None
                            else:
                                return TeamMember(id=res['id'], member_user_id=res['member_user_id'], team_id=res['team_id'], confirmed=res['confirmed'])
                        else:
                            raise HTTPException(status_code=500, detail="Internal error")
                    else:
                        raise HTTPException(status_code=404, detail="Team does not exist")
                else:
                    raise HTTPException(status_code=500, detail="Internal error")

def get_team_members_by_team_id(team_id: int, only_confirmed: bool) -> list[User]:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT users.id, users.username, users.email, users.name, users.password FROM users JOIN team_members ON users.id = team_members.member_user_id WHERE team_id = {team_id}{' AND confirmed = 1' if only_confirmed else ''}")
            res: Any = cursor.fetchall()
            team_members: list[User] = []
            for team_member in res:
                team_members.append(User(id=team_member['id'], username=team_member['username'], email=team_member['email'], name=team_member['name'], password=team_member['password']))
            return team_members

def get_team_members_by_team_name(team_name: str, only_confirmed: bool) -> list[UserMember]:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            team: Team | None = get_team(name=team_name, individual=0)
            if team is not None:
                team_id : int | None = team.id
                if team_id is not None:
                    cursor.execute(f"SELECT users.id, users.username, users.email, users.name, users.password, team_members.confirmed FROM users JOIN team_members ON users.id = team_members.member_user_id WHERE team_id = {team_id}{' AND confirmed = 1' if only_confirmed else ''}")
                    res: Any = cursor.fetchall()
                    team_members: list[UserMember] = []
                    for team_member in res:
                        team_members.append(UserMember(id=team_member['id'], username=team_member['username'], email=team_member['email'], name=team_member['name'], password=team_member['password'], confirmed=team_member['confirmed']))
                    return team_members
                else:
                    raise HTTPException(status_code=500, detail="Internal error")
            else:
                raise HTTPException(status_code=404, detail="Team does not exist")

def confirm_team_member(team_name: str, team_member_username: str, token: str) -> None:
    connection: MySQLConnectionAbstract
    with MySQLConnection(**database_config) as connection:
        connection.autocommit = True
        cursor: MySQLCursorAbstract
        with connection.cursor(dictionary=True) as cursor:
            team_member_user_id: int | None = get_and_check_user_by_token(token).id
            if team_member_user_id is not None:
                team_member_db: TeamMember | None = get_team_member_by_names(team_member_username=team_member_username, team_name=team_name)
                if team_member_db is not None:
                    if team_member_db.id is not None:
                        cursor.execute(f"UPDATE team_members SET confirmed = 1 WHERE id = {team_member_db.id}")
                    else:
                        raise HTTPException(status_code=500, detail="Internal error")
                else:
                    raise HTTPException(status_code=404, detail="Member does not exist")
            else:
                raise HTTPException(status_code=500, detail="Internal error")
