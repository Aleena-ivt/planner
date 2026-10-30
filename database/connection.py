from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

# Файл базы данных будет создан в корне проекта
database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False}

# echo=True выводит SQL-команды в консоль (удобно для отчета)
engine_url = create_engine(database_connection_string, echo=True, connect_args=connect_args)

def conn():
    # Создает базу данных и таблицы
    SQLModel.metadata.create_all(engine_url)

def get_session():
    with Session(engine_url) as session:
        yield session