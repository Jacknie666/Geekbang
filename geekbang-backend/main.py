
from fastapi import FastAPI

from api_v1.user import router as user_router

app = FastAPI()

app.include_router(user_router)
@app.get("/")
async def root():
    return "hello! Geekbang"

