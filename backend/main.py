import uvicorn
from src.config import settings  # Импорт настроек, если используется класс Settings

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.WEB_HOST, port=settings.WEB_PORT, reload=True)
