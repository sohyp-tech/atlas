from fastapi import FastAPI, APIRouter, Depends, Path, HTTPException
from database.database import books_engine, Base, get_books_db
from database.schema import BookCreate
from database.models import Users, Books
from sqlalchemy.orm import Session
from typing import Annotated
from passlib.context import CryptContext
from logger import logger

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

@router.post("/put/{user_id}")
def add_book(user_id: int, validate: BookCreate, db: Session = Depends(get_books_db)):

    try:
        new_book = Books (
            author = validate.book_author,
            title = validate.book_title,
            book_cont = validate.book_content,
            added_by_id = user_id
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return {
            "status": f"200, Book {validate.book_title} added successfully!"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in add_book: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error")


@router.get("/")
def get_all_books(db: Session = Depends(get_books_db)):

    try:
        books = db.query(Books).all()
        if books:
            return [
                {
                    "id": book.id,
                    "author": book.author,
                    "title": book.title,
                    "book_cont": book.book_cont,
                    "added_by_id": book.added_by_id,
                    "date": book.date,
                }
                for book in books
            ]
        else:
            raise HTTPException(status_code = 404, detail = "No books added")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_all_books: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error.")

@router.get("/{adder_id}")
def get_owner_books(adder_id: Annotated[int, Path(gt = 0)], db: Session = Depends(get_books_db)):

    try:
        owner_books = db.query(Books).filter(Books.added_by_id == adder_id).all()
        if owner_books:
            return [
                {
                    "id": book.id,
                    "author": book.author,
                    "adder_id": book.added_by_id,
                    "title": book.title,
                    "book_cont": book.book_cont,
                    "date": book.date
                }
                for book in owner_books
            ]
        else:
            raise HTTPException(status_code = 404, detail = "No books added.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_owner_books: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error.")


@router.put("/edit/{book_title}/{adder_name}{book_id}/new_data/{new_author}/{new_title}/{new_content}/password{password}")
def edit_book(book_title: str, adder_name: str, book_id: Annotated[int, Path(gt = 0)], password: Annotated[str, Path(gt = 0, le = 30)], new_author: str, new_title: str, new_content: str, db: Session = Depends(get_books_db)):

    try:
        book = db.query(Books).filter(Books.added_by_id == book_id, Books.title == book_title).first()
        if not book:
            db.rollback()
            raise HTTPException(status_code = 404, detail = "No books found.")
        else:
            user = db.queru(Users).filter(Users.id == book_id).first()
            isCorrectPassword = pwd_context.verify(password, user.password)
            if not isCorrectPassword:
                db.rollback()
                raise HTTPException(status_code = 401, detail = "Uncorrect Password.")
            else:
                book.author = new_author
                book.title = new_title
                book.book_cont = new_content
                db.commit()
                db.refresh(book)

                return {
                    "status": f"200, Book {book_title} Updated successfully to {new_title}."
                }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in edit_book: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error.")


@router.delete("/delete/{book_title}/password{password}")
def delete_book(book_title: str, password: Annotated[str, Path(gt = 0, le = 30)], db: Session = Depends(get_books_db)):

    try:
        book = db.query(Books).filter(Books.title == book_title).first()
        if not book:
            db.rollback()
            raise HTTPException(status_code = 404, detail = "No books found.")
        else:
            user = db.queru(Users).filter(Users.id == book_id).first()
            isCorrectPassword = pwd_context.verify(password, user.password)
            if not isCorrectPassword:
                db.rollback()
                raise HTTPException(status_code = 401, detail = "Uncorrect Password.")
            else :
                db.delete(book)
                db.commit()

                return {
                    "status": f"200, Book {book_title} Deleted successfully."
                }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_book: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error.")
