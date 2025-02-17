# newspeeking/db/database.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func

from newspeeking.config import get_database_url

engine = create_engine(get_database_url())
Base = declarative_base()


class ArticleDB(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    headline = Column(String)
    article_text = Column(String)
    publication_date = Column(DateTime, nullable=True)
    author = Column(String, nullable=True)
    category = Column(String)
    created_at = Column(DateTime, server_default=func.now())


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
