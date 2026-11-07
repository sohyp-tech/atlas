from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: int
    user_name: str
    user_age: float
    user_detail: str
    user_password: str

class BookCreate(BaseModel):
    book_author: str
    book_title: str
    book_content: str

class ReverseCreate(BaseModel):
    reverser_name: str
    reverser_revers: str
