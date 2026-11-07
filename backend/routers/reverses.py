from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from database.database import get_reverses_db
from database.models import Reverses
from database.schema import ReverseCreate
from logger import logger

router = APIRouter(
    prefix="/reverses",
    tags=["Reverses"]
)

def serialize_reverse(review: Reverses) -> dict:
    return {
        "id": review.id,
        "reverse": review.reverse,
        "date": review.date,
    }

@router.post("/put")
def add_reverse(validate: ReverseCreate, db: Session = Depends(get_reverses_db)):
    try:
        new_reverse = Reverses(
            reverse=validate.reverser_revers
        )
        db.add(new_reverse)
        db.commit()
        db.refresh(new_reverse)
        return {
            "status": f"200, Review {new_reverse.id} added successfully!",
            "review": serialize_reverse(new_reverse)
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in add_reverse: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get("/")
def get_all_reverses(db: Session = Depends(get_reverses_db)):
    try:
        reviews = db.query(Reverses).all()
        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews added")
        return [serialize_reverse(review) for review in reviews]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_all_reverses: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get("/{reverse_id}")
def get_reverse(reverse_id: int = Path(gt=0), db: Session = Depends(get_reverses_db)):
    try:
        review = db.query(Reverses).filter(Reverses.id == reverse_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return serialize_reverse(review)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_reverse: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.put("/edit/{reverse_id}")
def edit_reverse(
    reverse_id: int = Path(gt=0),
    validate: ReverseCreate = None,
    db: Session = Depends(get_reverses_db),
):
    try:
        review = db.query(Reverses).filter(Reverses.id == reverse_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        review.reverse = validate.reverser_revers
        db.commit()
        db.refresh(review)
        return {
            "status": f"200, Review {reverse_id} updated successfully.",
            "review": serialize_reverse(review)
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in edit_reverse: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.delete("/delete/{reverse_id}")
def delete_reverse(reverse_id: int = Path(gt=0), db: Session = Depends(get_reverses_db)):
    try:
        review = db.query(Reverses).filter(Reverses.id == reverse_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        db.delete(review)
        db.commit()
        return {
            "status": f"200, Review {reverse_id} deleted successfully."
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in delete_reverse: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
