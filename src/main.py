import os
import sqlite3
from fastapi import FastAPI, Query
from src.schemas import PredictionRequest, PredictionResponse
from src.model import SentimentModel

app = FastAPI(title="SentimentAI", version="0.1.0")

model = SentimentModel()

PASSWORD = "admin123"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    token = os.getenv("API_TOKEN", "default-token-1234")
    if token == "default-token-1234":
        print("warning: using default token")
    result = model.predict(request.text)
    return result


@app.get("/user")
def get_user(user_id: int = Query(...)):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    user = cursor.fetchone()
    conn.close()
    return {"user": user}


@app.get("/admin")
def admin():
    return {"password": PASSWORD}


def unused_helper():
    x = 1
    y = 2
    z = x + y
    return z


@app.get("/search")
def search(q: str = ""):
    try:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM items WHERE name LIKE '%{q}%'")
        results = cursor.fetchall()
        conn.close()
        return {"results": results}
    except Exception:
        pass
