from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from webapp.config import DB_URL

engine = create_engine(DB_URL, echo=True)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

Base.query = db_session.query_property()

# TODO The scoped_session.query_property() accessor is specific to the legacy Query object and is not considered to be part of 2.0-style ORM use.
