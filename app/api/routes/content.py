from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.content import get_hot_information, get_hot_guides
from app.models.category import get_categories
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from bson.objectid import ObjectId

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
    ).sort("created_at", -1)
    information_list = await cursor.to_list(length=20)
    # 转换所有文档的_id为id
    for content in information_list:
        content["id"] = str(content.pop("_id"))
    
    return templates.TemplateResponse(
        "information.html",
        {
            "request": request,
            "categories": categories,
            "information_list": information_list
        }
    )

@router.get("/information/edit", response_class=HTMLResponse)
async def information_edit_page(request: Request, id: str = None):
    # 获取所有分类
    categories = await get_categories()
    
    # 如果提供了id，获取现有内容
    content = None
    if id:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        content = await db.information.find_one({"_id": ObjectId(id)})
    
    return templates.TemplateResponse(
        "information_edit.html",
        {
            "request": request,
            "categories": categories,
            "content": content
        }
    )
