from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fastapi_test'







SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()
Base.metadata.create_all(bind=engine)




#while True:
    #try:
        #conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres',
        #cursor_factory = RealDictCursor)

        #cursor = conn.cursor()
        #print('database connection successfully')
        #break

    #except Exception as error:
        #print('connecting database failed')


#app.dependency_overrides[get_db] = override_get_db


client=TestClient(app)
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
       
    yield  TestClient(app)
    


