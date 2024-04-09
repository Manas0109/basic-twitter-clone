from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
import database,models,schemas, utils, oauth2
from pydantic import EmailStr
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])



@router.post('/login',response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user == None:
        raise HTTPException(status_code=403,detail="Invalid User credentials")
    
    if utils.verify(user_credentials.password,user.password) == None:
        raise HTTPException(status_code=403,detail="Invalid credentials")
    
    
    
    #create token

    access_token = oauth2.create_access_token(data= {"user_id": user.id})

    return {"access_token" : access_token, "token_type":"Bearer"}

