from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from dotenv import lood_dotenv

load_dotenv()

Base = declarative_base()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

DB_USERS_NAME = os.getenv("DB_USERS_NAME")
DB_BOOKS_NAME = os.getenv("DB_POSTS_NAME")
DB_REVERSES_NAME = os.getenv("DB_COMMENTS_NAME")

USERS_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_USERS_NAME}"
BOOKS_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_BOOKS_NAME}"
REVERSES_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_REVERSES_NAME}"

users_engine = create_engine( USERS_DATABASE_URL )
books_engine = create_engine( BOOKS_DATABASE_URL )
reverses_engine = create_engine( REVERSES_DATABASE_URL )

LocalUsersSession = sessionmaker(autocommit=False, autoflush=False, bind=users_engine)
LocalBooksSession = sessionmaker(autocommit=False, autoflush=False, bind=books_engine)
LocalReversesSession = sessionmaker(autocommit=False, autoflush=False, bind=reverses_engine)


def get_users_db():
    db = LocalUsersSession()
    try:
        yield db
    finally:
        db.close()

def get_books_db():
    db = LocalBooksSession()
    try:
        yield db
    finally:
        db.close()

def get_reverses_db():
    db = LocalReversesSession()
    try:
        yield db
    finally:
        db.close()
