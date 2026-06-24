import logging
import sqlite3
from fastapi import FastAPI, HTTPException, Query
from src.schemas import PredictionRequest, PredictionResponse
from src.model import SentimentModel

logger = logging.getLogger(__name__)
app = FastAPI(title="SentimentAI", version="0.1.0")
model = SentimentModel()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    result = model.predict(request.text)
    return result


@app.get("/user")
def get_user(user_id: int = Query(...)):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}


@app.get("/search")
def search(q: str = ""):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE name LIKE ?", (f"%{q}%",))
    results = cursor.fetchall()
    conn.close()
    return {"results": results}
