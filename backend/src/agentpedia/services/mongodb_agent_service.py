"""
基于MongoDB的Agent服务实现
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from agentpedia.core.mongodb import mongodb_manager
from agentpedia.models.mongodb_models import AgentModel, AgentStatus
from agentpedia.schemas.agent import AgentFilterParams
from agentpedia.schemas.base import PaginationParams
from agentpedia.services.validation_service import validation_service

logger = logging.getLogger(__name__)


class MongoDBAgentService:
    """MongoDB Agent服务"""
    
    def __init__(self):
        self.collection = None
    
    async def init_service(self):
        """初始化服务"""
        self.collection = mongodb_manager.get_collection("agents")
        # 创建索引
        await self._create_indexes()
    
    async def _create_indexes(self):
        """创建必要的索引"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        # 创建slug唯一索引
        self.collection.create_index("slug", unique=True)
        
        # 创建名称索引（支持文本搜索）
        self.collection.create_index([("name.zh", "text"), ("name.en", "text")])
        
        # 创建标签索引
        self.collection.create_index("tags")
        
        # 创建状态索引
        self.collection.create_index("status")
        
        # 创建技术栈索引
        self.collection.create_index("technical_stack.base_model")
        self.collection.create_index("technical_stack.frameworks")
        self.collection.create_index("technical_stack.programming_languages")
        
        # 创建时间索引
        self.collection.create_index("created_at")
        self.collection.create_index("updated_at")
        
        logger.info("MongoDB indexes created for agents collection")
    
    async def create_agent(self, agent_data: AgentModel) -> AgentModel:
        """创建Agent"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        # 设置时间戳
        now = datetime.utcnow()
        agent_data.created_at = now
        agent_data.updated_at = now
        
        # 插入数据
        result = self.collection.insert_one(agent_data.model_dump())
        agent_data.id = str(result.inserted_id)
        
        logger.info(f"Agent created with ID: {agent_data.id}")
        return agent_data
    
    async def get_agent_by_id(self, agent_id: str) -> Optional[AgentModel]:
        """根据ID获取Agent"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        doc = self.collection.find_one({"_id": agent_id})
        if doc:
            return AgentModel(**doc)
        return None
    
    async def get_agent_by_slug(self, slug: str) -> Optional[AgentModel]:
        """根据slug获取Agent"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        doc = self.collection.find_one({"slug": slug})
        if doc:
            return AgentModel(**doc)
        return None
    
    async def update_agent(self, agent_id: str, agent_data: AgentModel) -> Optional[AgentModel]:
        """更新Agent"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        # 设置更新时间
        agent_data.updated_at = datetime.utcnow()
        
        # 更新数据
        result = self.collection.update_one(
            {"_id": agent_id},
            {"$set": agent_data.model_dump(exclude={"id", "created_at"})}
        )
        
        if result.modified_count > 0:
            return await self.get_agent_by_id(agent_id)
        return None
    
    async def delete_agent(self, agent_id: str) -> bool:
        """删除Agent"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        result = self.collection.delete_one({"_id": agent_id})
        return result.deleted_count > 0
    
    async def get_agents_with_filters(
        self, 
        pagination: PaginationParams, 
        filters: AgentFilterParams
    ) -> tuple[List[AgentModel], int]:
        """根据过滤条件获取Agent列表"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        # 构建查询条件
        query = {}
        
        # 状态过滤
        if filters.status:
            query["status"] = filters.status
        
        # 标签过滤
        if filters.tags:
            query["tags"] = {"$in": filters.tags}
        
        # 技术栈过滤
        if filters.technical_stack:
            # 这里可以根据具体需求调整过滤逻辑
            query["$or"] = [
                {"technical_stack.base_model": {"$in": filters.technical_stack}},
                {"technical_stack.frameworks": {"$in": filters.technical_stack}},
                {"technical_stack.programming_languages": {"$in": filters.technical_stack}}
            ]
        
        # 搜索关键词过滤
        if filters.search:
            query["$text"] = {"$search": filters.search}
        
        # 计算总数
        total = self.collection.count_documents(query)
        
        # 构建排序和分页
        sort_field = "_id"
        sort_direction = 1
        
        if filters.sort_by == "created_at":
            sort_field = "created_at"
            sort_direction = -1 if filters.sort_order == "desc" else 1
        elif filters.sort_by == "updated_at":
            sort_field = "updated_at"
            sort_direction = -1 if filters.sort_order == "desc" else 1
        
        # 执行查询
        cursor = self.collection.find(query)
        cursor = cursor.sort(sort_field, sort_direction)
        cursor = cursor.skip((pagination.page - 1) * pagination.size).limit(pagination.size)
        
        # 转换结果
        agents = [AgentModel(**doc) for doc in cursor]
        
        return agents, total
    
    async def search_agents(
        self, 
        query: str, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[AgentModel]:
        """搜索Agent"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        # 构建搜索查询
        search_query = {"$text": {"$search": query}}
        
        # 添加额外过滤条件
        if filters:
            search_query.update(filters)
        
        # 执行搜索
        cursor = self.collection.find(search_query)
        # 按相关性排序
        cursor = cursor.sort([("$textScore", {"$meta": "textScore"})])
        # 限制结果数量
        cursor = cursor.limit(20)
        
        # 转换结果
        agents = [AgentModel(**doc) for doc in cursor]
        
        return agents
    
    async def get_related_agents(self, agent_id: str, limit: int = 5) -> List[AgentModel]:
        """获取相关Agent"""
        if not self.collection:
            raise RuntimeError("Service not initialized")
        
        # 获取当前Agent
        current_agent = await self.get_agent_by_id(agent_id)
        if not current_agent:
            return []
        
        # 构建相关性查询
        related_query = {
            "_id": {"$ne": agent_id},  # 排除自己
            "$or": []
        }
        
        # 基于标签的相关性
        if current_agent.tags:
            related_query["$or"].append({"tags": {"$in": current_agent.tags}})
        
        # 基于技术栈的相关性
        if current_agent.technical_stack:
            tech_stack_conditions = []
            if current_agent.technical_stack.base_model:
                tech_stack_conditions.append({
                    "technical_stack.base_model": {"$in": current_agent.technical_stack.base_model}
                })
            if current_agent.technical_stack.frameworks:
                tech_stack_conditions.append({
                    "technical_stack.frameworks": {"$in": current_agent.technical_stack.frameworks}
                })
            if current_agent.technical_stack.programming_languages:
                tech_stack_conditions.append({
                    "technical_stack.programming_languages": {"$in": current_agent.technical_stack.programming_languages}
                })
            if tech_stack_conditions:
                related_query["$or"].extend(tech_stack_conditions)
        
        # 如果没有相关性条件，返回空列表
        if not related_query["$or"]:
            return []
        
        # 执行查询
        cursor = self.collection.find(related_query)
        cursor = cursor.limit(limit)
        
        # 转换结果
        agents = [AgentModel(**doc) for doc in cursor]
        
        return agents

# 创建全局服务实例
mongodb_agent_service = MongoDBAgentService()