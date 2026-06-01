from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./filmlens.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Rating(Base):
    __tablename__ = "ratings"
    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(Integer, index=True, nullable=False)
    movie_id  = Column(Integer, index=True, nullable=False)
    rating    = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedback"
    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, index=True, nullable=False)
    movie_id            = Column(Integer, index=True, nullable=False)
    recommendation_type = Column(String, nullable=False)
    signal              = Column(String, nullable=False)
    timestamp           = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")
