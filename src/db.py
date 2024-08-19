from sqlmodel import SQLModel, create_engine, Session


engine = create_engine('sqlite:///database.db')


def get_db():
    try:
        session = Session(engine)
        yield session
    finally:
        session.close()


def create_tables():
    SQLModel.metadata.create_all(engine)
