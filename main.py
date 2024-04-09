from typing import Optional
from fastapi import Depends, FastAPI, HTTPException


from pydantic import BaseModel

import models
from database import engine
from routers import post, user, auth, vote
from sqlalchemy.orm import Session
from database import get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def read_root():
    return {'data': 'Hello there'}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts