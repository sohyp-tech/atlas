from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
import datetime

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15))
    age = Column(Float)
    detail = Column(String(500))
    password = Column(String(80))

    books = relationship("Books", back_populates="added_by")
    reveses = relationship("Reverses", back_populates="reverser")

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String(60))

    title = Column(String(60))
    added_by = relationship("User", back_populates="books")
    added_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_cont = Column(String(30000))
    date = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)

class Reverses(Base):
    __tablename__ = "revirses"

    id = Column(Integer, primary_key=True, index=True)
    reverser = relationship("User", back_populates="reveses")
    reverse = Column(String(750))
    date = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
