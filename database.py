from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:manasLW19@localhost:5432/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#while True:
#    try:
#        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user='postgres',
#                                password='manasLW19',cursor_factory=RealDictCursor)
#        cur = conn.cursor()
#        print("Connected to the database")
#        break
#    except:
#        print("I am unable to connect to the database")
#        break
