import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

engine = create_engine(
    f"postgresql://{os.environ.get('POSTGRES_USER')}:"
    f"{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_SERVER')}"
)


async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


SessionDep = Annotated[Session, Depends(get_session)]
