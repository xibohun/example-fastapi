








from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm  import Session
from typing import List
from ..database import engine, get_db
from starlette.status import HTTP_201_CREATED
from typing import Optional


router = APIRouter(
    prefix = '/posts',
    tags = ['Posts']
)











@router.get('/')
async def root():
    return {'messeage' : 'welcome to my api'}

@router.get('/', response_model = List[schemas.Post])

def get_posts(db: Session = Depends(get_db), Limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    #cursor.execute(""" select * from post """)
    #posts = cursor.fetchall()
    #print(posts)

    posts = db.query(models.Post).limit(Limit).offset(skip=2).all()


    return posts

@router.post('/', status_code=HTTP_201_CREATED, response_model= schemas.Post)

def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db), user_id: int =Depends(oauth2.get_current_user)):
    
    #cursor.execute(""" INSERT INTO post(title, content) VALUES(%s,%s)RETURNING * """,(post.title, post.content))
    
    #new_post = cursor.fetchone()
    #conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)




    return  new_post

@router.get('/{id}', response_model = schemas.Post)

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







@router.get('/sqlalchemy')

def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return  posts

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)

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


    

@router.put('/{id}', status_code=status.HTTP_404_NOT_FOUND, response_model= schemas.Post)

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

    return query_post.first()
