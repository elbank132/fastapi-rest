import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

raw_password = os.getenv("DB_PASSWORD")
db_password = urllib.parse.quote_plus(raw_password) #encoding

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

#Create the Engine (The Connection Pool Manager)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Create the Session Factory (The Unit of Work)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create the Base Model
Base = declarative_base()