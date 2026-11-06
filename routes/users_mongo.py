from fastapi import APIRouter, HTTPException
from database.connection_mongo import DatabaseNoSQL
from models.users_mongo import UserNoSQL, UserSignInNoSQL

user_nosql_router = APIRouter(tags=["Users (MongoDB)"])
user_db = DatabaseNoSQL(UserNoSQL)

@user_nosql_router.post("/signup")
async def signup(user: UserNoSQL):
    existing = await UserNoSQL.find_one(UserNoSQL.email == user.email)
    if existing:
        raise HTTPException(status_code=409, detail="User exists")
    await user_db.save(user)
    return {"message": "User created in MongoDB"}

@user_nosql_router.post("/signin")
async def signin(user: UserSignInNoSQL):
    existing = await UserNoSQL.find_one(UserNoSQL.email == user.email)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    if existing.password == user.password:
        return {"message": "Signed in to MongoDB"}
    raise HTTPException(status_code=401, detail="Invalid credentials")