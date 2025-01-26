from fastapi import APIRouter, HTTPException
from app.db.mongodb import db
from app.models.content import (
    Content, ContentType, get_hot_information, get_hot_guides,
    SearchSuggestion, SearchSuggestionType, SearchContentType
)
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
            
        projection = {"data.metrics.description": 0, "data.data_table": 0} if brief else None

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

@router.get("/{content_type}/search")
async def search_content(
    content_type: SearchContentType,
    q: str,
    brief: bool = True,
    skip: int = 0,
    limit: int = 20
):
    """搜索内容
    
    可搜索字段:
    - topic (主题)
    - title (对外标题)
    - source_list[].name (来源名称)
    - data[].name (仅对资讯类内容)
    """
    try:
        collection = db.db[content_type]
        
        # 构建搜索条件
        search_query = {
            "$and": [
                {"$or": [
                    {"topic": {"$regex": q, "$options": "i"}},
                    {"title": {"$regex": q, "$options": "i"}},
                    {"source_list.name": {"$regex": q, "$options": "i"}},
                ]}
            ]
        }

        # 如果不是选择全部内容进行搜索时, 添加content_type的过滤条件
        if content_type != SearchContentType.ALL:
            search_query["$and"].append({"content_type": content_type})
        
        # 如果是资讯类内容，增加对data.name的搜索
        if content_type == SearchContentType.INFORMATION:
            search_query["$and"][0]["$or"].append(
                {"data.name": {"$regex": q, "$options": "i"}}
            )
        
        # 设置查询投影
        projection = {"data.metrics.description": 0, "data.data_table": 0} if brief else None
            
        # 执行查询
        cursor = collection.find(
            search_query,
            projection=projection
        ).skip(skip).limit(limit)
        contents = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            contents.append(Content(**doc))
            
        # 获取总数
        total = await collection.count_documents(search_query)
        
        return ResponseModel[List[Content]](
            data=contents,
            message="搜索成功",
            meta={
                "total": total,
                "skip": skip,
                "limit": limit
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"搜索失败: {str(e)}")

@router.get("/{content_type}/search/suggestions", response_model=ResponseModel[List[SearchSuggestion]])
async def get_search_suggestions(
    content_type: SearchContentType,
    q: str = "",
    limit: int = 10
):
    """获取搜索建议关键词
    
    基于以下数据源提供搜索建议:
    - 热门内容的标题和主题
    - 相关标签
    - 相关分类
    - 相关来源
    """
    try:
        if not q:
            # 如果q参数为空, 则暂时使用模拟数据
            suggestions = [
                {
                    "suggestion_type": "topic",
                    "content_type": ContentType.GUIDES,
                    "name": "银行开户便利排行",
                    "id": "xxxxxxxx"
                },
                {
                    "suggestion_type": "topic",
                    "content_type": ContentType.GUIDES,
                    "name": "日本大使馆",
                    "id": "xxxxxxxx"
                },
                {
                    "suggestion_type": "topic",
                    "content_type": ContentType.GUIDES,
                    "name": "签证费用",
                    "id": "xxxxxxxx"
                },
                {
                    "suggestion_type": "topic",
                    "content_type": ContentType.GUIDES,
                    "name": "银行开户资金",
                    "id": "xxxxxxxx"
                },
                {
                    "suggestion_type": "topic",
                    "content_type": ContentType.GUIDES,
                    "name": "澳洲签证",
                    "id": "xxxxxxxx"
                },
                {
                    "suggestion_type": "topic",
                    "content_type": ContentType.GUIDES,
                    "name": "工签续签",
                    "id": "xxxxxxxx"
                },
            ]
        else:
        
            # 构建聚合管道
            pipeline = [
                # 匹配相关内容
                {"$match": {
                    "$or": [
                        {"topic": {"$regex": q, "$options": "i"}},
                        {"title": {"$regex": q, "$options": "i"}},
                        {"tags": {"$regex": q, "$options": "i"}},
                        {"category": {"$regex": q, "$options": "i"}},
                        {"source_list.name": {"$regex": q, "$options": "i"}}
                    ]
                }},
                # 使用facet进行分组聚合
                {"$facet": {
                    "topics": [
                        {"$match": {"is_hot": True}},
                        {"$project": {
                            "_id": {"$toString": "$_id"},
                            "name": "$topic",
                            "suggestion_type": {"$literal": "topic"},
                            "content_type": {"$literal": content_type},
                            "data": {
                                "title": "$title",
                                "category": "$category",
                                "is_hot": "$is_hot"
                            }
                        }},
                        {"$limit": limit}
                    ],
                    "titles": [
                        {"$match": {"title": {"$exists": True}}},
                        {"$project": {
                            "_id": {"$toString": "$_id"},
                            "name": "$title",
                            "suggestion_type": {"$literal": "title"},
                            "content_type": {"$literal": content_type},
                            "data": {
                                "topic": "$topic",
                                "category": "$category",
                                "is_hot": "$is_hot"
                            }
                        }},
                        {"$limit": limit}
                    ],
                    "tags": [
                        {"$unwind": "$tags"},
                        {"$group": {
                            "_id": "$tags",
                            "count": {"$sum": 1},
                            "categories": {"$addToSet": "$category"},
                            "sample_id": {"$first": {"$toString": "$_id"}}
                        }},
                        {"$project": {
                            "_id": "$sample_id",
                            "name": "$_id",
                            "suggestion_type": {"$literal": "tag"},
                            "content_type": {"$literal": content_type},
                            "data": {
                                "count": "$count",
                                "categories": "$categories"
                            }
                        }},
                        {"$sort": {"data.count": -1}},
                        {"$limit": limit}
                    ],
                    "categories": [
                        {"$group": {
                            "_id": "$category",
                            "count": {"$sum": 1},
                            "sample_id": {"$first": {"$toString": "$_id"}}
                        }},
                        {"$project": {
                            "_id": "$sample_id",
                            "name": "$_id",
                            "suggestion_type": {"$literal": "category"},
                            "content_type": {"$literal": content_type},
                            "data": {
                                "count": "$count"
                            }
                        }},
                        {"$sort": {"data.count": -1}},
                        {"$limit": limit}
                    ],
                    "sources": [
                        {"$unwind": "$source_list"},
                        {"$group": {
                            "_id": "$source_list.name",
                            "count": {"$sum": 1},
                            "sample_id": {"$first": {"$toString": "$_id"}},
                            "logo": {"$first": "$source_list.logo"}
                        }},
                        {"$project": {
                            "_id": "$sample_id",
                            "name": "$_id",
                            "suggestion_type": {"$literal": "source"},
                            "content_type": {"$literal": content_type},
                            "data": {
                                "count": "$count",
                                "logo": "$logo"
                            }
                        }},
                        {"$sort": {"data.count": -1}},
                        {"$limit": limit}
                    ]
                }},
                # 合并所有建议
                {"$project": {
                    "suggestions": {
                        "$concatArrays": ["$topics", "$titles", "$tags", "$categories", "$sources"]
                    }
                }}
            ]

            if content_type != SearchContentType.ALL:
                collection = db.db[content_type]
                result = await collection.aggregate(pipeline).to_list(length=1)
                suggestions = result[0]["suggestions"] if result else []
            else:
                suggestions = []
                for content_type_i in ContentType:
                    # 寻找pipeline中的content_type, 进行修改
                    for stage in pipeline:
                        for facet in stage.get("$facet", {}):
                            for sub_pipeline in stage["$facet"][facet]:
                                if sub_pipeline.get("$project", {}).get("content_type"):
                                    sub_pipeline["$project"]["content_type"] = content_type_i.value
                        
                    collection = db.db[content_type_i.value]
                    result = await collection.aggregate(pipeline).to_list(length=1)
                    suggestions.extend(result[0]["suggestions"] if result else [])

        # Convert to SearchSuggestion model
        suggestions = [
            SearchSuggestion(
                suggestion_type=suggestion["suggestion_type"],
                content_type=suggestion["content_type"],
                name=suggestion["name"],
                id=suggestion.get("id"),
                data=suggestion.get("data")
            )
            for suggestion in suggestions
        ]
        
        return ResponseModel(
            data=suggestions,
            message="获取搜索建议成功",
            meta={"total": len(suggestions)}
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获取搜索建议失败: {str(e)}")
        

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
