from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = 'sqlite:///./sql_app.db'

engine = create_engine(SQL_DATABASE_URL, connect_args={'check_same_thread': False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session() -> Session:
    session = Session()
    try:
        yield session

    finally:
        session.close()
