"""
对话相关的Pydantic schemas
"""
from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, validator

from agentpedia.models.conversation import ConversationStatus, MessageRole, MessageType
from agentpedia.schemas.base import BaseSchema, TimestampSchema, IDSchema


class MessageBase(BaseSchema):
    """消息基础schema"""
    role: MessageRole = Field(..., description="消息角色")
    content: str = Field(..., min_length=1, max_length=50000, description="消息内容")
    type: MessageType = Field(default=MessageType.TEXT, description="消息类型")
    attachments: Optional[List[str]] = Field(default=None, description="附件列表")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(default=None, description="工具调用")
    tool_results: Optional[List[Dict[str, Any]]] = Field(default=None, description="工具结果")


class MessageCreate(MessageBase):
    """创建消息schema"""
    conversation_id: Optional[int] = Field(default=None, description="对话ID")


class MessageUpdate(BaseSchema):
    """更新消息schema"""
    content: Optional[str] = Field(None, min_length=1, max_length=50000, description="消息内容")
    is_edited: Optional[bool] = Field(default=True, description="是否已编辑")


class MessageResponse(MessageBase, IDSchema, TimestampSchema):
    """消息响应schema"""
    conversation_id: int = Field(..., description="对话ID")
    tokens_used: int = Field(default=0, description="使用的token数量")
    cost: float = Field(default=0.0, description="成本")
    processing_time: float = Field(default=0.0, description="处理时间（秒）")
    is_edited: bool = Field(default=False, description="是否已编辑")
    is_deleted: bool = Field(default=False, description="是否已删除")

    class Config:
        from_attributes = True


class ConversationBase(BaseSchema):
    """对话基础schema"""
    title: Optional[str] = Field(None, max_length=200, description="对话标题")
    agent_id: int = Field(..., description="Agent ID")


class ConversationCreate(ConversationBase):
    """创建对话schema"""
    pass


class ConversationUpdate(BaseSchema):
    """更新对话schema"""
    title: Optional[str] = Field(None, max_length=200, description="对话标题")
    status: Optional[ConversationStatus] = Field(None, description="对话状态")


class ConversationResponse(ConversationBase, IDSchema, TimestampSchema):
    """对话响应schema"""
    user_id: int = Field(..., description="用户ID")
    status: ConversationStatus = Field(..., description="对话状态")
    message_count: int = Field(default=0, description="消息数量")
    total_tokens: int = Field(default=0, description="总token数量")
    total_cost: float = Field(default=0.0, description="总成本")

    class Config:
        from_attributes = True


class ConversationDetail(ConversationResponse):
    """对话详情schema"""
    messages: List[MessageResponse] = Field(default=[], description="消息列表")


class ConversationStats(BaseSchema):
    """对话统计schema"""
    total_conversations: int = Field(..., description="总对话数")
    active_conversations: int = Field(..., description="活跃对话数")
    total_messages: int = Field(..., description="总消息数")
    total_tokens: int = Field(..., description="总token数")
    total_cost: float = Field(..., description="总成本")
    average_messages_per_conversation: float = Field(..., description="平均每对话消息数")


class ChatRequest(BaseSchema):
    """聊天请求schema"""
    message: str = Field(..., min_length=1, max_length=50000, description="消息内容")
    conversation_id: Optional[int] = Field(None, description="对话ID，如果为空则创建新对话")
    stream: bool = Field(default=False, description="是否流式响应")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="温度参数")
    max_tokens: Optional[int] = Field(None, ge=1, le=8192, description="最大token数")


class ChatResponse(BaseSchema):
    """聊天响应schema"""
    conversation_id: int = Field(..., description="对话ID")
    message_id: int = Field(..., description="消息ID")
    content: str = Field(..., description="响应内容")
    tokens_used: int = Field(..., description="使用的token数量")
    cost: float = Field(..., description="成本")
    processing_time: float = Field(..., description="处理时间（秒）")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(default=None, description="工具调用")


class ChatStreamChunk(BaseSchema):
    """聊天流式响应块schema"""
    conversation_id: int = Field(..., description="对话ID")
    message_id: Optional[int] = Field(None, description="消息ID")
    content: str = Field(..., description="内容块")
    is_final: bool = Field(default=False, description="是否为最后一块")
    tokens_used: Optional[int] = Field(None, description="使用的token数量")
    cost: Optional[float] = Field(None, description="成本")
    processing_time: Optional[float] = Field(None, description="处理时间（秒）")