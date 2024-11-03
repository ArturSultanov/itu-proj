import uvicorn
from src.config import settings

if __name__ == "__main__":
    uvicorn.run("src.app:app", host=settings.WEB_HOST, port=settings.WEB_PORT, reload=True)
