from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="RetroPulse")

CardCategory = Literal["Went Well", "To Improve", "Action Items"]


class CardCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=280)
    category: CardCategory
    author: str = Field(default="Anonymous", max_length=60)

    @field_validator("text", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("author", mode="before")
    @classmethod
    def normalize_author(cls, v: str | None) -> str:
        if not v or not isinstance(v, str) or not v.strip():
            return "Anonymous"
        return v.strip()


class Card(BaseModel):
    id: int
    text: str
    category: CardCategory
    votes: int = 0
    author: str = "Anonymous"


cards_db: list[Card] = []
next_id: int = 1


@app.get("/")
def read_v1_index() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/v2")
def read_v2_index() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "v2.html")


@app.get("/api/cards", response_model=list[Card])
def list_cards() -> list[Card]:
    return cards_db


@app.post("/api/cards", response_model=Card, status_code=201)
def create_card(payload: CardCreate) -> Card:
    global next_id
    card = Card(
        id=next_id,
        text=payload.text,
        category=payload.category,
        votes=0,
        author=payload.author,
    )
    next_id += 1
    cards_db.append(card)
    return card


@app.post("/api/cards/{card_id}/upvote", response_model=Card)
def upvote_card(card_id: int) -> Card:
    for card in cards_db:
        if card.id == card_id:
            card.votes += 1
            return card
    raise HTTPException(status_code=404, detail="Card not found")


@app.delete("/api/cards", status_code=204)
def clear_cards() -> None:
    cards_db.clear()
