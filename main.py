from fastapi import FastAPI
import uvicorn

from api.urls import router as task_routes
from core.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(task_routes)


if __name__ == "__main__":
    try:
        uvicorn.run(app, port=settings.port, host=settings.host)
    except Exception as e:
        print("Ошибка в программе", e)
