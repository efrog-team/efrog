from fastapi import FastAPI, HTTPException
from database.users import register_user as register_user_db
from database.users import get_user as get_user_db
from models import User
from security.hash import hash_hex
from security.jwt import generate_token

app: FastAPI = FastAPI()

@app.post("/register-user")
def register_user(user: User) -> dict[str, str]:
    if get_user_db(user.username, user.email) is None:
        register_user_db(user)
    else:
        raise HTTPException(status_code=409, detail="User already exists")
    return {}

@app.get("/get-token")
def get_token(username: str = '', password: str = '') -> dict[str, str]:
    user_db: User | None = get_user_db(username)
    if user_db is None:
        raise HTTPException(status_code=401, detail="User does not exist")
    elif user_db.password == hash_hex(password):
        return {"token": generate_token(username, hash_hex(password))}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")