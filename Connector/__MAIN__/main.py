from fastapi import FastAPI, HTTPException
from database.users_teams_members import create_user as create_user_db, get_user as get_user_db
from database.users_teams_members import create_team as create_team_db
from database.users_teams_members import create_team_memeber as create_team_memeber_db, get_team_members_by_team_name as get_team_members_db, confirm_team_member as confirm_team_member_db
from models import User, UserRequest, TeamRequest, TeamMemberRequest, ConfirmTeamMemberRequest
from security.hash import hash_hex
from security.jwt import encode_token

app: FastAPI = FastAPI()

@app.post("/create-user")
def create_user(user: UserRequest) -> dict[str, str]:
    create_user_db(user)
    return {}
    
@app.get("/get-user")
def get_user(username: str = '') -> dict[str, str]:
    user_db: User | None = get_user_db(username=username)
    if user_db is None:
        raise HTTPException(status_code=401, detail="User does not exist")
    else:
        return {
            'username': user_db.username,
            'email': user_db.email,
            'name': user_db.name
        }

@app.get("/get-token")
def get_token(username: str = '', password: str = '') -> dict[str, str]:
    user_db: User | None = get_user_db(username=username)
    if user_db is None:
        raise HTTPException(status_code=401, detail="User does not exist")
    elif user_db.password == hash_hex(password):
        return {'token': encode_token(username, hash_hex(password))}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")

@app.post("/create-team")
def create_team(team: TeamRequest) -> dict[str, str]:
    create_team_db(team)
    return {}

@app.post("/create-team-member")
def create_team_member(team_member: TeamMemberRequest) -> dict[str, str]:
    create_team_memeber_db(team_member)
    return {}

@app.get("/get-team-members")
def get_team_members(team_name: str, only_confirmed: bool) -> dict[str, list[dict[str, str]]]:
    res: list[dict[str, str]] = []
    for member in get_team_members_db(team_name, only_confirmed):
        res.append({
            'username': member.username,
            'email': member.email,
            'name': member.name,
            'confirmed': str(bool(member.confirmed))
        })
    return {
        'members': res
    }

@app.put("/confirm-team-member")
def confirm_team_member(member: ConfirmTeamMemberRequest) -> dict[str, str]:
    confirm_team_member_db(member)
    return {}