from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from database.connection import get_session
from models.users import User, UserSignIn, NewUser
from sqlmodel import Session

user_router = APIRouter(tags=["User"])


@user_router.post("/signup")
async def sign_user_up(user: NewUser, session: Session = Depends(get_session)) -> dict:
    # Проверяем, есть ли уже пользователь с таким email в базе данных
    statement = select(User).where(User.email == user.email)
    user_exist = session.exec(statement).first()

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already."
        )

    # Создаем нового пользователя и сохраняем в БД
    new_user = User(email=user.email, password=user.password, events=[])
    session.add(new_user)
    session.commit()

    return {"message": "User created successfully"}


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn, session: Session = Depends(get_session)) -> dict:
    # Ищем пользователя по email
    statement = select(User).where(User.email == user.email)
    user_exist = session.exec(statement).first()

    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )

    # Проверяем пароль
    if user_exist.password == user.password:
        return {"message": "User signed in successfully."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials passed."
    )