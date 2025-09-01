from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

SQLALCHEMY_URL= os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_URL)

sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()