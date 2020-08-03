from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine


def session_creator():
    engine = create_engine("sqlite:///database.db")
    DBSession = sessionmaker(bind=engine)
    return DBSession()
