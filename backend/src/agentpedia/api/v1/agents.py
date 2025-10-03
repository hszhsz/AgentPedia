"""
Agent API路由
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from agentpedia.api.deps import (
    get_current_active_user,
    get_optional_current_user,
    get_agent_service
)
from agentpedia.core.logging import get_logger
from agentpedia.models.user import User
from agentpedia.schemas.base import APIResponse, PaginatedResponse, PaginationParams
from agentpedia.schemas.agent import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentDetail,
    AgentStats,
    AgentClone,
    AgentExport,
    AgentImport,
    AgentChat,
    AgentChatResponse,
    AgentFilterParams
)
from agentpedia.services.agent_service import AgentService

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=PaginatedResponse[AgentResponse])
async def list_agents(
    pagination: PaginationParams = Depends(),
    filters: AgentFilterParams = Depends(),
    current_user: Optional[User] = Depends(get_optional_current_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """获取Agent列表"""
    try:
        user_id = current_user.id if current_user else None
        agents, total = await agent_service.get_agents_with_filters(
            pagination, filters, user_id
        )

        try:
            response_data = []
            for agent in agents:
                try:
                    response_data.append(AgentResponse.model_validate(agent))
                except Exception as e:
                    logger.error(f"Error validating agent {agent.id}: {e}")
                    continue

            return PaginatedResponse.create(
                items=response_data,
                total=total,
                page=pagination.page,
                size=pagination.size
            )
        except Exception as e:
            logger.error(f"Error creating paginated response: {e}")
            # Return a simple response
            return {
                "items": [],
                "total": 0,
                "page": pagination.page,
                "size": pagination.size,
                "pages": 0,
                "has_next": False,
                "has_prev": False
            }
    
    except Exception as e:
        logger.error(
            "List agents failed",
            error=str(e),
            user_id=current_user.id if current_user else None
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取Agent列表失败"
        )


@router.post("/", response_model=APIResponse[AgentResponse])
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """创建Agent"""
    try:
        agent = await agent_service.create_agent(agent_data, current_user.id)
        
        logger.info(
            "Agent created successfully",
            agent_id=agent.id,
            agent_name=agent.name,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data=AgentResponse.model_validate(agent),
            message="Agent创建成功"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(
            "Agent creation failed",
            error=str(e),
            agent_name=agent_data.name,
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent创建失败"
        )


@router.get("/my", response_model=PaginatedResponse[AgentResponse])
async def list_my_agents(
    pagination: PaginationParams = Depends(),
    filters: AgentFilterParams = Depends(),
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """获取我的Agent列表"""
    try:
        agents, total = await agent_service.get_user_agents(
            current_user.id, pagination, filters
        )
        
        return PaginatedResponse.create(
            items=[AgentResponse.model_validate(agent) for agent in agents],
            total=total,
            page=pagination.page,
            size=pagination.size
        )
    
    except Exception as e:
        logger.error(
            "List my agents failed",
            error=str(e),
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取我的Agent列表失败"
        )


@router.get("/{agent_id}", response_model=APIResponse[AgentDetail])
async def get_agent(
    agent_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """获取Agent详情"""
    try:
        agent = await agent_service.get_with_tools(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        # 检查访问权限
        if agent.visibility.value == "private" and (
            not current_user or agent.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此Agent"
            )
        
        return APIResponse(
            success=True,
            data=AgentDetail.model_validate(agent),
            message="获取Agent详情成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Get agent failed",
            error=str(e),
            agent_id=agent_id,
            user_id=current_user.id if current_user else None
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取Agent详情失败"
        )


@router.put("/{agent_id}", response_model=APIResponse[AgentResponse])
async def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """更新Agent"""
    try:
        agent = await agent_service.update_agent(agent_id, agent_data, current_user.id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        logger.info(
            "Agent updated successfully",
            agent_id=agent_id,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data=AgentResponse.model_validate(agent),
            message="Agent更新成功"
        )
    
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限修改此Agent"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Agent update failed",
            error=str(e),
            agent_id=agent_id,
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent更新失败"
        )


@router.delete("/{agent_id}", response_model=APIResponse[dict])
async def delete_agent(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """删除Agent"""
    try:
        success = await agent_service.delete_agent(agent_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        logger.info(
            "Agent deleted successfully",
            agent_id=agent_id,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data={},
            message="Agent删除成功"
        )
    
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限删除此Agent"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Agent deletion failed",
            error=str(e),
            agent_id=agent_id,
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent删除失败"
        )


@router.post("/{agent_id}/clone", response_model=APIResponse[AgentResponse])
async def clone_agent(
    agent_id: int,
    clone_data: AgentClone,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """克隆Agent"""
    try:
        agent = await agent_service.clone_agent(
            agent_id, clone_data.name, current_user.id
        )
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        logger.info(
            "Agent cloned successfully",
            original_agent_id=agent_id,
            new_agent_id=agent.id,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data=AgentResponse.model_validate(agent),
            message="Agent克隆成功"
        )
    
    except (PermissionError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Agent cloning failed",
            error=str(e),
            agent_id=agent_id,
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent克隆失败"
        )


@router.post("/{agent_id}/publish", response_model=APIResponse[dict])
async def publish_agent(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """发布Agent"""
    try:
        success = await agent_service.publish_agent(agent_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        logger.info(
            "Agent published successfully",
            agent_id=agent_id,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data={},
            message="Agent发布成功"
        )
    
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限发布此Agent"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Agent publishing failed",
            error=str(e),
            agent_id=agent_id,
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent发布失败"
        )


@router.post("/{agent_id}/unpublish", response_model=APIResponse[dict])
async def unpublish_agent(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """取消发布Agent"""
    try:
        success = await agent_service.unpublish_agent(agent_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        logger.info(
            "Agent unpublished successfully",
            agent_id=agent_id,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data={},
            message="Agent取消发布成功"
        )
    
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限取消发布此Agent"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Agent unpublishing failed",
            error=str(e),
            agent_id=agent_id,
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent取消发布失败"
        )


@router.get("/{agent_id}/stats", response_model=APIResponse[AgentStats])
async def get_agent_stats(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """获取Agent统计信息"""
    try:
        # 检查权限
        agent = await agent_service.get(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        if agent.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限查看此Agent统计信息"
            )
        
        stats = await agent_service.get_agent_stats(agent_id)
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        return APIResponse(
            success=True,
            data=AgentStats(**stats),
            message="获取Agent统计信息成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Get agent stats failed",
            error=str(e),
            agent_id=agent_id,
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取Agent统计信息失败"
        )


@router.get("/{agent_id}/export", response_model=APIResponse[AgentExport])
async def export_agent(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """导出Agent配置"""
    try:
        export_data = await agent_service.export_agent(agent_id, current_user.id)
        if not export_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        logger.info(
            "Agent exported successfully",
            agent_id=agent_id,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data=AgentExport(**export_data),
            message="Agent导出成功"
        )
    
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限导出此Agent"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Agent export failed",
            error=str(e),
            agent_id=agent_id,
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent导出失败"
        )


@router.post("/import", response_model=APIResponse[AgentResponse])
async def import_agent(
    import_data: AgentImport,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """导入Agent配置"""
    try:
        # 将导入数据转换为创建数据
        agent_create_data = AgentCreate(
            name=import_data.name,
            description=import_data.description,
            type=import_data.type,
            visibility="private",  # 导入的Agent默认为私有
            model_provider=import_data.model_provider,
            model_name=import_data.model_name,
            model_version=import_data.model_version,
            system_prompt=import_data.system_prompt,
            temperature=import_data.temperature,
            max_tokens=import_data.max_tokens,
            top_p=import_data.top_p,
            frequency_penalty=import_data.frequency_penalty,
            presence_penalty=import_data.presence_penalty,
            enable_memory=import_data.enable_memory,
            memory_window=import_data.memory_window,
            enable_tools=import_data.enable_tools,
            enable_web_search=import_data.enable_web_search,
            enable_code_execution=import_data.enable_code_execution,
            tools=import_data.tools,
            rate_limit_per_minute=import_data.rate_limits.per_minute,
            rate_limit_per_hour=import_data.rate_limits.per_hour,
            rate_limit_per_day=import_data.rate_limits.per_day,
        )
        
        agent = await agent_service.create_agent(agent_create_data, current_user.id)
        
        logger.info(
            "Agent imported successfully",
            agent_id=agent.id,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data=AgentResponse.model_validate(agent),
            message="Agent导入成功"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(
            "Agent import failed",
            error=str(e),
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent导入失败"
        )


@router.post("/{agent_id}/chat", response_model=APIResponse[AgentChatResponse])
async def chat_with_agent(
    agent_id: int,
    chat_data: AgentChat,
    current_user: User = Depends(get_current_active_user),
    agent_service: AgentService = Depends(get_agent_service)
):
    """与Agent对话"""
    try:
        # 检查Agent是否存在和可访问
        agent = await agent_service.get(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent不存在"
            )
        
        # 检查访问权限
        if agent.visibility.value == "private" and agent.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此Agent"
            )
        
        # TODO: 实现实际的对话逻辑
        # 这里应该调用对话服务来处理消息
        
        # 暂时返回模拟响应
        response = AgentChatResponse(
            message="这是一个模拟响应，实际的对话功能尚未实现。",
            tokens_used=50,
            cost=0.001,
            processing_time=1.5
        )
        
        logger.info(
            "Chat with agent",
            agent_id=agent_id,
            user_id=current_user.id,
            message_length=len(chat_data.message)
        )
        
        return APIResponse(
            success=True,
            data=response,
            message="对话成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Chat with agent failed",
            error=str(e),
            agent_id=agent_id,
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="对话失败"
        )