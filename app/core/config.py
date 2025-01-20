from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

class Settings(BaseSettings):
    # MongoDB配置
    MONGODB_HOST: str = os.getenv("MONGODB_HOST", "localhost")
    MONGODB_PORT: int = int(os.getenv("MONGODB_PORT", 27017))
    MONGODB_USERNAME: str = os.getenv("MONGODB_USERNAME", "root")
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD", "mongopwd")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "newhk")
    
    @property
    def MONGODB_URL(self) -> str:
        """构建MongoDB连接URL"""
        return f"mongodb://{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}"

    # AI配置
    AI_API_KEY: str = os.getenv("AI_API_KEY", "your-api-key")
    AI_API_BASE_URL: str = os.getenv("AI_API_BASE_URL", "https://api.deepseek.com")
    AI_MODEL_NAME: str = os.getenv("AI_MODEL_NAME", "deepseek-chat")

    class Config:
        env_file = ".env"

settings = Settings() 