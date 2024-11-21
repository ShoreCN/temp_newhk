from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.content import get_hot_information, get_hot_guides
from app.models.category import get_categories
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/information", response_class=HTMLResponse)
async def information_page(request: Request):
    # 获取所有分类
    categories = await get_categories()
    
    # 获取资讯内容
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    cursor = db.information.find(
        {},
        {'_id': 0}
    ).sort("created_at", -1)
    information_list = await cursor.to_list(length=20)
    
    return templates.TemplateResponse(
        "information.html",
        {
            "request": request,
            "categories": categories,
            "information_list": information_list
        }
    ) 