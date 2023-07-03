from pydantic import BaseModel

class User(BaseModel):
    id: int | None
    username: str
    email: str
    name: str
    password: str # hashed

class UserRequest(BaseModel):
    username: str
    email: str
    name: str
    password: str # unhashed

class UserMember(BaseModel):
    id: int | None
    username: str
    email: str
    name: str
    password: str # hashed
    confirmed: int

class Team(BaseModel):
    id: int | None
    name: str
    owner_user_id: int
    individual: int

class TeamRequest(BaseModel):
    name: str
    owner_jwt: str

class TeamMember(BaseModel):
    id: int | None
    member_user_id: int
    team_id: int
    confirmed: int

class TeamMemberRequest(BaseModel):
    owner_jwt: str
    member_username: str
    team_name: str

class ConfirmTeamMemberRequest(BaseModel):
    member_jwt: str
    member_username: str
    team_name: str