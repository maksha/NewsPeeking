# 📰 NewsPeeking API 👁️

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Crawler](https://img.shields.io/badge/Crawler-BeautifulSoup4%20%7C%20Requests-orange?style=for-the-badge&logo=octopus&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/)
[![NLP](https://img.shields.io/badge/NLP-NLTK-lightgreen?style=for-the-badge&logo=nltk&logoColor=black)](https://www.nltk.org/)
[![Database](https://img.shields.io/badge/Database-SQLite-lightgray?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)

---

**NewsPeeking API** is a RESTful API built with FastAPI that allows you to crawl news websites, extract article data, and classify news articles using Natural Language Processing (NLP) techniques. It's designed to be modular, configurable, and easy to use for developers who need to programmatically access and analyze news content.

## ✨ Key Features

*   **Web Crawling:** Efficiently crawls news websites using BeautifulSoup4 and `requests`.
*   **Article Extraction:** Extracts key information from news articles:
    *   📰 **Headline**
    *   📝 **Article Text**
    *   📅 **Publication Date**
    *   ✍️ **Author Information**
*   **Intelligent Crawling Modes:**
    *   **List Articles Mode (Default):** Extracts and lists article URLs from news website listing pages (homepages, category pages).
    *   **Crawl Articles Mode (Optional):** Crawls individual articles, extracts content, classifies them, and stores them in a database.
*   **Article Classification:** Categorizes articles using NLP (NLTK) and keyword-based classification (configurable categories).
*   **Structured Storage:** Stores extracted and classified data in a structured SQLite database.
*   **Website-Specific Configuration:** Highly adaptable to different news website structures through YAML configuration files. Define custom CSS selectors for each website.
*   **RESTful API:** Built with FastAPI for a modern, fast, and well-documented API.
*   **Error Handling & Rate Limiting:** Robust error handling for invalid URLs and website issues. Basic rate limiting to be respectful to websites.
*   **Database Reset Endpoint:** Includes an endpoint to easily reset/flush the database for development and testing.

## 🚀 API Endpoints

### 📌 `/crawl` (POST)

*   **Description:** Crawls a news website URL. Operates in two modes:
    *   **Default Mode (List Articles):** Returns a list of article URLs from a listing page.
    *   **Crawl Articles Mode:** Crawls individual articles, extracts data, classifies, and stores in the database.
*   **Request Body:**
    ```json
    {
      "url": "https://www.example-news-website.com/",
      "crawl_articles": true  // Optional: Set to true to crawl and store articles, default is false (list URLs)
    }
    ```
    *   `url` (string, required): The URL of the news website (listing page or article page).
    *   `crawl_articles` (boolean, optional, default: `false`): Set to `true` to enable crawling and storing article content. If `false` or not provided, the API will only list article URLs.
*   **Response (Default Mode - List Articles):**
    ```json
    {
      "message": "Article URLs extracted from listing page.",
      "article_urls": [
        "https://www.example-news-website.com/article1",
        "https://www.example-news-website.com/article2",
        ...
      ]
    }
    ```
*   **Response (Crawl Articles Mode - Success):**
    ```json
    {
      "message": "Crawling from listing page successful, 15 new articles stored, 3 articles updated.",
      "articles_crawled": 18
    }
    ```
*   **Response (Error - 400 Bad Request):**
    ```json
    {
      "detail": "Failed to crawl article data from URL."
    }
    ```

### 🔄 `/reset_db` (POST)

*   **Description:** Resets the database by deleting all stored articles. Useful for development and testing.
*   **Request Body:** None
*   **Response (Success - 200 OK):**
    ```json
    {
      "message": "Database reset successful: All articles deleted."
    }
    ```

## 🛠️ Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/maksha/NewsPeeking.git
    cd NewsPeeking
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate     # On Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration:**
    *   Edit the `config.yaml` file in the project root to configure:
        *   **`default` settings:** `rate_limit_delay`, `categories`, `database_url` (default is `sqlite:///./news_articles.db`).
        *   **`websites` settings:** Website-specific configurations including:
            *   `listing_page`: `article_link_selectors`, `url_pattern_inclusion`.
            *   `article_page`: `headline_selector`, `article_text_selector`, `publication_date_selector`, `author_selector`.
        *   See the example `config.yaml` for detailed structure.

5.  **Run the API:**
    ```bash
    uvicorn newspeeking.main:app --reload
    ```
    The API will be accessible at `http://127.0.0.1:8000`.

## ⚙️ Configuration (`config.yaml`)

The `config.yaml` file allows you to customize the behavior of NewsPeeking, especially for different news websites.

```yaml
default:
  rate_limit_delay: 1
  categories: # ... (Category definitions) ...

websites:
  nytimes.com: # Website-specific settings for nytimes.com
    listing_page:
      article_link_selectors: # CSS selectors to find article links on listing pages
        - "..."
      url_pattern_inclusion: "..." # URL path pattern for article URLs
    article_page:
      headline_selector: "..."    # CSS selector for article headline
      article_text_selector: "..."  # CSS selector for article text paragraphs
      publication_date_selector: "..." # CSS selector for publication date
      author_selector: "..."       # CSS selector for author

  inet.detik.com: # Website-specific settings for inet.detik.com
    # ... (Similar structure as nytimes.com) ...
```
### **Configuration Settings:**

- `default.rate_limit_delay`: Delay (in seconds) between requests to a website (default: 1). Adjust for politeness and to avoid getting blocked.
- `default.categories`: Defines categories and keywords used for article classification. Customize these to suit your needs.
- `websites.[domain].listing_page.article_link_selectors`: A list of CSS selectors used to extract article URLs from listing pages. Crucially, you need to inspect the HTML of target websites and update these selectors.
- `websites.[domain].listing_page.url_pattern_inclusion`: A URL path pattern used to filter extracted URLs to identify likely article URLs.
- `websites.[domain].article_page.[selectors]`: CSS selectors used to extract headline, article text, publication date, and author from individual article pages. You MUST inspect website HTML and update these for each website you want to crawl.

## 🎬 Usage Examples
1. List Article URLs from NYTimes Homepage (Default Mode):

    ```bash
    curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"url": "https://www.nytimes.com/"}' \
    http://127.0.0.1:8000/crawl
    ```

2. Crawl and Store Articles from NYTimes Technology Section Page:

    ```bash
    curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"url": "https://www.nytimes.com/section/technology", "crawl_articles": true}' \
    http://127.0.0.1:8000/crawl
    ```

3. Reset the Database:

    ```bash
    curl -X POST http://127.0.0.1:8000/reset_db
    Use code with caution.
    ```

## 📦 Dependencies

*   [**FastAPI**](https://fastapi.tiangolo.com/) - A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. *(Used for building the REST API endpoints.)*
*   [**Uvicorn**](https://www.uvicorn.org/) - An ASGI web server for Python. *(Used to run the FastAPI application.)*
*   [**Requests**](https://requests.readthedocs.io/en/latest/) -  Python HTTP for Humans. *(Used for making HTTP requests to fetch web page content.)*
*   [**BeautifulSoup4**](https://www.crummy.com/software/BeautifulSoup/) - Python library for pulling data out of HTML and XML files. *(Used for parsing HTML content and extracting data.)*
*   [**NLTK (Natural Language Toolkit)**](https://www.nltk.org/) -  A leading platform for building Python programs to work with human language data. *(Used for Natural Language Processing tasks, specifically article classification.)*
*   [**Validators**](https://pypi.org/project/validators/) - Python validation library. *(Used for validating URL formats.)*
*   [**SQLAlchemy**](https://www.sqlalchemy.org/) - Python SQL toolkit and Object-Relational Mapper. *(Used as an ORM to interact with the SQLite database.)*
*   [**python-dateutil**](https://dateutil.readthedocs.io/en/stable/) - Extensions to the standard Python datetime module. *(Used for robust parsing of dates from web pages.)*
*   [**PyYAML**](https://pyyaml.org/) - YAML parser and emitter for Python. *(Used for loading configuration settings from YAML files.)*

*Thank you to the developers of these amazing open-source dependencies!*

## 🗺️ Roadmap & Future Improvements
- Advanced NLP Classification: Implement more sophisticated NLP techniques (e.g., TF-IDF, word embeddings, machine learning classifiers) for improved article categorization.
- Pagination Handling: Implement pagination crawling to fetch articles from multi-page listing pages.
- More Robust Rate Limiting: Implement more advanced rate limiting strategies to be even more respectful to websites and handle large-scale crawling.
- Asynchronous Crawling: Convert crawling to asynchronous operations for improved performance and speed.
- Data Validation & Cleaning: Add more robust data validation and cleaning steps.
- User Interface: Develop a web UI to interact with the API and visualize crawled data.
- Expand Website Configurations: Add configurations for more news websites.

# 📝 License


Made with ❤️ by maksha