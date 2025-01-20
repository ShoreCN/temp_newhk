from openai import OpenAI
from app.core.config import settings
from app.models.ai_chat import ChatSession, Message, MessageRole
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.AI_API_KEY,
            base_url=settings.AI_API_BASE_URL
        )
        self.db_client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.db_client[settings.DATABASE_NAME]
        # 为chat_sessions创建一个TTL索引(24小时之后自动删除)
        self.db.chat_sessions.create_index([("created_at", 1)], expireAfterSeconds=86400)
        # 为chat_requests创建一个TTL索引(36小时之后自动删除)
        self.db.chat_requests.create_index([("created_at", 1)], expireAfterSeconds=129600)

    async def get_session(self, session_id: str) -> ChatSession:
        session_data = await self.db.chat_sessions.find_one({"session_id": session_id})
        if not session_data:
            return None
        return ChatSession(**session_data)
        
    async def create_session(self, device_id: str) -> ChatSession:
        session = ChatSession(
            session_id=str(ObjectId()),
            device_id=device_id,
            messages=[
                Message(
                    role=MessageRole.SYSTEM,
                    content="你是一个帮助新来香港的人解答问题的AI助手。请提供准确、有帮助的信息。"
                )
            ],
            created_at=int(datetime.now().timestamp()),
            updated_at=int(datetime.now().timestamp())
        )
        await self.db.chat_sessions.insert_one(session.model_dump())
        return session
        
    async def check_rate_limit(self, device_id: str) -> bool:
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        # 检查小时限制
        hour_count = await self.db.chat_requests.count_documents({
            "device_id": device_id,
            "created_at": {"$gte": hour_ago}
        })
        if hour_count >= 10:
            return False
            
        # 检查天限制
        day_count = await self.db.chat_requests.count_documents({
            "device_id": device_id,
            "created_at": {"$gte": day_ago}
        })
        if day_count >= 30:
            return False
            
        return True
        
    async def chat(self, session: ChatSession, message: str) -> tuple[str, list]:
        # 记录用户请求
        await self.db.chat_requests.insert_one({
            "device_id": session.device_id,
            "created_at": datetime.now()
        })
        
        # 添加用户消息
        session.messages.append(Message(role=MessageRole.USER, content=message))
        
        # 调用AI API
        response = self.client.chat.completions.create(
            model=settings.AI_MODEL_NAME,
            messages=[m.model_dump() for m in session.messages],
            stream=False
        )
        
        ai_message = response.choices[0].message.content
        
        # 添加AI回复
        session.messages.append(Message(role=MessageRole.ASSISTANT, content=ai_message))
        session.updated_at = datetime.now()
        
        # 更新会话
        await self.db.chat_sessions.update_one(
            {"session_id": session.session_id},
            {"$set": session.model_dump()}
        )
        
        # 查找相关内容作为来源
        # sources = await self._find_relevant_sources(message)
        sources = []
        return ai_message, sources
        
    async def _find_relevant_sources(self, query: str) -> list:
        # 从guides和information集合中查找相关内容
        sources = []
        
        for collection in ["guides", "information"]:
            results = await self.db[collection].find({
                "$text": {"$search": query}
            }).limit(2).to_list(length=2)
            
            for doc in results:
                sources.append({
                    "type": collection,
                    "title": doc.get("title", doc.get("topic", "")),
                    "id": str(doc["_id"])
                })
                
        return sources 