"""
对话服务类
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload

from agentpedia.models.conversation import Conversation, Message, ConversationStatus, MessageRole, MessageType
from agentpedia.models.agent import Agent
from agentpedia.models.user import User
from agentpedia.schemas.conversation import (
    ConversationCreate, ConversationUpdate, MessageCreate, MessageUpdate,
    ChatRequest, ChatResponse
)
from agentpedia.services.base import BaseService
from agentpedia.core.exceptions import NotFoundError, PermissionError, ValidationError


class ConversationService(BaseService[Conversation, ConversationCreate, ConversationUpdate]):
    """对话服务类"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Conversation, db)
    
    async def create_conversation(self, conversation_data: ConversationCreate, user_id: int) -> Conversation:
        """创建对话"""
        # 检查Agent是否存在
        agent = await self.db.get(Agent, conversation_data.agent_id)
        if not agent:
            raise NotFoundError("Agent不存在")
        
        # 检查用户是否存在
        user = await self.db.get(User, user_id)
        if not user:
            raise NotFoundError("用户不存在")
        
        # 创建对话
        conversation_dict = conversation_data.model_dump()
        conversation_dict['user_id'] = user_id
        conversation_dict['status'] = ConversationStatus.ACTIVE
        
        # 如果没有提供标题，生成默认标题
        if not conversation_dict.get('title'):
            conversation_dict['title'] = f"与 {agent.name} 的对话"
        
        conversation = Conversation(**conversation_dict)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        
        return conversation
    
    async def get_conversation_by_id(self, conversation_id: int, user_id: int) -> Conversation:
        """根据ID获取对话"""
        query = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        ).options(selectinload(Conversation.messages))
        
        result = await self.db.execute(query)
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise NotFoundError("对话不存在或无权访问")
        
        return conversation
    
    async def get_user_conversations(
        self,
        user_id: int,
        agent_id: Optional[int] = None,
        status: Optional[ConversationStatus] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Conversation]:
        """获取用户的对话列表"""
        query = select(Conversation).where(Conversation.user_id == user_id)
        
        # 过滤条件
        if agent_id:
            query = query.where(Conversation.agent_id == agent_id)
        
        if status:
            query = query.where(Conversation.status == status)
        
        if search:
            query = query.where(Conversation.title.ilike(f"%{search}%"))
        
        # 排序和分页
        query = query.order_by(desc(Conversation.updated_at)).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars())
    
    async def update_conversation(
        self, 
        conversation_id: int, 
        conversation_data: ConversationUpdate, 
        user_id: int
    ) -> Conversation:
        """更新对话"""
        conversation = await self.get_conversation_by_id(conversation_id, user_id)
        
        # 更新数据
        update_data = conversation_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conversation, field, value)
        
        await self.db.commit()
        await self.db.refresh(conversation)
        
        return conversation
    
    async def delete_conversation(self, conversation_id: int, user_id: int) -> bool:
        """删除对话"""
        conversation = await self.get_conversation_by_id(conversation_id, user_id)
        
        # 软删除对话和所有消息
        conversation.status = ConversationStatus.DELETED
        
        # 删除所有消息
        messages_query = select(Message).where(Message.conversation_id == conversation_id)
        messages_result = await self.db.execute(messages_query)
        messages = list(messages_result.scalars())
        
        for message in messages:
            message.is_deleted = True
        
        await self.db.commit()
        return True
    
    async def get_conversation_stats(self, user_id: int) -> Dict[str, Any]:
        """获取用户的对话统计信息"""
        # 总对话数
        total_query = select(func.count(Conversation.id)).where(
            and_(
                Conversation.user_id == user_id,
                Conversation.status != ConversationStatus.DELETED
            )
        )
        total_result = await self.db.execute(total_query)
        total_conversations = total_result.scalar() or 0
        
        # 活跃对话数
        active_query = select(func.count(Conversation.id)).where(
            and_(
                Conversation.user_id == user_id,
                Conversation.status == ConversationStatus.ACTIVE
            )
        )
        active_result = await self.db.execute(active_query)
        active_conversations = active_result.scalar() or 0
        
        # 总消息数
        messages_query = select(func.count(Message.id)).join(Conversation).where(
            and_(
                Conversation.user_id == user_id,
                Message.is_deleted == False
            )
        )
        messages_result = await self.db.execute(messages_query)
        total_messages = messages_result.scalar() or 0
        
        # 总token数和成本
        tokens_cost_query = select(
            func.sum(Conversation.total_tokens),
            func.sum(Conversation.total_cost)
        ).where(
            and_(
                Conversation.user_id == user_id,
                Conversation.status != ConversationStatus.DELETED
            )
        )
        tokens_cost_result = await self.db.execute(tokens_cost_query)
        tokens_cost = tokens_cost_result.first()
        
        total_tokens = tokens_cost[0] or 0
        total_cost = float(tokens_cost[1] or 0)
        
        # 平均每对话消息数
        avg_messages = total_messages / total_conversations if total_conversations > 0 else 0
        
        return {
            'total_conversations': total_conversations,
            'active_conversations': active_conversations,
            'total_messages': total_messages,
            'total_tokens': total_tokens,
            'total_cost': total_cost,
            'average_messages_per_conversation': round(avg_messages, 2)
        }


class MessageService(BaseService[Message, MessageCreate, MessageUpdate]):
    """消息服务类"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Message, db)
    
    async def create_message(self, message_data: MessageCreate, conversation_id: int) -> Message:
        """创建消息"""
        # 检查对话是否存在
        conversation = await self.db.get(Conversation, conversation_id)
        if not conversation:
            raise NotFoundError("对话不存在")
        
        # 创建消息
        message_dict = message_data.model_dump()
        message_dict['conversation_id'] = conversation_id
        
        message = Message(**message_dict)
        self.db.add(message)
        
        # 更新对话的消息计数
        conversation.message_count += 1
        
        await self.db.commit()
        await self.db.refresh(message)
        
        return message
    
    async def get_conversation_messages(
        self,
        conversation_id: int,
        user_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[Message]:
        """获取对话的消息列表"""
        # 检查对话权限
        conversation = await self.db.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise PermissionError("无权限访问此对话")
        
        query = select(Message).where(
            and_(
                Message.conversation_id == conversation_id,
                Message.is_deleted == False
            )
        ).order_by(Message.created_at).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars())
    
    async def update_message(self, message_id: int, message_data: MessageUpdate, user_id: int) -> Message:
        """更新消息"""
        # 获取消息和对话
        message = await self.db.get(Message, message_id)
        if not message:
            raise NotFoundError("消息不存在")
        
        conversation = await self.db.get(Conversation, message.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise PermissionError("无权限修改此消息")
        
        # 只允许修改用户自己的消息
        if message.role != MessageRole.USER:
            raise PermissionError("只能修改用户消息")
        
        # 更新数据
        update_data = message_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(message, field, value)
        
        await self.db.commit()
        await self.db.refresh(message)
        
        return message
    
    async def delete_message(self, message_id: int, user_id: int) -> bool:
        """删除消息"""
        # 获取消息和对话
        message = await self.db.get(Message, message_id)
        if not message:
            raise NotFoundError("消息不存在")
        
        conversation = await self.db.get(Conversation, message.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise PermissionError("无权限删除此消息")
        
        # 软删除消息
        message.is_deleted = True
        
        # 更新对话的消息计数
        conversation.message_count = max(0, conversation.message_count - 1)
        
        await self.db.commit()
        return True
    
    async def update_message_stats(
        self,
        message_id: int,
        tokens_used: int,
        cost: float,
        processing_time: float
    ) -> bool:
        """更新消息统计信息"""
        message = await self.db.get(Message, message_id)
        if not message:
            return False
        
        message.tokens_used = tokens_used
        message.cost = cost
        message.processing_time = processing_time
        
        # 更新对话统计
        conversation = await self.db.get(Conversation, message.conversation_id)
        if conversation:
            conversation.total_tokens += tokens_used
            conversation.total_cost += cost
        
        await self.db.commit()
        return True