from fastapi import FastAPI, HTTPException, Header
from database.users_teams_members import create_user as create_user_db, get_user as get_user_db, get_and_check_user_by_token as get_user_by_token_db
from database.users_teams_members import create_team as create_team_db
from database.users_teams_members import create_team_memeber as create_team_memeber_db, get_team_members_by_team_name as get_team_members_db, confirm_team_member as confirm_team_member_db
from models import User, UserRequest, UserToken, TeamRequest, TeamMemberRequest
from security.hash import hash_hex
from security.jwt import encode_token
from typing import Annotated

app: FastAPI = FastAPI()

@app.post("/users")
def post_user(user: UserRequest) -> dict[str, str]:
    create_user_db(user)
    return {}

@app.post("/token")
def post_token(user: UserToken) -> dict[str, str]:
    user_db: User | None = get_user_db(username=user.username)
    if user_db is None:
        raise HTTPException(status_code=401, detail="User does not exist")
    elif user_db.password == hash_hex(user.password):
        return {'token': encode_token(user.username, hash_hex(user.password))}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")

@app.get("/users/me")
def get_user_me(authorization: Annotated[str | None, Header()]) -> dict[str, str]:
    if authorization is not None:
        user_db: User | None = get_user_by_token_db(authorization)
        return {
            'username': user_db.username,
            'email': user_db.email,
            'name': user_db.name
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/users/{username}")
def get_user(username: str) -> dict[str, str]:  
    user_db: User | None = get_user_db(username=username)
    if user_db is None:
        raise HTTPException(status_code=401, detail="User does not exist")
    else:
        return {
            'username': user_db.username,
            'email': user_db.email,
            'name': user_db.name
        }

@app.post("/teams")
def post_team(team: TeamRequest, authorization: Annotated[str | None, Header()]) -> dict[str, str]:
    if authorization is not None:
        create_team_db(team, authorization)
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {}

@app.post("/teams/{team_name}/team-members")
def post_team_member(team_member: TeamMemberRequest, team_name: str, authorization: Annotated[str | None, Header()]) -> dict[str, str]:
    if authorization is not None:
        create_team_memeber_db(team_member, team_name, authorization)
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {}

@app.get("/teams/{team_name}/team-members")
def get_team_members(team_name: str, only_confirmed: bool) -> dict[str, list[dict[str, str]]]:
    res: list[dict[str, str]] = []
    for team_member in get_team_members_db(team_name, only_confirmed):
        res.append({
            'username': team_member.username,
            'email': team_member.email,
            'name': team_member.name,
            'confirmed': str(bool(team_member.confirmed))
        })
    return {
        'team_members': res
    }

@app.put("/teams/{team_name}/team-members/{team_member_username}/confirm")
def put_confirm_team_member(team_name: str, team_member_username: str, authorization: Annotated[str | None, Header()]) -> dict[str, str]:
    if authorization is not None:
        confirm_team_member_db(team_name, team_member_username, authorization)
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {}