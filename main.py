from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_map(request: Request, client_id: str):
    return templates.TemplateResponse("map.html", {"request": request, "client_id": client_id})

@app.get("/get_coordinates")
async def get_coordinates(query: str, client_id: str):
    url = f"https://openapi.map.naver.com/v1/geocode?query={query}&client_id={client_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if data["addresses"]:
            lat = float(data["addresses"][0]["y"])
            lng = float(data["addresses"][0]["x"])
            return {"lat": lat, "lng": lng}
    return {"lat": None, "lng": None}



