"""
收藏功能服务
"""
from typing import List, Optional
from datetime import datetime
import logging
from agentpedia.core.mongodb import mongodb_manager
from agentpedia.models.favorite import FavoriteCreate, FavoriteInDB, FavoriteResponse

logger = logging.getLogger(__name__)


class FavoriteService:
    """收藏服务"""
    
    def __init__(self):
        self.collection = None
    
    async def init_service(self):
        """初始化服务"""
        self.collection = mongodb_manager.get_collection("favorites")
        # 创建索引
        await self._create_indexes()
    
    async def _create_indexes(self):
        """创建必要的索引"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        # 创建用户ID索引
        self.collection.create_index("user_id")
        
        # 创建Agent ID索引
        self.collection.create_index("agent_id")
        
        # 创建用户ID和Agent ID的复合唯一索引
        self.collection.create_index(
            [("user_id", 1), ("agent_id", 1)], 
            unique=True
        )
        
        logger.info("MongoDB indexes created for favorites collection")
    
    async def add_favorite(self, favorite_data: FavoriteCreate) -> FavoriteResponse:
        """添加收藏"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        # 检查是否已收藏
        existing = self.collection.find_one({
            "user_id": favorite_data.user_id,
            "agent_id": favorite_data.agent_id
        })
        
        if existing:
            # 如果已收藏，返回现有记录
            return FavoriteResponse(**existing)
        
        # 创建新收藏记录
        favorite_model = FavoriteInDB(**favorite_data.model_dump())
        result = self.collection.insert_one(favorite_model.model_dump())
        favorite_model.id = str(result.inserted_id)
        
        logger.info(f"Favorite added: user_id={favorite_data.user_id}, agent_id={favorite_data.agent_id}")
        return FavoriteResponse(**favorite_model.model_dump())
    
    async def remove_favorite(self, user_id: str, agent_id: str) -> bool:
        """移除收藏"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        result = self.collection.delete_one({
            "user_id": user_id,
            "agent_id": agent_id
        })
        
        deleted = result.deleted_count > 0
        if deleted:
            logger.info(f"Favorite removed: user_id={user_id}, agent_id={agent_id}")
        
        return deleted
    
    async def get_user_favorites(self, user_id: str) -> List[FavoriteResponse]:
        """获取用户收藏列表"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        cursor = self.collection.find({"user_id": user_id})
        favorites = [FavoriteResponse(**doc) for doc in cursor]
        
        return favorites
    
    async def is_favorite(self, user_id: str, agent_id: str) -> bool:
        """检查是否已收藏"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        existing = self.collection.find_one({
            "user_id": user_id,
            "agent_id": agent_id
        })
        
        return existing is not None

# 创建全局服务实例
favorite_service = FavoriteService()