import models,  schemas
from database import SessionLocal, engine, get_db
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/',response_model=schemas.Userout)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=schemas.Userout)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=404, detail='User not found')   
    return user