# newspeeking/main.py

from fastapi import FastAPI
from newspeeking.api.endpoints import router as api_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NewsPeeking API",
              description="API to crawl news websites, extract articles, and classify them.",
              version="1.0.0",
              openapi_url="/openapi.json",  # OpenAPI schema
              docs_url="/docs",             # Swagger UI
              redoc_url="/redoc"            # ReDoc
              )

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8088, reload=True)
