import os
from typing import Generator

from sqlmodel import SQLModel, create_engine, Session


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vanguard_eval.db")

# For SQLite we need check_same_thread=False; for Postgres this is ignored.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
