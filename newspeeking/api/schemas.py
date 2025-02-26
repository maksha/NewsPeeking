# Pydantic schemas for API request and response data validation.
from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class CrawlRequest(BaseModel):
    url: HttpUrl


class ArticleResponse(BaseModel):
    url: str
    headline: str
    article_text: str
    publication_date: Optional[str] = None
    author: Optional[str] = None
    category: str


class CrawlResponse(BaseModel):
    message: str
    articles_crawled: int = 0


class MessageResponse(BaseModel):  # New response model for reset_db
    message: str
