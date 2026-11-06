from fastapi import FastAPI, APIRouter, Depends, Query, HTTPException
from database.database import users_engine, Base, get_users_db
from database.schema import UserCreate
from database.models import Users
from sqlalchemy import Session
from typing import Annotated
from passlib.context import CryptContext
from logger import logger

router = APIRouter(
    prefix=["/users"],
    tags=["users"]
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

@router.post('/put')
def put_user(validate: UserCreate, db: Session = Depends(get_users_db)):

    try:
        new_user = Users(
            id = validate.user_id,
            name = validate.user_name,
            age = validate.user_age,
            detail = validate.user_detail,
            password = pwd_context.hash(validate.user_passwords)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "status": "200",
            "user": "user added successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        looger.error(f"Error in put_user: {str(e)}")
        raise HTTPException(status_code = 500, detail ="Internal Server Error"))


@router.get("/user/id{id}")
def get_user(id: Annotated[int, Query(gt = 0, le=1000000)], db: Session = Depends(get_users_db)):
    
    try:
        user = db.query(Users).filter(Users.id == id).first()

        if not user:
            raise HTTPException(status_code = 404, detail = "user not found")
        else:
            return {
                "user_name": user.name,
                "user_age": user.age,
                "user_detail": user.detail,
                "user_books": user.books
            }
    except HTTPException:
        raise
    except Exception as e:
        looger.error(f"Error in get_user: {str(e)}")
        raise HTTPException(status_code = 500, detail ="Internal Server Error"))


@router.put("/update/{id}/{user_name}/{password}/{new_name}/{new_age}")
def update_user(id: int, user_name: str, password: str, db: Session = Depends(get_users_db)):

    try:
        user = db.query(Users).filter(Users.id == id, Users.name == user_name).first()
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        else:
            isCorrectPassword = pwd_context.verify(password, user.password)
            if isCorrectPassword:
                user.name = new_name
                user.age = new_age
                db.commit()
                db.refresh(user)
                return {
                    "status": f"200, user {user_name} updated to {new_name}"
                }
            else:
                db.rollback()
                raise HTTPException(status_code = 401, detail = "Invalid Data Or Password")
    except HTTPException:
        raise
    except Exception as e:
        looger.error(f"Error in update_user: {str(e)}")
        raise HTTPException(status_code = 500, detail ="Internal Server Error"))


@router.delete("/delete/{user_id}/{user_name}/{user_password}")
def delete_user(user_id: int, user_name: str, user_password: str, db: Session = Depends(get_users_db)):

    try:
        user = db.query(Users).filter(Users.name == user_name, Users.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail = "user not found")
        else:
            isCorrectPassword = pwd_context.verify(user_password, user.password)
            if isCorrectPassword:
                db.delete(user)
                db.commit()
            else:
                db.rollback()
                raise HTTPException(status_code = 401, detail = "Invalid Data Or Password")
    except HTTPException:
        raise
    except Exception as e:
        looger.error(f"Error in delete_user: {str(e)}")
        raise HTTPException(status_code = 500, detail ="Internal Server Error"))
