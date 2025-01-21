from fastapi import APIRouter, HTTPException, Depends
from app.models.ai_chat import ChatRequest, ChatResponse, ChatHistoryResponse
from app.services.ai_service import AIService
from app.models.response import ResponseModel
from datetime import datetime, timedelta
from typing import List, Optional

router = APIRouter(prefix="/ai", tags=["AI"])
ai_service = AIService()

@router.post("/chat", response_model=ResponseModel[ChatResponse])
async def chat(request: ChatRequest):
    """
    进行对话
    - 如果未提供session_id, 则创建一个新的会话;  
    - 同时提供session_id和device_id, 才能继续历史会话;  
    - 如果获取不到会话历史, 则创建一个新的会话;
    - 如果会话过期, 则创建一个新的会话. 每条会话有效期为24小时.
    
    Args:  
        session_id: 会话ID  
        device_id: 设备ID  
        message: 对话内容  

    Raises:  
        HTTPException: 超过API调用限制

    Returns:  
        session_id: 会话ID  
        message: 对话内容  
        sources: 来源  
    """
    # 检查频率限制
    if not await ai_service.check_rate_limit(request.device_id):
        raise HTTPException(429, "已超过API调用限制")
    
    # 获取或创建会话
    session = None
    if request.session_id and request.device_id:
        session = await ai_service.get_session(request.session_id, request.device_id)
        if session:
            # 检查会话是否过期
            if datetime.now() - session.created_at > timedelta(days=1):
                print(f"会话{request.session_id}已过期, 重新创建")
                session = None
    
    if not session:
        session = await ai_service.create_session(request.device_id)
    
    # 进行对话
    message, sources = await ai_service.chat(session, request.message)
    
    return ResponseModel(data=ChatResponse(
        session_id=session.session_id,
        message=message,
        sources=sources
    ))

@router.get("/chat/history", response_model=ResponseModel[ChatHistoryResponse])
async def get_chat_history(
    device_id: str,
    session_id: str,
    limit: int = 20,
    offset: int = 0
):
    """
    获取历史对话记录
    
    Args:  
        device_id: 设备ID  
        session_id: 会话ID  
        limit: 返回记录数量限制  
        offset: 分页偏移量  
    """
    try:
        history, total = await ai_service.get_chat_history(
            device_id=device_id,
            session_id=session_id,
            limit=limit,
            offset=offset
        )
        return ResponseModel(data=history, meta={"total": total, "offset": offset, "limit": limit})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}") 
