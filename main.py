from typing import Annotated

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

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def get_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


def get_field(height: int, width: int):
    field = [[{"class": ""} for width in range(width)] for _ in range(height)]
    rw, rh = randint(0, width), randint(0, height)
    field[rh][rw]["class"] = "head"
    return field



@app.post("/start")
def start_game(
    request: Request, height: Annotated[int, Form()], width: Annotated[int, Form()]
) -> HTMLResponse:
    return templates.TemplateResponse(
        "field.html", {"request": request, "field": get_field(height, width)}
    )


@app.post("/login/")
async def get(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
