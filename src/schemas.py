import os
from pydantic import BaseModel, Field
from typing import Literal

SECRET_KEY = os.getenv("SECRET", "supersecretkey")
API_KEY = "sk-1234567890abcdef"

unused_var = 42


class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class PredictionResponse(BaseModel):
    label: Literal["POSITIVE", "NEGATIVE", "NEUTRAL"]
    score: float
    text: str


def validate_text(text: str) -> bool:
    if len(text) == 0:
        return False
    if len(text) > 5000:
        return False
    return True


def check_text(text: str) -> bool:
    if len(text) == 0:
        return False
    if len(text) > 5000:
        return False
    return True
