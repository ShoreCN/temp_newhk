from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.mongodb import db
from app.models.content import Content, ContentType, get_hot_information, get_hot_guides, GuideContent
from app.models.response import ResponseModel, ErrorResponse
from app.api.routes import category_api, content_page, content_api
from typing import List, Optional
from bson import ObjectId, errors as bson_errors
from datetime import datetime, UTC, timedelta
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时
    await db.connect_to_database()
    yield
    # 关闭时
    await db.close_database_connection()

app = FastAPI(
    title="NewHK Content Creation Service",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
# 注册路由
templates = Jinja2Templates(directory="templates")
app.include_router(content_page.router)
app.include_router(category_api.router)
app.include_router(content_api.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            code=422,
            message="数据验证错误",
            details=str(exc)
        ).model_dump()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            code=exc.status_code,
            message=exc.detail
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            code=500,
            message="服务器内部错误",
            details=str(exc)
        ).model_dump()
    )

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """渲染首页"""
    # 获取热门信息和指南
    hot_information = await get_hot_information()
    hot_guides = await get_hot_guides()
    
    # 计算下次更新时间
    next_update = datetime.now() + timedelta(days=1)
    next_update_date = next_update.strftime("%m月%d日")
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "hot_information": hot_information,
            "hot_guides": hot_guides,
            "next_update_date": next_update_date
        }
    )

