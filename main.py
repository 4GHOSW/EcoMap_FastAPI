from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

@app.get("/map/{client_id}/{lat}/{lng}", response_class=HTMLResponse)
async def get_map(
    request: Request,
    client_id: str,  # 클라이언트 ID를 쿼리 파라미터로 받기
    lat: float,  # 기본값 설정
    lng: float    # 기본값 설정
):
    return templates.TemplateResponse("map.html", {
        "request": request,
        "client_id": client_id,
        "lat": lat,
        "lng": lng
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

