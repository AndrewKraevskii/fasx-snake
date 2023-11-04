from typing import Annotated, List, Dict, Any

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    status,
    Request,
    Form,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from random import randint
from pydantic import BaseModel
import json


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def get_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


def get_field(height: int, width: int):
    field = [[{"cell_class": ""} for width in range(width)] for _ in range(height)]
    rw, rh = randint(0, width - 1), randint(0, height - 1)
    field[rh][rw]["cell_class"] = "head"
    return field


def add_to_field(field: list[list[dict]]):
    rw, rh = randint(0, len(field[0]) - 1), randint(0, len(field) - 1)
    field[rh][rw]["cell_class"] = "head"
    return field


@app.post("/start")
def start_game(
    request: Request, height: Annotated[int, Form()], width: Annotated[int, Form()]
) -> HTMLResponse:
    return templates.TemplateResponse(
        "field.html", {"request": request, "field": get_field(height, width)}
    )


class Cell(BaseModel):
    cell_class: str


class Field(BaseModel):
    field: list[list[Cell]]


@app.post("/update")
def start_game(request: Request, field: Annotated[Any, Form()]) -> HTMLResponse:
    # TODO: find way to check for list[list[dict]] in Form without json.loads
    field = json.loads(field)
    return templates.TemplateResponse(
        "field.html", {"request": request, "field": add_to_field(field)}
    )
