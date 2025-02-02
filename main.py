from fastapi import FastAPI
import uvicorn


app = FastAPI()

@app.get("/")
async def hello_world():

    return "Hello World"

if __name__ == "__main__":

    try:
        uvicorn.run(app, port=8000, host="127.0.0.1")
    except Exception as e:
        print("Ошибка в программе", e)

# run uvicorn main:app --reload