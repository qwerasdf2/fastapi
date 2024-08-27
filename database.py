from config import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
db_engine = create_engine(url=DATABASE_URL)
session_factory = sessionmaker(bind=db_engine, autoflush=False)

def get_session_factory():
    with session_factory() as db_session:
        return db_session