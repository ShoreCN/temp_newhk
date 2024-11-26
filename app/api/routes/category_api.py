from fastapi import APIRouter, HTTPException
from typing import List, Optional
from bson import ObjectId, errors as bson_errors
from datetime import datetime, UTC
from app.models.category import Category, CategoryType
from app.models.response import ResponseModel
from app.models.content import ContentType
from app.db.mongodb import db

router = APIRouter(
    prefix="/category",
    tags=["category"]
)

@router.post("/")
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

@router.get("/{id}")
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

@router.get("/")
async def list_categories(category_type: Optional[CategoryType] = None, parent_id: Optional[str] = None):
    """列出所有分类，支持按父分类筛选"""
    try:
        collection = db.db["category"]
        query = {}
        if category_type:
            query["category_type"] = category_type
        if parent_id:
            query["parent_id"] = parent_id
            
        total = await collection.count_documents(query)
        cursor = collection.find(query)
        categories = await cursor.to_list(length=100)
        
        for category in categories:
            category["id"] = str(category.pop("_id"))
        
        return ResponseModel[List[Category]](
            data=[Category(**category) for category in categories],
            message="获取分类列表成功",
            meta={
                "total": total,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}")
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

@router.delete("/{id}")
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