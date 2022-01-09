
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi import Body
from typing import Optional, List
#from pydantic import BaseModel
from random import randrange
from passlib.context import CryptContext

from starlette.status import HTTP_201_CREATED
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .config import settings
models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware












app = FastAPI()

origins = []
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods ='*',
    allow_headers ='*'

)




    
    
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres',
        cursor_factory = RealDictCursor)

        cursor = conn.cursor()
        print('database connection successfully')
        break

    except Exception as error:
        print('connecting database failed')









my_posts = [{'title' : 'title of post 1','content' : 'content of post 1', 'id' :'1'},
{'title':'favourite foods', 'content' :'l like pizza', 'id':'2'}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




@app.get('/')
async def root():
    return {'messeage' : 'welcome to my api'}

@app.get('/posts', response_model = List[schemas.Post])

def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" select * from post """)
    #posts = cursor.fetchall()
    #print(posts)

    posts = db.query(models.Post).all()


    return posts

@app.post('/post', status_code=HTTP_201_CREATED, response_model= schemas.Post)

def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db)):
    
    #cursor.execute(""" INSERT INTO post(title, content) VALUES(%s,%s)RETURNING * """,(post.title, post.content))
    
    #new_post = cursor.fetchone()
    #conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)




    return  new_post

@app.get('/post/{id}', response_model = schemas.Post)

def get_post(id: int, db: Session= Depends(get_db)):

    #cursor.execute(""" select * from post where ID=%s """ , (str(id),))
    #post = cursor.fetchone()
    #conn.commit()

    post = db.query(models.Post).filter(models.Post.id==id).first()
    print(post)



    
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} not found' )
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message' : f'post with id: {id} not found'}
    return  post







@app.get('/sqlalchemy')

def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return  posts

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id:int, db:Session = Depends(get_db)):
    
    #cursor.execute(""" DELETE FROM post WHERE id = %s returning * """, (str(id),))
    #delete_post = cursor.fetchone()
    #conn.commit()

    post_query= db.query(models.Post).filter(models.Post.id==id)
    #post.delete(synchronize_session=False)
    post = post_query.first()
    
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id :{id} not found")
    
    #return Response(staus_code= status.HTTP_204_NO_CONTENT)

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(staus_code= status.HTTP_204_NO_CONTENT)


    

@app.put('/posts/{id}', status_code=status.HTTP_404_NOT_FOUND, response_model= schemas.Post)

def update_posts(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db)):

    #cursor.execute(""" UPDATE post SET title=%s, content=%s  WHERE id= %s RETURNING * """, 
    #(post.title, post.content,str(id),))
    #update_post = cursor.fetchone()
    #conn.commit()

    #index = find_index_post(id)

    query_post = db.query(models.Post).filter(models.Post.id==id)
    post = query_post.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f'post with id:{id} not found')

    query_post.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    
    return  query_post.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)

def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model = schemas.UserOut)

def get_user(id:int, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f'Users with id:{id} not found')

    return user



















