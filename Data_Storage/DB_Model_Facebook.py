from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base for the models
Base = declarative_base()

# Define the Facebook Posts model
class FacebookPost(Base):
    __tablename__ = 'facebook_posts'
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    post_text = Column(Text)
    post_date = Column(String(100))
    media_url = Column(String(255))  # Optional field for media (images/videos)

# Define the Honeypot Accounts model
class HoneypotAccount(Base):
    __tablename__ = 'honeypot_accounts'
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    username = Column(String(100))
    platform = Column(String(50))
    created_at = Column(String(100))

# Setup the SQLite database (you can change this to other DBs like MySQL or PostgreSQL)
DATABASE_URL = 'sqlite:///facebook_honeypot.db'
engine = create_engine(DATABASE_URL)

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
