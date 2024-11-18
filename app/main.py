from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.db.mongodb import db
from app.models.content import Content, ContentType
from app.models.response import ResponseModel, ErrorResponse
from typing import List
from bson import ObjectId, errors as bson_errors
from datetime import datetime, UTC
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
    domain: str = None, 
    skip: int = 0, 
    limit: int = 20
):
    """列出内容，支持按领域筛选和分页"""
    try:
        collection = db.db[content_type]
        query = {"content_type": content_type}
        if domain:
            query["domain.name"] = domain
            
        total = await collection.count_documents(query)
        cursor = collection.find(query).skip(skip).limit(limit)
        contents = await cursor.to_list(length=limit)
        
        # 转换所有文档的_id为id
        for content in contents:
            content["id"] = str(content.pop("_id"))
        
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