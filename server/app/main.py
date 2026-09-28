from fastapi import FastAPI
from app.routes.webhook import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(router, prefix="/webhook")


@app.get("/")
def home():
    return {"status": "running"}
