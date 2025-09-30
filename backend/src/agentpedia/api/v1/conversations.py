"""
对话相关的API路由
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from agentpedia.api.deps import get_current_user, get_db
from agentpedia.models.conversation import ConversationStatus
from agentpedia.models.user import User
from agentpedia.schemas.base import APIResponse, PaginatedResponse
from agentpedia.schemas.conversation import (
    ConversationCreate, ConversationUpdate, ConversationResponse, ConversationDetail,
    MessageCreate, MessageUpdate, MessageResponse, ConversationStats,
    ChatRequest, ChatResponse
)
from agentpedia.services.conversation_service import ConversationService, MessageService
from agentpedia.core.exceptions import NotFoundError, PermissionError

router = APIRouter()


@router.post("/", response_model=APIResponse[ConversationResponse])
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建新对话"""
    try:
        service = ConversationService(db)
        conversation = await service.create_conversation(conversation_data, current_user.id)
        return APIResponse(
            success=True,
            data=ConversationResponse.model_validate(conversation),
            message="对话创建成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=APIResponse[List[ConversationResponse]])
async def get_conversations(
    agent_id: Optional[int] = Query(None, description="Agent ID"),
    status: Optional[ConversationStatus] = Query(None, description="对话状态"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的对话列表"""
    try:
        service = ConversationService(db)
        conversations = await service.get_user_conversations(
            user_id=current_user.id,
            agent_id=agent_id,
            status=status,
            search=search,
            skip=skip,
            limit=limit
        )
        return APIResponse(
            success=True,
            data=[ConversationResponse.model_validate(conv) for conv in conversations],
            message="获取对话列表成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/stats", response_model=APIResponse[ConversationStats])
async def get_conversation_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取对话统计信息"""
    try:
        service = ConversationService(db)
        stats = await service.get_conversation_stats(current_user.id)
        return APIResponse(
            success=True,
            data=ConversationStats(**stats),
            message="获取统计信息成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{conversation_id}", response_model=APIResponse[ConversationDetail])
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取对话详情"""
    try:
        service = ConversationService(db)
        conversation = await service.get_conversation_by_id(conversation_id, current_user.id)
        
        # 转换为详情响应
        conversation_detail = ConversationDetail.model_validate(conversation)
        conversation_detail.messages = [
            MessageResponse.model_validate(msg) for msg in conversation.messages
            if not msg.is_deleted
        ]
        
        return APIResponse(
            success=True,
            data=conversation_detail,
            message="获取对话详情成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{conversation_id}", response_model=APIResponse[ConversationResponse])
async def update_conversation(
    conversation_id: int,
    conversation_data: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新对话"""
    try:
        service = ConversationService(db)
        conversation = await service.update_conversation(
            conversation_id, conversation_data, current_user.id
        )
        return APIResponse(
            success=True,
            data=ConversationResponse.model_validate(conversation),
            message="对话更新成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{conversation_id}", response_model=APIResponse[bool])
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除对话"""
    try:
        service = ConversationService(db)
        result = await service.delete_conversation(conversation_id, current_user.id)
        return APIResponse(
            success=True,
            data=result,
            message="对话删除成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# 消息相关路由
@router.post("/{conversation_id}/messages", response_model=APIResponse[MessageResponse])
async def create_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建消息"""
    try:
        service = MessageService(db)
        message = await service.create_message(message_data, conversation_id)
        return APIResponse(
            success=True,
            data=MessageResponse.model_validate(message),
            message="消息创建成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{conversation_id}/messages", response_model=APIResponse[List[MessageResponse]])
async def get_messages(
    conversation_id: int,
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(50, ge=1, le=100, description="限制数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取对话的消息列表"""
    try:
        service = MessageService(db)
        messages = await service.get_conversation_messages(
            conversation_id, current_user.id, skip, limit
        )
        return APIResponse(
            success=True,
            data=[MessageResponse.model_validate(msg) for msg in messages],
            message="获取消息列表成功"
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/messages/{message_id}", response_model=APIResponse[MessageResponse])
async def update_message(
    message_id: int,
    message_data: MessageUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新消息"""
    try:
        service = MessageService(db)
        message = await service.update_message(message_id, message_data, current_user.id)
        return APIResponse(
            success=True,
            data=MessageResponse.model_validate(message),
            message="消息更新成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/messages/{message_id}", response_model=APIResponse[bool])
async def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除消息"""
    try:
        service = MessageService(db)
        result = await service.delete_message(message_id, current_user.id)
        return APIResponse(
            success=True,
            data=result,
            message="消息删除成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{conversation_id}/chat", response_model=APIResponse[ChatResponse])
async def chat_with_agent(
    conversation_id: int,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """与Agent聊天"""
    # TODO: 实现实际的聊天逻辑
    # 这里需要集成AI模型服务
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="聊天功能尚未实现"
    )