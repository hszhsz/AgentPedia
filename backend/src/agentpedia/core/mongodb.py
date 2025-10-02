"""
MongoDB 连接管理器
"""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from agentpedia.core.config import get_settings

logger = logging.getLogger(__name__)


class MongoDBManager:
    """MongoDB连接管理器"""

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self._initialized = False

    async def init_mongodb(self):
        """初始化MongoDB连接"""
        if self._initialized:
            return

        settings = get_settings()
        mongodb_url = settings.get_mongodb_url()

        try:
            # 创建客户端
            self.client = AsyncIOMotorClient(
                mongodb_url,
                maxPoolSize=10,
                minPoolSize=1,
                maxIdleTimeMS=30000,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                retryWrites=True,
                w="majority"
            )

            # 测试连接
            await self.client.admin.command('ping')

            # 获取数据库
            self.database = self.client[settings.MONGODB_DATABASE]

            self._initialized = True
            logger.info(f"MongoDB connected: {settings.MONGODB_DATABASE}")

        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def close_mongodb(self):
        """关闭MongoDB连接"""
        if self.client:
            self.client.close()
            self._initialized = False
            logger.info("MongoDB connection closed")

    def get_database(self) -> AsyncIOMotorDatabase:
        """获取数据库实例"""
        if not self._initialized:
            raise RuntimeError("MongoDB not initialized")
        return self.database

    def get_collection(self, collection_name: str):
        """获取集合实例"""
        if not self._initialized:
            raise RuntimeError("MongoDB not initialized")
        return self.database[collection_name]

    async def create_indexes(self):
        """创建必要的索引"""
        if not self._initialized:
            raise RuntimeError("MongoDB not initialized")

        # agents 集合索引
        agents_collection = self.database.agents

        # 基础索引
        await agents_collection.create_index("slug", unique=True)
        await agents_collection.create_index("status")
        await agents_collection.create_index("created_at")
        await agents_collection.create_index("updated_at")
        await agents_collection.create_index("tags")

        # 文本搜索索引
        await agents_collection.create_index([
            ("name.zh", "text"),
            ("name.en", "text"),
            ("description.short.zh", "text"),
            ("description.short.en", "text"),
            ("description.detailed.zh", "text"),
            ("description.detailed.en", "text"),
            ("features.zh", "text"),
            ("features.en", "text")
        ])

        # 技术栈索引
        await agents_collection.create_index("technical_stack.base_model")
        await agents_collection.create_index("technical_stack.frameworks")
        await agents_collection.create_index("technical_stack.programming_languages")

        logger.info("MongoDB indexes created")

    async def drop_indexes(self):
        """删除所有索引（除了默认的_id索引）"""
        if not self._initialized:
            raise RuntimeError("MongoDB not initialized")

        agents_collection = self.database.agents

        # 获取所有索引
        indexes = await agents_collection.list_indexes()

        # 删除所有非 _id 索引
        for index in indexes:
            if index["name"] != "_id_":
                await agents_collection.drop_index(index["name"])

        logger.info("MongoDB indexes dropped")


# 创建全局 MongoDB 管理器实例
mongodb_manager = MongoDBManager()