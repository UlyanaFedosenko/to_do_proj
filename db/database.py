from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings


DATABASE_URL = settings

engine = create_engine(str(DATABASE_URL.pg_dsn))

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()


Base = declarative_base()