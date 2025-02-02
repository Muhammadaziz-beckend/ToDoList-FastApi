from fastapi import FastAPI
import uvicorn

from core.settings import settings

app = FastAPI()


@app.get("/")
async def hello_world():

    return "Hello World"


if __name__ == "__main__":

    try:
        uvicorn.run(app, port=settings.port, host=settings.host)
    except Exception as e:
        print("Ошибка в программе", e)

# run uvicorn main:app --reload