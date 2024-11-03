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
    return templates.TemplateResponse("map.html", {
        "request": request,
        "client_id": client_id,
        "client_secret": client_secret,
        "skt_apikey": skt_apikey
    })

@app.get("/routes/carbon/{sx}/{sy}/{ex}/{ey}")
async def get_carbon_routes(sx: float, sy: float, ex: float, ey: float, apiKey: str):
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
        "appKey": apiKey
    }

    response = requests.post(url, json=payload, headers=headers)
    
    try:
        pre_result = response.json().get("metaData", {}).get("plan", {}).get("itineraries", [])
        result = []
        totTimes = []
        for item in pre_result:
            buf = []
            totTime = 0
            for jtem in item.get("legs", []):
                if "steps" in jtem:
                    part_dist = 0
                    path = []
                    for ktem in jtem["steps"]:
                        part_dist += ktem["distance"]
                        path_buf = ktem["linestring"].split()[:-1]
                        for path_ in path_buf:
                            path_ = path_.split(",")
                            path.append(path_)
                    velocity = (part_dist / 1000) / (jtem["sectionTime"] / 60 / 60)

                    buf.append({
                        "mode": "WALK",
                        "part_distance": part_dist / 1000,
                        "part_time": jtem["sectionTime"] / 60 / 60,
                        "path": path,
                        "velocity": velocity,
                        "CO2": 0,
                    })
                    totTime += jtem["sectionTime"] / 60 / 60
                if "passShape" in jtem:
                    path = []
                    path_buf = jtem["passShape"]["linestring"].split()
                    for path_ in path_buf:
                        path_ = path_.split(",")
                        path.append(path_)
                    
                    velocity = (jtem["distance"] / 1000) / (jtem["sectionTime"] / 60 / 60)
                    
                    buf.append({
                        "mode": "BUS",
                        "part_distance": jtem["distance"] / 1000,
                        "part_time": jtem["sectionTime"] / 60 / 60,
                        "path": path,
                        "velocity": velocity,
                        "CO2": (jtem["distance"] / 1000) * 5054.5880 * velocity ** (-0.4910)
                    })
                    totTime += jtem["sectionTime"] / 60 / 60
            totTimes.append(totTime)
            result.append(buf)
        
        return {"routes": result}  # Return wrapped in a dict for clarity
    except Exception as e:
        return {"status": 500, "message": str(e)}

@app.get("/img/{img_fname}")
async def get_img(img_fname: str):
    img_dir = os.path.join("img", img_fname)
    if os.path.exists(img_dir):
        return FileResponse(img_dir)
    else:
        return {"error": "File not found"}