"""
Agent服务层
"""
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from agentpedia.models.agent import Agent, AgentStatus, AgentTool, AgentType, AgentVisibility
from agentpedia.schemas.agent import AgentCreate, AgentUpdate, AgentFilterParams
from agentpedia.schemas.base import PaginationParams
from agentpedia.services.base import BaseService


class AgentService(BaseService[Agent, AgentCreate, AgentUpdate]):
    """Agent服务"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Agent, db)
    
    async def create_agent(self, agent_data: AgentCreate, owner_id: int) -> Agent:
        """创建Agent"""
        # 检查名称是否已存在（同一用户下）
        existing_agent = await self.get_by_name_and_owner(agent_data.name, owner_id)
        if existing_agent:
            raise ValueError("Agent名称已存在")
        
        # 创建Agent
        agent = Agent(
            name=agent_data.name,
            description=agent_data.description,
            type=agent_data.type,
            visibility=agent_data.visibility,
            owner_id=owner_id,
            model_provider=agent_data.model_provider,
            model_name=agent_data.model_name,
            model_version=agent_data.model_version,
            system_prompt=agent_data.system_prompt,
            temperature=agent_data.temperature,
            max_tokens=agent_data.max_tokens,
            top_p=agent_data.top_p,
            frequency_penalty=agent_data.frequency_penalty,
            presence_penalty=agent_data.presence_penalty,
            enable_memory=agent_data.enable_memory,
            memory_window=agent_data.memory_window,
            enable_tools=agent_data.enable_tools,
            enable_web_search=agent_data.enable_web_search,
            enable_code_execution=agent_data.enable_code_execution,
            rate_limit_per_minute=agent_data.rate_limit_per_minute,
            rate_limit_per_hour=agent_data.rate_limit_per_hour,
            rate_limit_per_day=agent_data.rate_limit_per_day,
            status=AgentStatus.ACTIVE,
        )
        
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        
        # 添加工具关联
        if agent_data.tools:
            await self.add_tools_to_agent(agent.id, agent_data.tools)
        
        return agent
    
    async def get_by_name_and_owner(self, name: str, owner_id: int) -> Optional[Agent]:
        """根据名称和所有者获取Agent"""
        stmt = select(Agent).where(
            Agent.name == name,
            Agent.owner_id == owner_id,
            Agent.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_with_tools(self, agent_id: int) -> Optional[Agent]:
        """获取Agent及其工具"""
        stmt = (
            select(Agent)
            .options(selectinload(Agent.tools))
            .where(
                Agent.id == agent_id,
                Agent.deleted_at.is_(None)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_agent(self, agent_id: int, agent_data: AgentUpdate, user_id: int) -> Optional[Agent]:
        """更新Agent"""
        agent = await self.get(agent_id)
        if not agent:
            return None
        
        # 检查权限
        if agent.owner_id != user_id:
            raise PermissionError("无权限修改此Agent")
        
        # 更新字段
        update_data = agent_data.model_dump(exclude_unset=True, exclude={"tools"})
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        agent.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(agent)
        
        # 更新工具关联
        if agent_data.tools is not None:
            await self.update_agent_tools(agent_id, agent_data.tools)
        
        return agent
    
    async def delete_agent(self, agent_id: int, user_id: int) -> bool:
        """删除Agent"""
        agent = await self.get(agent_id)
        if not agent:
            return False
        
        # 检查权限
        if agent.owner_id != user_id:
            raise PermissionError("无权限删除此Agent")
        
        agent.soft_delete()
        await self.db.commit()
        return True
    
    async def clone_agent(self, agent_id: int, new_name: str, user_id: int) -> Optional[Agent]:
        """克隆Agent"""
        original_agent = await self.get_with_tools(agent_id)
        if not original_agent:
            return None
        
        # 检查可见性权限
        if original_agent.visibility == AgentVisibility.PRIVATE and original_agent.owner_id != user_id:
            raise PermissionError("无权限克隆此Agent")
        
        # 检查新名称是否已存在
        existing_agent = await self.get_by_name_and_owner(new_name, user_id)
        if existing_agent:
            raise ValueError("Agent名称已存在")
        
        # 创建克隆
        cloned_agent = Agent(
            name=new_name,
            description=f"克隆自 {original_agent.name}",
            type=original_agent.type,
            visibility=AgentVisibility.PRIVATE,  # 克隆的Agent默认为私有
            owner_id=user_id,
            model_provider=original_agent.model_provider,
            model_name=original_agent.model_name,
            model_version=original_agent.model_version,
            system_prompt=original_agent.system_prompt,
            temperature=original_agent.temperature,
            max_tokens=original_agent.max_tokens,
            top_p=original_agent.top_p,
            frequency_penalty=original_agent.frequency_penalty,
            presence_penalty=original_agent.presence_penalty,
            enable_memory=original_agent.enable_memory,
            memory_window=original_agent.memory_window,
            enable_tools=original_agent.enable_tools,
            enable_web_search=original_agent.enable_web_search,
            enable_code_execution=original_agent.enable_code_execution,
            rate_limit_per_minute=original_agent.rate_limit_per_minute,
            rate_limit_per_hour=original_agent.rate_limit_per_hour,
            rate_limit_per_day=original_agent.rate_limit_per_day,
            status=AgentStatus.ACTIVE,
        )
        
        self.db.add(cloned_agent)
        await self.db.commit()
        await self.db.refresh(cloned_agent)
        
        # 复制工具关联
        if original_agent.tools:
            tool_names = [tool.tool_name for tool in original_agent.tools]
            await self.add_tools_to_agent(cloned_agent.id, tool_names)
        
        return cloned_agent
    
    async def get_agents_with_filters(
        self,
        pagination: PaginationParams,
        filters: AgentFilterParams,
        user_id: Optional[int] = None
    ) -> Tuple[List[Agent], int]:
        """获取Agent列表（带过滤和分页）"""
        # 构建查询条件
        conditions = [Agent.deleted_at.is_(None)]
        
        # 可见性过滤
        if user_id:
            conditions.append(
                or_(
                    Agent.visibility == AgentVisibility.PUBLIC,
                    Agent.owner_id == user_id
                )
            )
        else:
            conditions.append(Agent.visibility == AgentVisibility.PUBLIC)
        
        if filters.search:
            search_term = f"%{filters.search}%"
            conditions.append(
                or_(
                    Agent.name.ilike(search_term),
                    Agent.description.ilike(search_term)
                )
            )
        
        if filters.type:
            conditions.append(Agent.type == filters.type)
        
        if filters.status:
            conditions.append(Agent.status == filters.status)
        
        if filters.owner_id:
            conditions.append(Agent.owner_id == filters.owner_id)
        
        if filters.created_after:
            conditions.append(Agent.created_at >= filters.created_after)
        
        if filters.created_before:
            conditions.append(Agent.created_at <= filters.created_before)
        
        # 查询总数
        try:
            count_stmt = select(func.count(Agent.id)).where(and_(*conditions))
            count_result = await self.db.execute(count_stmt)
            total = count_result.scalar() or 0
        except Exception as e:
            print(f"Error counting agents: {e}")
            total = 0
        
        # 查询数据
        try:
            stmt = (
                select(Agent)
                .options(selectinload(Agent.owner))
                .where(and_(*conditions))
                .offset(pagination.offset)
                .limit(pagination.size)
                .order_by(Agent.created_at.desc())
            )
            result = await self.db.execute(stmt)
            agents = list(result.scalars())
        except Exception as e:
            print(f"Error querying agents: {e}")
            agents = []

        return agents, total
    
    async def get_user_agents(
        self,
        user_id: int,
        pagination: PaginationParams,
        filters: AgentFilterParams
    ) -> Tuple[List[Agent], int]:
        """获取用户的Agent列表"""
        filters.owner_id = user_id
        return await self.get_agents_with_filters(pagination, filters, user_id)
    
    async def add_tools_to_agent(self, agent_id: int, tool_names: List[str]) -> bool:
        """为Agent添加工具"""
        # 删除现有工具关联
        await self.remove_all_tools_from_agent(agent_id)
        
        # 添加新的工具关联
        for tool_name in tool_names:
            agent_tool = AgentTool(
                agent_id=agent_id,
                tool_name=tool_name,
                is_enabled=True
            )
            self.db.add(agent_tool)
        
        await self.db.commit()
        return True
    
    async def update_agent_tools(self, agent_id: int, tool_names: List[str]) -> bool:
        """更新Agent的工具"""
        return await self.add_tools_to_agent(agent_id, tool_names)
    
    async def remove_all_tools_from_agent(self, agent_id: int) -> bool:
        """移除Agent的所有工具"""
        stmt = select(AgentTool).where(AgentTool.agent_id == agent_id)
        result = await self.db.execute(stmt)
        agent_tools = list(result.scalars())
        
        for agent_tool in agent_tools:
            await self.db.delete(agent_tool)
        
        await self.db.commit()
        return True
    
    async def toggle_tool(self, agent_id: int, tool_name: str, is_enabled: bool) -> bool:
        """切换工具启用状态"""
        stmt = select(AgentTool).where(
            AgentTool.agent_id == agent_id,
            AgentTool.tool_name == tool_name
        )
        result = await self.db.execute(stmt)
        agent_tool = result.scalar_one_or_none()
        
        if agent_tool:
            agent_tool.is_enabled = is_enabled
            await self.db.commit()
            return True
        
        return False
    
    async def update_usage_stats(
        self,
        agent_id: int,
        tokens_used: int,
        cost: float,
        processing_time: float
    ) -> bool:
        """更新使用统计"""
        agent = await self.get(agent_id)
        if not agent:
            return False
        
        agent.update_usage_stats(tokens_used, cost, processing_time)
        await self.db.commit()
        return True
    
    async def publish_agent(self, agent_id: int, user_id: int) -> bool:
        """发布Agent"""
        agent = await self.get(agent_id)
        if not agent:
            return False
        
        # 检查权限
        if agent.owner_id != user_id:
            raise PermissionError("无权限发布此Agent")
        
        agent.visibility = AgentVisibility.PUBLIC
        agent.published_at = datetime.utcnow()
        await self.db.commit()
        return True
    
    async def unpublish_agent(self, agent_id: int, user_id: int) -> bool:
        """取消发布Agent"""
        agent = await self.get(agent_id)
        if not agent:
            return False
        
        # 检查权限
        if agent.owner_id != user_id:
            raise PermissionError("无权限取消发布此Agent")
        
        agent.visibility = AgentVisibility.PRIVATE
        agent.published_at = None
        await self.db.commit()
        return True
    
    async def get_agent_stats(self, agent_id: int) -> Optional[dict]:
        """获取Agent统计信息"""
        agent = await self.get(agent_id)
        if not agent:
            return None
        
        return {
            "total_conversations": agent.total_conversations,
            "total_messages": agent.total_messages,
            "total_tokens_used": agent.total_tokens_used,
            "total_cost": float(agent.total_cost),
            "average_processing_time": float(agent.average_processing_time),
            "last_used_at": agent.last_used_at.isoformat() if agent.last_used_at else None,
        }
    
    async def export_agent(self, agent_id: int, user_id: int) -> Optional[dict]:
        """导出Agent配置"""
        agent = await self.get_with_tools(agent_id)
        if not agent:
            return None
        
        # 检查权限
        if agent.owner_id != user_id:
            raise PermissionError("无权限导出此Agent")
        
        return {
            "name": agent.name,
            "description": agent.description,
            "type": agent.type.value,
            "model_provider": agent.model_provider.value,
            "model_name": agent.model_name,
            "model_version": agent.model_version,
            "system_prompt": agent.system_prompt,
            "temperature": float(agent.temperature),
            "max_tokens": agent.max_tokens,
            "top_p": float(agent.top_p),
            "frequency_penalty": float(agent.frequency_penalty),
            "presence_penalty": float(agent.presence_penalty),
            "enable_memory": agent.enable_memory,
            "memory_window": agent.memory_window,
            "enable_tools": agent.enable_tools,
            "enable_web_search": agent.enable_web_search,
            "enable_code_execution": agent.enable_code_execution,
            "tools": [tool.tool_name for tool in agent.tools if tool.is_enabled],
            "rate_limits": {
                "per_minute": agent.rate_limit_per_minute,
                "per_hour": agent.rate_limit_per_hour,
                "per_day": agent.rate_limit_per_day,
            },
            "exported_at": datetime.utcnow().isoformat(),
            "version": "1.0",
        }