from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_map(request: Request, client_id: str, client_secret: str, odsay_apikey: str):
    return templates.TemplateResponse("map.html", {"request": request, "client_id": client_id, "client_secret": client_secret, "odsay_apikey": odsay_apikey})

@app.get("/img/{img_fname}")
async def get_img(img_fname: str):
    # 이미지 파일이 저장된 디렉토리
    img_dir = os.path.join("img", img_fname)  # 'images' 폴더 안에 있는 파일을 찾음
    if os.path.exists(img_dir):
        return FileResponse(img_dir)  # 이미지 파일 반환
    else:
        return {"error": "File not found"}  # 파일이 존재하지 않을 경우 에러 메시지 반환