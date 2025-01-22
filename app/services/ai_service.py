from openai import OpenAI
from app.core.config import settings
from app.models.ai_chat import ChatSession, Message, MessageRole, ChatHistoryResponse, \
                                SessionInfo, ChatSessionResponse, SessionStatus, ChatResponse
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional, Tuple

class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.AI_API_KEY,
            base_url=settings.AI_API_BASE_URL
        )
        self.db_client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.db_client[settings.DATABASE_NAME]
        # 为chat_sessions创建一个TTL索引(24小时之后自动删除)
        # self.db.chat_sessions.create_index([("created_at", 1)], expireAfterSeconds=86400)
        # 为chat_requests创建一个TTL索引(36小时之后自动删除)
        self.db.chat_requests.create_index([("created_at", 1)], expireAfterSeconds=129600)

    async def get_session(self, session_id: str, device_id: str) -> ChatSession:
        session_data = await self.db.chat_sessions.find_one({"session_id": session_id, "device_id": device_id})
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
                    # content="你是一个帮助新来香港的人解答问题的AI助手。请提供准确、有帮助的信息。"
                    content="""
                        # 角色
                        你是一个香港万事通，对香港的工作、生活、学习等方面了如指掌。可以用清晰、准确且易懂的语言回答用户关于香港的各种问题。

                        ## 技能
                        ### 技能 1: 解答香港工作问题
                        1. 当用户询问香港相关问题时，先确定问题的具体方向，如政务、交通、住房等。
                        2. 结合利用搜索和知识库查找相关信息，确保回答准确且有依据。
                        3. 详细解答问题，并提供一些实用的建议或资源。
                        4. 最后基于提问和回答，给出三个用户可能想继续追问的问题，问题要简短具体，与上下文紧密相关，不需要序号或其他格式。
                        5. 回答中的内容来源和继续采用 JSON 格式，内容包括回答、建议、小贴士和资源。
                        ===回复示例===
                        - 👨‍💼 回答：<对问题的详细解答>
                        - 💡 建议：<相关建议>
                        - 💡 小贴士：<小贴士内容>

                        {{JSON_START}}
                        {
                            "source": [{"<内容来源1>":"<内容来源1链接>"}, {"<内容来源2>":"<内容来源2链接>"}, {"<内容来源3>":"<内容来源3链接>"}],
                            "next_questions": ["<推荐追问问题1>", "<推荐追问问题2>", "<推荐追问问题3>"]
                        }
                        {{JSON_START}}
                        ===示例结束===

                        ## 限制:
                        - 只回答与香港的工作、生活、学习有关的问题，拒绝回答无关话题。
                        - 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。
                        - 确保信息来源准确可靠，可通过搜索工具进行核实。
                    """
                )
            ],
            session_info=SessionInfo(
                name="",
                first_message="",
                total_tokens=0,
                prompt_tokens=0,
                completion_tokens=0,
                model=settings.AI_MODEL_NAME
            ),
            created_at=datetime.now(),
            updated_at=datetime.now()
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

    # 基于提示词的格式要求和AI回答结果, 提取出JSON数据(以{{JSON_START}}和{{JSON_END}}为分隔符)
        
    async def chat(self, session: ChatSession, message: str) -> ChatResponse:
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
            # 需要将created_at和sources从Message中排除
            messages=[m.model_dump(exclude={"created_at", "sources"}) for m in session.messages],
            stream=False
        )

        # 获取AI回复
        ai_message = response.choices[0].message.content
        
        # 添加AI回复
        session.messages.append(Message(role=MessageRole.ASSISTANT, content=ai_message))
        session.updated_at = datetime.now()

        # 更新会话信息
        session.session_info.total_tokens = response.usage.total_tokens
        session.session_info.prompt_tokens = response.usage.prompt_tokens
        session.session_info.completion_tokens = response.usage.completion_tokens
        session.session_info.request_count += 1
        # 如果会话是新的, 则设置first_message
        if not session.session_info.first_message: 
            session.session_info.first_message = message

        # 更新会话
        await self.db.chat_sessions.update_one(
            {"session_id": session.session_id},
            {"$set": session.model_dump()}
        )
        
        # 查找相关内容作为来源
        # sources = await self._find_relevant_sources(message)
        sources = []
        return ChatResponse(
            session_id=session.session_id,
            message=ai_message,
            sources=sources,
            suggestions=[]
        )
        
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

    async def get_chat_history(
        self,
        device_id: str,
        session_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[ChatHistoryResponse, int]:
        """
        从chat_sessions集合中获取历史对话记录
        
        Args:
            device_id: 设备ID
            session_id: 会话ID，只返回特定会话的记录
            limit: 返回记录数量限制
            offset: 分页偏移量
        
        Returns:
            List[ChatHistoryResponse]: 历史对话记录列表
        """
        query = {"device_id": device_id}
        query["session_id"] = session_id
            
        # 从chat_sessions集合中获取会话
        session = await self.db.chat_sessions.find_one(
            query
        )
        
        # 跳过系统消息
        messages = [msg for msg in session["messages"] if msg["role"] != "system"]
        session["messages"] = messages
        
        # 将created_at和updated_at转换为int
        session["created_at"] = int(session["created_at"].timestamp())
        session["updated_at"] = int(session["updated_at"].timestamp())
        
        # 将messages中的created_at转换为int
        for msg in session["messages"]:
            if msg.get("created_at"):
                msg["created_at"] = int(msg["created_at"].timestamp())

        # 手动实现分页
        total = len(session["messages"])
        start_idx = offset
        end_idx = offset + limit
        session["messages"] = session["messages"][start_idx:end_idx]
        
        chat_history = ChatHistoryResponse(**session)
        return chat_history, total

    async def get_sessions(
        self,
        device_id: str,
        limit: int = 20,
        offset: int = 0,
        status: Optional[SessionStatus] = None,
        is_brief: bool = False
    ) -> Tuple[List[ChatSessionResponse], int]:
        """获取设备的会话列表"""
        query = {"device_id": device_id}
        if status:
            query["status"] = status
        projection = {"messages": 0} if is_brief else {}
        
        # 更新过期状态
        await self.update_expired_sessions(device_id)
        
        total = await self.db.chat_sessions.count_documents(query)
        
        cursor = self.db.chat_sessions.find(query, projection)\
            .sort("updated_at", -1)\
            .skip(offset)\
            .limit(limit)
        
        sessions = []
        async for doc in cursor:
            # 将created_at和updated_at转换为int
            doc["created_at"] = int(doc["created_at"].timestamp())
            doc["updated_at"] = int(doc["updated_at"].timestamp())
            # 不需要_id
            doc.pop("_id", None)
            if is_brief:
                doc["messages"] = []
            sessions.append(ChatSessionResponse(**doc))
        
        return sessions, total

    async def get_session_info(self, session_id: str, device_id: str) -> Optional[ChatSessionResponse]:
        """获取会话详情"""
        # 更新过期状态
        await self.update_expired_sessions(device_id)
        
        doc = await self.db.chat_sessions.find_one({
            "session_id": session_id,
            "device_id": device_id
        })
        
        if doc:
            # 将created_at和updated_at转换为int
            doc["created_at"] = int(doc["created_at"].timestamp())
            doc["updated_at"] = int(doc["updated_at"].timestamp())
            # 不需要_id
            doc.pop("_id", None)
            return ChatSessionResponse(**doc)
        return None

    async def update_expired_sessions(self, device_id: str):
        """更新过期的会话状态"""
        expire_time = datetime.now() - timedelta(days=1)
        await self.db.chat_sessions.update_many(
            {
                "device_id": device_id,
                "status": SessionStatus.ACTIVE,
                "created_at": {"$lt": expire_time}
            },
            {
                "$set": {
                    "updated_at": datetime.now(),
                    "session_info": {
                        "status": SessionStatus.EXPIRED,
                        "stop_reason": "session expired"
                    },
                }
            }
        )
