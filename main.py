from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_map(request: Request, client_id: str, client_secret: str):
    return templates.TemplateResponse("map.html", {"request": request, "client_id": client_id, "client_secret": client_secret})


