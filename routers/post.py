import models
import schemas
from database import SessionLocal, engine, get_db
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List,Optional
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/',response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit: int=10,skip:int=0,search:Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post('/',response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id =user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# def find_post(id):
#     for post in my_posts:
#         if post['id'] == id:
#             return post
#     return None


# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
        
# @router.get('/posts/{id}')
# def get_post(id: int):
#     post =  my_posts[id]

#     if not post:
#         raise HTTPException(status_code=404, detail='Post not found')
#     return {'post_detail': post}

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=404, detail='Post not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not authenticated')

    
    post_query.delete(synchronize_session=False)
    db.commit()
    return {'message': 'Post deleted successfully'}
