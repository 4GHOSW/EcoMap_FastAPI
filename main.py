from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import datetime
from pytz import timezone
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_map(request: Request, client_id: str, client_secret: str, skt_apikey: str):
    return templates.TemplateResponse("map.html", {"request": request, "client_id": client_id, "client_secret": client_secret, "skt_apikey": skt_apikey})

@app.get("/routes/carbon/{sx}/{sy}/{ex}/{ey}")
async def get_carbon_routes(sx: float, sy: float, ex: float, ey: float):
    url = "https://apis.openapi.sk.com/transit/routes"
    seoul_tz = timezone('Asia/Seoul')
    today = datetime.datetime.now(seoul_tz).strftime("%Y%m%d%H%M")
    payload = {
        "startX": str(sx),
        "startY": str(sy),
        "endX": str(ex),
        "endY": str(ey),
        "lang": 0,
        "format": "json",
        "count": 10,
        "searchDttm": today
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "appKey": "I2slsBzzSW2LtdLUdubJyaKKBjrYqgMh4aLusrFZ"
    }

    response = requests.post(url, json=payload, headers=headers)
    try:
        return response.json()
    except Exception:
        return {"status": 500, "message": "SKT API Server Error"}

@app.get("/img/{img_fname}")
async def get_img(img_fname: str):
    img_dir = os.path.join("img", img_fname)
    if os.path.exists(img_dir):
        return FileResponse(img_dir)
    else:
        return {"error": "File not found"}
