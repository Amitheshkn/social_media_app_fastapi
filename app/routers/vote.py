from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(payload_vote: schemas.Vote, db: Session = Depends(get_db),
         current_user_id: int = Depends(oauth2.get_current_user)):

    post_exists = db.query(models.Post).filter(models.Post.id == payload_vote.post_id).first()
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id - {payload_vote.post_id} does not exist")

    found_vote_query = db.query(models.Vote).filter(models.Vote.post_id == payload_vote.post_id,
                                                    models.Vote.user_id == current_user_id)
    found_vote = found_vote_query.first()

    if payload_vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user_id} has already voted on post {payload_vote.post_id}")

        new_vote = models.Vote(post_id=payload_vote.post_id, user_id=current_user_id)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
        found_vote_query.delete()
        db.commit()

        return {"message": "Successfully removed vote"}
