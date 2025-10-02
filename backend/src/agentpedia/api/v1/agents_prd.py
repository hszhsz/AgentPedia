"""
根据PRD文档要求的Agent API端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
import logging

from agentpedia.api.deps import get_current_active_user, get_optional_current_user
from agentpedia.core.logging import get_logger
from agentpedia.models.user import User
from agentpedia.schemas.agent_prd import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentFilterParams,
    AgentSearchQuery,
    AgentListResponse
)
from agentpedia.services.mongodb_agent_service import mongodb_agent_service

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=AgentListResponse)
async def list_agents(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页大小"),
    status: Optional[str] = Query(None, description="状态过滤"),
    tags: Optional[str] = Query(None, description="标签过滤，多个标签用逗号分隔"),
    technical_stack: Optional[str] = Query(None, description="技术栈过滤，多个技术用逗号分隔"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    sort_by: Optional[str] = Query("created_at", description="排序字段"),
    sort_order: Optional[str] = Query("desc", description="排序顺序"),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """获取Agent列表"""
    try:
        # 构建过滤参数
        filter_params = AgentFilterParams(
            status=status,
            tags=tags.split(",") if tags else None,
            technical_stack=technical_stack.split(",") if technical_stack else None,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # 构建分页参数
        from agentpedia.schemas.base import PaginationParams
        pagination_params = PaginationParams(page=page, size=size)
        
        # 获取Agent列表
        agents, total = await mongodb_agent_service.get_agents_with_filters(
            pagination_params, filter_params
        )
        
        # 转换为响应模型
        agent_responses = [AgentResponse(**agent.model_dump()) for agent in agents]
        
        return AgentListResponse(
            items=agent_responses,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    
    except Exception as e:
        logger.error(f"List agents failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取Agent列表失败"
        )


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """创建Agent"""
    try:
        # 创建Agent模型实例
        from agentpedia.models.mongodb_models import AgentModel
        agent_model = AgentModel(**agent_data.model_dump())
        agent_model.created_by = str(current_user.id)
        
        # 保存到数据库
        created_agent = await mongodb_agent_service.create_agent(agent_model)
        
        logger.info(f"Agent created successfully: {created_agent.id}")
        
        return AgentResponse(**created_agent.model_dump())
    
    except Exception as e:
        logger.error(f"Create agent failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建Agent失败"
        )


@router.get("/search", response_model=List[AgentResponse])
async def search_agents(
    query: str = Query(..., description="搜索关键词"),
    language: str = Query("zh", description="搜索语言"),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """搜索Agent"""
    try:
        # 构建搜索查询
        search_query = AgentSearchQuery(
            query=query,
            language=language
        )
        
        # 执行搜索
        agents = await mongodb_agent_service.search_agents(query)
        
        # 转换为响应模型
        agent_responses = [AgentResponse(**agent.model_dump()) for agent in agents]
        
        return agent_responses
    
    except Exception as e:
        logger.error(f"Search agents failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="搜索Agent失败"
        )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """获取Agent详情"""
    try:
        agent = await mongodb_agent_service.get_agent_by_id(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        return AgentResponse(**agent.model_dump())
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get agent failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取Agent详情失败"
        )


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """更新Agent"""
    try:
        # 检查Agent是否存在
        existing_agent = await mongodb_agent_service.get_agent_by_id(agent_id)
        if not existing_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        # 检查权限
        if existing_agent.created_by != str(current_user.id) and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限修改此Agent"
            )
        
        # 更新Agent
        from agentpedia.models.mongodb_models import AgentModel
        update_data = agent_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(existing_agent, key, value)
        
        updated_agent = await mongodb_agent_service.update_agent(agent_id, existing_agent)
        if not updated_agent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="更新Agent失败"
            )
        
        logger.info(f"Agent updated successfully: {agent_id}")
        
        return AgentResponse(**updated_agent.model_dump())
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update agent failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新Agent失败"
        )


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """删除Agent"""
    try:
        # 检查Agent是否存在
        existing_agent = await mongodb_agent_service.get_agent_by_id(agent_id)
        if not existing_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        # 检查权限
        if existing_agent.created_by != str(current_user.id) and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限删除此Agent"
            )
        
        # 删除Agent
        success = await mongodb_agent_service.delete_agent(agent_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="删除Agent失败"
            )
        
        logger.info(f"Agent deleted successfully: {agent_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete agent failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除Agent失败"
        )


@router.get("/{agent_id}/related", response_model=List[AgentResponse])
async def get_related_agents(
    agent_id: str,
    limit: int = Query(5, ge=1, le=20, description="相关Agent数量"),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """获取相关Agent"""
    try:
        # 获取相关Agent
        related_agents = await mongodb_agent_service.get_related_agents(agent_id, limit)
        
        # 转换为响应模型
        agent_responses = [AgentResponse(**agent.model_dump()) for agent in related_agents]
        
        return agent_responses
    
    except Exception as e:
        logger.error(f"Get related agents failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取相关Agent失败"
        )