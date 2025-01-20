from fastapi import APIRouter, HTTPException, Depends
from app.models.ai_chat import ChatRequest, ChatResponse
from app.services.ai_service import AIService
from app.models.response import ResponseModel
from datetime import datetime, timedelta

router = APIRouter(prefix="/ai", tags=["AI"])
ai_service = AIService()

@router.post("/chat", response_model=ResponseModel[ChatResponse])
async def chat(request: ChatRequest):
    # 检查频率限制
    if not await ai_service.check_rate_limit(request.device_id):
        raise HTTPException(429, "已超过API调用限制")
    
    # 获取或创建会话
    session = None
    if request.session_id:
        session = await ai_service.get_session(request.session_id)
        if session:
            # 检查会话是否过期
            if datetime.now() - session.created_at > timedelta(days=1):
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