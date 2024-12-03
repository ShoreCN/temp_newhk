from fastapi import APIRouter, HTTPException
from app.db.mongodb import db
from app.models.content import Content, ContentType, get_hot_information, get_hot_guides
from app.models.response import ResponseModel
from typing import List, Optional
from bson import ObjectId, errors as bson_errors
from datetime import datetime

router = APIRouter(
    prefix="/content",
    tags=["content"]
)

@router.post("/")
async def create_content(content: Content):
    """创建新的内容"""
    try:
        content_dict = content.model_dump(exclude={"id"})
        content_dict["created_at"] = int(datetime.now().timestamp())
        content_dict["updated_at"] = int(datetime.now().timestamp())
        
        collection = db.db[content.content_type]
        result = await collection.insert_one(content_dict)
        
        # 查询刚插入的文档以获取完整数据
        created_content = await collection.find_one({"_id": result.inserted_id})
        created_content["id"] = str(created_content.pop("_id"))
        
        return ResponseModel[Content](
            data=Content(**created_content),
            message="内容创建成功"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建内容失败: {str(e)}")

@router.get("/{content_type}/{id}")
async def get_content(content_type: ContentType, id: str):
    """获取指定ID的内容"""
    try:
        collection = db.db[content_type]
        content = await collection.find_one({"_id": ObjectId(id)})
        if not content:
            raise HTTPException(status_code=404, detail="内容不存在")
        
        content["id"] = str(content.pop("_id"))
        
        return ResponseModel[Content](
            data=Content(**content),
            message="获取内容成功"
        )
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="无效的ID格式")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{content_type}/")
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
            query["category"] = category
        if is_hot is not None:
            query["is_hot"] = is_hot
            
        projection = {"data": 0} if brief else None

        total = await collection.count_documents(query)
        cursor = collection.find(query, projection).skip(skip).limit(limit)
        contents = await cursor.to_list(length=limit)
        
        for content in contents:
            content["id"] = str(content.pop("_id"))
            if brief and "data" not in content:
                content["data"] = None
        
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

@router.put("/{content_type}/{id}")
async def update_content(content_type: ContentType, id: str, content: Content):
    """更新指定ID的内容"""
    try:
        collection = db.db[content_type]
        update_data = content.model_dump(exclude={"id"})
        update_data["updated_at"] = int(datetime.now().timestamp())
        
        result = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="内容不存在")
            
        result["id"] = str(result.pop("_id"))
        
        return ResponseModel[Content](
            data=Content(**result),
            message="内容更新成功"
        )
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="无效的ID格式")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{content_type}/{id}")
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

@router.patch("/{content_type}/{id}/hot")
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
                    "updated_at": int(datetime.now().timestamp())
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

@router.get("/hot/{content_type}")
async def get_hot_content(content_type: ContentType, brief: bool = False):
    try:
        if content_type == ContentType.INFORMATION:
            info_list = await get_hot_information()
        elif content_type == ContentType.GUIDE:
            guide_list = await get_hot_guides()
            
        projection = {"content": 0} if brief else None

        contents = await list_contents(content_type, is_hot=True, brief=brief)
        
        return ResponseModel[List[Content]](
            data=contents.data,
            message="获取热门内容成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
