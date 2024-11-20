from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.mongodb import db
from app.models.content import Content, ContentType, get_hot_information, get_hot_guides, GuideContent
from app.models.response import ResponseModel, ErrorResponse
from app.models.category import Category, CategoryType
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
templates = Jinja2Templates(directory="templates")

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

@app.post("/content/")
async def create_content(content: Content):
    """创建新的内容"""
    try:
        content_dict = content.model_dump(exclude={"id"})
        content_dict["created_at"] = datetime.now(UTC)
        content_dict["updated_at"] = datetime.now(UTC)
        
        collection = db.db[content.content_type]
        result = await collection.insert_one(content_dict)
        print(f"insert result: {result}")
        
        # 查询刚插入的文档以获取完整数据
        created_content = await collection.find_one({"_id": result.inserted_id})
        print(f"created content: {created_content}")
        created_content["id"] = str(created_content.pop("_id"))  # 转换_id为id
        
        return ResponseModel[Content](
            data=Content(**created_content),
            message="内容创建成功"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建内容失败: {str(e)}")

@app.get("/content/{content_type}/{id}")
async def get_content(content_type: ContentType, id: str):
    """获取指定ID的内容"""
    try:
        collection = db.db[content_type]
        content = await collection.find_one({"_id": ObjectId(id)})
        if not content:
            raise HTTPException(status_code=404, detail="内容不存在")
        
        # 转换_id为id
        content["id"] = str(content.pop("_id"))
        
        return ResponseModel[Content](
            data=Content(**content),
            message="获取内容成功"
        )
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="无效的ID格式")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/content/{content_type}/")
async def list_contents(
    content_type: ContentType, 
    category: str = None,
    is_hot: Optional[bool] = None,
    brief: bool = False,
    skip: int = 0, 
    limit: int = 20
):
    """列出内容，支持按领域筛选、热门筛选和分页"""
    try:
        collection = db.db[content_type]
        query = {"content_type": content_type}
        if category:
            query["category.name"] = category
        if is_hot is not None:
            query["is_hot"] = is_hot
            
        # 设置投影，如果brief为True则排除content字段
        projection = {"content": 0} if brief else None

        total = await collection.count_documents(query)
        cursor = collection.find(query, projection).skip(skip).limit(limit)
        contents = await cursor.to_list(length=limit)
        
        # 转换所有文档的_id为id
        for content in contents:
            content["id"] = str(content.pop("_id"))
            # 如果是brief模式且content字段被排除，添加空的content字段以满足验证
            if brief and "content" not in content:
                content["content"] = None
        
        return ResponseModel[List[Content]](
            data=[Content(**content) for content in contents],
            message="获取内容列表成功",
            meta={
                "total": total,
                "skip": skip,
                "limit": limit
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/content/{content_type}/{id}")
async def update_content(content_type: ContentType, id: str, content: Content):
    """更新指定ID的内容"""
    try:
        collection = db.db[content_type]
        update_data = content.model_dump(exclude={"id"})
        update_data["updated_at"] = datetime.now(UTC)
        
        result = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="内容不存在")
            
        # 转换_id为id
        result["id"] = str(result.pop("_id"))
        
        return ResponseModel[Content](
            data=Content(**result),
            message="内容更新成功"
        )
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="无效的ID格式")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/content/{content_type}/{id}")
async def delete_content(content_type: ContentType, id: str):
    """删除指定ID的内容"""
    try:
        collection = db.db[content_type]
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="内容不存在")
        return ResponseModel(message="内容删除成功")
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="无效的ID格式")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/content/{content_type}/{id}/hot")
async def set_content_hot_status(
    content_type: ContentType,
    id: str,
    is_hot: bool
):
    """设置或取消内容的热门状态"""
    try:
        collection = db.db[content_type]
        result = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "is_hot": is_hot,
                    "updated_at": datetime.now(UTC)
                }
            },
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="内容不存在")
            
        result["id"] = str(result.pop("_id"))
        
        return ResponseModel[Content](
            data=Content(**result),
            message="热门状态更新成功"
        )
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="无效的ID格式")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

@app.get("/hot/{content_type}")
async def get_hot_content(content_type: ContentType, brief: bool = False):
    try:
        if content_type == ContentType.INFORMATION:
            info_list = await get_hot_information()
        elif content_type == ContentType.GUIDE:
            guide_list = await get_hot_guides()
            
        # 设置投影，如果brief为True则排除content字段
        projection = {"content": 0} if brief else None

        # 使用content api的list_contents方法
        contents = await list_contents(content_type, is_hot=True, brief=brief)
        
        return ResponseModel[List[Content]](
            data=contents.data,
            message="获取热门内容成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/category/")
async def create_category(category: Category):
    """创建新的分类"""
    try:
        category_dict = category.model_dump(exclude={"id"})
        category_dict["created_at"] = datetime.now(UTC)
        category_dict["updated_at"] = datetime.now(UTC)
        
        collection = db.db["category"]
        result = await collection.insert_one(category_dict)
        
        created_category = await collection.find_one({"_id": result.inserted_id})
        created_category["id"] = str(created_category.pop("_id"))
        
        return ResponseModel[Category](
            data=Category(**created_category),
            message="分类创建成功"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建分类失败: {str(e)}")

@app.get("/category/{id}")
async def get_category(id: str):
    """获取指定ID的分类"""
    try:
        collection = db.db["category"]
        category = await collection.find_one({"_id": ObjectId(id)})
        if not category:
            raise HTTPException(status_code=404, detail="分类不存在")
        
        category["id"] = str(category.pop("_id"))
        
        return ResponseModel[Category](
            data=Category(**category),
            message="获取分类成功"
        )
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="无效的ID格式")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/category/")
async def list_categories(category_type: Optional[CategoryType] = None, parent_id: Optional[str] = None):
    """列出所有分类，支持按父分类筛选"""
    try:
        collection = db.db["category"]
        query = {}
        if category_type:
            query["category_type"] = category_type
        if parent_id:
            query["parent_id"] = parent_id
            
        cursor = collection.find(query)
        categories = await cursor.to_list(length=100)  # 假设分类数量不会太多
        
        for category in categories:
            category["id"] = str(category.pop("_id"))
        
        return ResponseModel[List[Category]](
            data=[Category(**category) for category in categories],
            message="获取分类列表成功"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/category/{id}")
async def update_category(id: str, category: Category):
    """更新指定ID的分类"""
    try:
        collection = db.db["category"]
        update_data = category.model_dump(exclude={"id"})
        update_data["updated_at"] = datetime.now(UTC)
        
        result = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="分类不存在")
            
        result["id"] = str(result.pop("_id"))
        
        return ResponseModel[Category](
            data=Category(**result),
            message="分类更新成功"
        )
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="无效的ID格式")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/category/{id}")
async def delete_category(id: str):
    """删除指定ID的分类"""
    try:
        collection = db.db["category"]
        # 检查是否有子分类
        children = await collection.find_one({"parent_id": id})
        if children:
            raise HTTPException(status_code=400, detail="无法删除含有子分类的分类")
            
        # 检查是否有关联的内容
        for content_type in ContentType:
            content_collection = db.db[content_type]
            related_content = await content_collection.find_one({"category.id": id})
            if related_content:
                raise HTTPException(status_code=400, detail="无法删除已被内容使用的分类")
        
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="分类不存在")
            
        return ResponseModel(message="分类删除成功")
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="无效的ID格式")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

