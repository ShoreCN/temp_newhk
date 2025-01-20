from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB配置
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_USERNAME: str = "root"
    MONGODB_PASSWORD: str = "mongopwd"
    DATABASE_NAME: str = "newhk"
    
    @property
    def MONGODB_URL(self) -> str:
        """构建MongoDB连接URL"""
        return f"mongodb://{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}"

    # AI配置
    AI_API_KEY: str = "your-api-key"
    AI_API_BASE_URL: str = "https://api.deepseek.com"
    AI_MODEL_NAME: str = "deepseek-chat"

    class Config:
        env_file = ".env"

settings = Settings() 