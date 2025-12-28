from sqlmodel import SQLModel, create_engine

SQLITE_URL = "sqlite:///./database.db"
engine = create_engine(SQLITE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)
