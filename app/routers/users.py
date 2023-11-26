from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hashing password
    email_exists = db.query(models.User).filter(models.User.email == payload.email).first()
    if email_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email already exists")

    hashed_password = utils.encode(payload.password)
    payload.password = hashed_password

    new_user = models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_info = db.query(models.User).filter(models.User.id == id).first()

    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id - {id} not found")

    return user_info
