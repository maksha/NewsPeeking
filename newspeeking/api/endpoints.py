# newspeeking/api/endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
import logging

from newspeeking.api.schemas import CrawlRequest, CrawlResponse, ArticleResponse
from newspeeking.crawler.crawler import crawl_website
from newspeeking.db.database import get_db, Session, ArticleDB

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/crawl", response_model=CrawlResponse, status_code=200)
async def crawl_endpoint(crawl_request: CrawlRequest, db: Session = Depends(get_db)):
    url = str(crawl_request.url)
    logger.info(f"Crawling requested for URL: {url}")

    existing_article = db.query(ArticleDB).filter(ArticleDB.url == url).first()
    if existing_article:
        return CrawlResponse(message=f"Article from URL '{url}' already exists in the database.")

    article_data = crawl_website(url)
    if article_data:
        db_article = ArticleDB(**article_data)
        db.add(db_article)
        db.commit()
        logger.info(
            f"Article from URL '{url}' successfully crawled and stored.")
        return CrawlResponse(message="Crawling successful, article stored in database.", articles_crawled=1)
    else:
        raise HTTPException(
            status_code=400, detail="Failed to crawl and extract article data.")


@router.get("/articles/", response_model=List[ArticleResponse], status_code=200)
async def read_articles(skip: int = 0, limit: int = 10, category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(ArticleDB)
    if category:
        query = query.filter(ArticleDB.category == category)
    articles_db = query.offset(skip).limit(limit).all()
    articles_response = [
        ArticleResponse(
            url=article.url,
            headline=article.headline,
            article_text=article.article_text,
            publication_date=article.publication_date.isoformat(
            ) if article.publication_date else None,
            author=article.author,
            category=article.category
        )
        for article in articles_db
    ]
    return articles_response
