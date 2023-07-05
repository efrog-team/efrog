from pydantic import BaseModel

class User(BaseModel):
    id: int | None
    username: str # at least 4 characters and no spaces
    email: str
    name: str
    password: str # hashed

class UserRequest(BaseModel):
    username: str
    email: str
    name: str
    password: str # unhashed

class UserToken(BaseModel):
    username: str
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
    name: str # at least 4 characters and no spaces
    owner_user_id: int
    individual: int

class TeamRequest(BaseModel):
    name: str

class TeamMember(BaseModel):
    id: int | None
    member_user_id: int
    team_id: int
    confirmed: int

class TeamMemberRequest(BaseModel):
    member_username: str