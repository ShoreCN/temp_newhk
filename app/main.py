from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db.mongodb import db
from app.models.content import Content, ContentType
from typing import List
from bson import ObjectId

app = FastAPI(title="NewHK Content Creation Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await db.connect_to_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close_database_connection()

@app.post("/content/", response_model=Content)
async def create_content(content: Content):
    """创建新的内容"""
    collection = db.db[content.content_type]
    result = await collection.insert_one(content.dict(by_alias=True))
    content.id = str(result.inserted_id)
    return content

@app.get("/content/{content_type}/{id}", response_model=Content)
async def get_content(content_type: ContentType, id: str):
    """获取指定ID的内容"""
    try:
        collection = db.db[content_type]
        content = await collection.find_one({"_id": ObjectId(id)})
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        return Content(**content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/content/{content_type}/", response_model=List[Content])
async def list_contents(content_type: ContentType, domain: str = None, skip: int = 0, limit: int = 20):
    """列出内容，支持按领域筛选和分页"""
    collection = db.db[content_type]
    query = {"content_type": content_type}
    if domain:
        query["domain.name"] = domain
        
    cursor = collection.find(query).skip(skip).limit(limit)
    contents = await cursor.to_list(length=limit)
    return [Content(**content) for content in contents]

@app.put("/content/{content_type}/{id}", response_model=Content)
async def update_content(content_type: ContentType, id: str, content: Content):
    """更新指定ID的内容"""
    try:
        collection = db.db[content_type]
        update_data = content.dict(exclude={"id"}, by_alias=True)
        result = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=True
        )
        if not result:
            raise HTTPException(status_code=404, detail="Content not found")
        return Content(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/content/{content_type}/{id}")
async def delete_content(content_type: ContentType, id: str):
    """删除指定ID的内容"""
    try:
        collection = db.db[content_type]
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Content not found")
        return {"message": "Content deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 