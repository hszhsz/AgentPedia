"""
MongoDB连接和管理模块
"""
from typing import Optional
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from agentpedia.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class MongoDBManager:
    """MongoDB连接管理器"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        
    async def init_mongodb(self) -> None:
        """初始化MongoDB连接"""
        try:
            # 构建MongoDB连接URI
            mongodb_uri = self._get_mongodb_uri()
            
            # 创建MongoDB客户端
            self.client = MongoClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,  # 5秒超时
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # 测试连接
            self.client.admin.command('ping')
            
            # 选择数据库
            self.db = self.client[settings.MONGODB_DATABASE]
            
            logger.info("MongoDB initialized successfully")
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"Error initializing MongoDB: {e}")
            raise
    
    def _get_mongodb_uri(self) -> str:
        """构建MongoDB连接URI"""
        if settings.MONGODB_URL:
            return settings.MONGODB_URL
        
        # 构建默认URI
        auth_part = ""
        if settings.MONGODB_USER and settings.MONGODB_PASSWORD:
            auth_part = f"{settings.MONGODB_USER}:{settings.MONGODB_PASSWORD}@"
        
        return f"mongodb://{auth_part}{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/{settings.MONGODB_DATABASE}"
    
    async def close_mongodb(self) -> None:
        """关闭MongoDB连接"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connections closed")
    
    def get_collection(self, collection_name: str):
        """获取集合"""
        if not self.db:
            raise RuntimeError("MongoDB not initialized")
        return self.db[collection_name]
    
    async def ping(self) -> bool:
        """检查MongoDB连接状态"""
        try:
            if self.client:
                self.client.admin.command('ping')
                return True
            return False
        except Exception:
            return False

# 创建全局MongoDB管理器实例
mongodb_manager = MongoDBManager()