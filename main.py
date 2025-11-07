from fastapi import FastAPI
from uvicorn import run
from app.controllers import opencv_app_router


app = FastAPI(title='FastAPI + OpenCV Video Analyzer')

app.include_router(opencv_app_router, prefix='/opencv_app')


if __name__ == "__main__":
    run(
        app="main:app",
        reload=True,
        log_level="debug",
        host="localhost",
        port=8000,
    )