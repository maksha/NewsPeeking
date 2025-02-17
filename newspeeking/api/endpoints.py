# newspeeking/api/endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging

from newspeeking.api.schemas import CrawlRequest, CrawlResponse, ArticleResponse, MessageResponse
from newspeeking.crawler.crawler import crawl_website
from newspeeking.db.database import get_db, Session, ArticleDB

router = APIRouter()
logger = logging.getLogger(__name__)


# Inherit URL from base CrawlRequest, add crawl_articles
class CrawlRequest(CrawlRequest):
    crawl_articles: Optional[bool] = False


@router.post("/crawl", response_model=CrawlResponse, status_code=200)
async def crawl_endpoint(crawl_request: CrawlRequest, db: Session = Depends(get_db)):
    """
    Endpoint to crawl a news website URL.
    - Default mode (crawl_articles=False or not provided): Extracts and returns a list of article URLs from a listing page.
    - Optional mode (crawl_articles=True): Crawls individual articles and stores (or updates) them in the database.
    """
    url = str(crawl_request.url)
    # Get crawl_articles parameter from request
    crawl_articles_param = crawl_request.crawl_articles
    logger.info(
        f"Crawling requested for URL: {url}, crawl_articles={crawl_articles_param}")

    if crawl_articles_param:  # crawl_articles=True mode: Crawl and store/update articles
        article_data_list = crawl_website(
            url, crawl_articles=True)  # Pass crawl_articles=True
        if isinstance(article_data_list, list):  # Listing page crawl
            articles_crawled_count = 0
            articles_updated_count = 0
            for article_data in article_data_list:
                if article_data:
                    existing_article = db.query(ArticleDB).filter(
                        ArticleDB.url == article_data["url"]).first()
                    if existing_article:  # Article already exists - Update instead of inserting
                        logger.info(
                            f"Article from URL '{article_data['url']}' already exists, updating data.")
                        # Function to update existing article
                        update_article_in_db(
                            db, existing_article, article_data)
                        articles_updated_count += 1
                    else:  # Article does not exist - Insert new article
                        db_article = ArticleDB(**article_data)
                        db.add(db_article)
                        articles_crawled_count += 1
            db.commit()  # Commit all updates and inserts in one transaction
            logger.info(
                f"Crawled and stored {articles_crawled_count} new articles, updated {articles_updated_count} articles from listing page URL: {url}")
            return CrawlResponse(message=f"Crawling from listing page successful, {articles_crawled_count} new articles stored, {articles_updated_count} articles updated.", articles_crawled=articles_crawled_count + articles_updated_count)

        elif isinstance(article_data_list, dict):  # Single article crawl
            article_data = article_data_list  # Rename for clarity
            existing_article = db.query(ArticleDB).filter(
                ArticleDB.url == url).first()
            if existing_article:  # Article already exists - Update
                logger.info(
                    f"Article from URL '{url}' already exists, updating data.")
                # Function to update existing article
                update_article_in_db(db, existing_article, article_data)
                articles_updated_count = 1
                db.commit()
                # Indicate update
                return CrawlResponse(message="Article already exists, data updated.", articles_crawled=1)
            else:  # Article does not exist - Insert new article
                db_article = ArticleDB(**article_data)
                db.add(db_article)
                db.commit()
                logger.info(
                    f"Crawled and stored single article from URL: {url}")
                return CrawlResponse(message="Crawling single article successful, article stored in database.", articles_crawled=1)

        else:  # crawl_website likely returned None (error)
            raise HTTPException(
                status_code=400, detail="Failed to crawl article data.")

    else:  # Default mode (crawl_articles=False): List article URLs
        # Pass crawl_articles=False
        article_urls = crawl_website(url, crawl_articles=False)
        if article_urls:
            # Return article URLs in response
            return JSONResponse(content={"message": "Article URLs extracted from listing page.", "article_urls": article_urls}, status_code=200)
        else:
            raise HTTPException(
                status_code=400, detail="Failed to extract article URLs from listing page.")


def update_article_in_db(db: Session, existing_article: ArticleDB, new_article_data: dict):
    """
    Updates an existing article in the database with new data.
    """
    existing_article.headline = new_article_data["headline"]
    existing_article.article_text = new_article_data["article_text"]
    existing_article.publication_date = new_article_data["publication_date"]
    existing_article.author = new_article_data["author"]
    existing_article.category = new_article_data["category"]


@router.post("/reset_db", response_model=MessageResponse, status_code=200)
async def reset_database(db: Session = Depends(get_db)):
    """
    Endpoint to reset the database by deleting all articles.
    Warning: This action is irreversible and will delete all stored articles.
    """
    try:
        db.query(ArticleDB).delete()  # Delete all records from ArticleDB table
        db.commit()
        return MessageResponse(message="Database reset successful: All articles deleted.")
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        db.rollback()  # Rollback in case of error
        raise HTTPException(
            status_code=500, detail="Failed to reset database.")
