from datetime import datetime,timedelta
from fastapi import Depends, HTTPException
from jose import jwt,JWTError
import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#secret key
#expiration time
#algorithm


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta( minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : expire})

    enocoded_data = jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHM)

    return enocoded_data

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token=token,key=SECRET_KEY,algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if id == None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = str(id))
    except JWTError:
        raise credentials_exception
    
    return token_data
        
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = 401 , detail="Could not validate credentials",headers = {"WWW-Authenticate": " Bearer"})

    token = verify_access_token(token,credentials_exception)

    user =  db.query(models.User).filter(models.User.id == token.id).first()

    return user