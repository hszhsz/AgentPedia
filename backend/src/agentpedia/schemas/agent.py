"""
Agent相关的Pydantic模式
"""
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
import json

from pydantic import Field, validator

from agentpedia.models.agent import AgentStatus, AgentType, AgentVisibility, ModelProvider
from agentpedia.schemas.base import BaseSchema, IDSchema, TimestampSchema, FilterParams


class AgentBase(BaseSchema):
    """Agent基础模式"""

    name: str = Field(..., description="Agent名称", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Agent描述", max_length=1000)
    type: AgentType = Field(AgentType.CHATBOT, description="Agent类型")
    visibility: AgentVisibility = Field(AgentVisibility.PRIVATE, description="可见性")

    # 扩展信息
    website_url: Optional[str] = Field(None, description="官方网站链接", max_length=500)
    one_liner: Optional[str] = Field(None, description="一句话简介", max_length=200)
    tags: Optional[List[str]] = Field(None, description="标签列表")
    detailed_description: Optional[str] = Field(None, description="详细介绍", max_length=10000)
    pricing_plans: Optional[List[Dict]] = Field(None, description="价格方案列表")
    
    # 模型配置
    model_provider: ModelProvider = Field(..., description="模型提供商")
    model_name: str = Field(..., description="模型名称", max_length=100)
    model_version: Optional[str] = Field(None, description="模型版本", max_length=50)
    
    # 配置参数
    system_prompt: Optional[str] = Field(None, description="系统提示词", max_length=5000)
    temperature: float = Field(0.7, description="温度参数", ge=0.0, le=2.0)
    max_tokens: int = Field(2048, description="最大token数", ge=1, le=32000)
    top_p: float = Field(1.0, description="Top-p参数", ge=0.0, le=1.0)
    frequency_penalty: float = Field(0.0, description="频率惩罚", ge=-2.0, le=2.0)
    presence_penalty: float = Field(0.0, description="存在惩罚", ge=-2.0, le=2.0)
    
    # 功能配置
    enable_memory: bool = Field(True, description="是否启用记忆")
    enable_tools: bool = Field(False, description="是否启用工具")
    enable_web_search: bool = Field(False, description="是否启用网络搜索")
    enable_code_execution: bool = Field(False, description="是否启用代码执行")
    
    # 限制配置
    max_conversation_length: int = Field(50, description="最大对话长度", ge=1, le=1000)
    memory_window: int = Field(10, description="记忆窗口大小", ge=1, le=100)
    rate_limit_per_minute: int = Field(60, description="每分钟请求限制", ge=1, le=1000)
    rate_limit_per_hour: int = Field(1000, description="每小时请求限制", ge=1, le=10000)
    rate_limit_per_day: int = Field(10000, description="每日请求限制", ge=1, le=100000)
    
    @validator("name")
    def validate_name(cls, v):
        """验证Agent名称"""
        if not v.strip():
            raise ValueError("Agent名称不能为空")
        return v.strip()

    @validator("tags", pre=True)
    def parse_tags(cls, v):
        """解析tags字段（支持JSON字符串和列表）"""
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return v
        return v

    @validator("pricing_plans", pre=True)
    def parse_pricing_plans(cls, v):
        """解析pricing_plans字段（支持JSON字符串和列表）"""
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return v
        return v


class AgentCreate(AgentBase):
    """创建Agent模式"""
    pass


class AgentUpdate(BaseSchema):
    """更新Agent模式"""

    name: Optional[str] = Field(None, description="Agent名称", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Agent描述", max_length=1000)
    type: Optional[AgentType] = Field(None, description="Agent类型")
    visibility: Optional[AgentVisibility] = Field(None, description="可见性")

    # 扩展信息
    website_url: Optional[str] = Field(None, description="官方网站链接", max_length=500)
    one_liner: Optional[str] = Field(None, description="一句话简介", max_length=200)
    tags: Optional[List[str]] = Field(None, description="标签列表")
    detailed_description: Optional[str] = Field(None, description="详细介绍", max_length=10000)
    pricing_plans: Optional[List[Dict]] = Field(None, description="价格方案列表")

    # 模型配置
    model_provider: Optional[ModelProvider] = Field(None, description="模型提供商")
    model_name: Optional[str] = Field(None, description="模型名称", max_length=100)
    model_version: Optional[str] = Field(None, description="模型版本", max_length=50)

    # 配置参数
    system_prompt: Optional[str] = Field(None, description="系统提示词", max_length=5000)
    temperature: Optional[float] = Field(None, description="温度参数", ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, description="最大token数", ge=1, le=32000)
    top_p: Optional[float] = Field(None, description="Top-p参数", ge=0.0, le=1.0)
    frequency_penalty: Optional[float] = Field(None, description="频率惩罚", ge=-2.0, le=2.0)
    presence_penalty: Optional[float] = Field(None, description="存在惩罚", ge=-2.0, le=2.0)

    # 功能配置
    enable_memory: Optional[bool] = Field(None, description="是否启用记忆")
    enable_tools: Optional[bool] = Field(None, description="是否启用工具")
    enable_web_search: Optional[bool] = Field(None, description="是否启用网络搜索")
    enable_code_execution: Optional[bool] = Field(None, description="是否启用代码执行")

    # 限制配置
    max_conversation_length: Optional[int] = Field(None, description="最大对话长度", ge=1, le=1000)
    memory_window: Optional[int] = Field(None, description="记忆窗口大小", ge=1, le=100)
    rate_limit_per_minute: Optional[int] = Field(None, description="每分钟请求限制", ge=1, le=1000)
    rate_limit_per_hour: Optional[int] = Field(None, description="每小时请求限制", ge=1, le=10000)
    rate_limit_per_day: Optional[int] = Field(None, description="每日请求限制", ge=1, le=100000)

    # 工具配置
    tools: Optional[List[str]] = Field(None, description="工具列表")


class AgentResponse(AgentBase, IDSchema, TimestampSchema):
    """Agent响应模式"""

    status: AgentStatus = Field(..., description="Agent状态")
    owner_id: int = Field(..., description="所有者ID")

    # 统计信息
    usage_count: int = Field(0, description="使用次数")
    total_tokens_used: int = Field(0, description="总token使用量")
    average_response_time: float = Field(0.0, description="平均响应时间")
    success_rate: float = Field(100.0, description="成功率")

    # 社交数据
    average_rating: float = Field(0.0, description="平均评分")
    total_ratings: int = Field(0, description="总评价数")
    total_reviews: int = Field(0, description="总评论数")
    total_favorites: int = Field(0, description="总收藏数")
    monthly_active_users: int = Field(0, description="月活用户数")
    annual_active_users: int = Field(0, description="年活用户数")

    # 商业数据
    annual_recurring_revenue: float = Field(0.0, description="年度经常性收入")
    monthly_recurring_revenue: float = Field(0.0, description="月度经常性收入")
    growth_rate: float = Field(0.0, description="增长率")
    traffic_rank: int = Field(0, description="流量排名")

    # 时间信息
    published_at: Optional[datetime] = Field(None, description="发布时间")
    last_used_at: Optional[datetime] = Field(None, description="最后使用时间")


class AgentDetail(AgentResponse):
    """Agent详细信息模式"""

    # 包含工具信息
    tools: List["AgentToolResponse"] = Field([], description="工具列表")

    @validator("tags", pre=True)
    def parse_tags(cls, v):
        """解析tags字段（支持JSON字符串和列表）"""
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return v
        return v

    @validator("pricing_plans", pre=True)
    def parse_pricing_plans(cls, v):
        """解析pricing_plans字段（支持JSON字符串和列表）"""
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return v
        return v


class AgentToolBase(BaseSchema):
    """Agent工具基础模式"""
    
    tool_name: str = Field(..., description="工具名称", max_length=100)
    tool_config: Optional[Dict] = Field(None, description="工具配置")
    is_enabled: bool = Field(True, description="是否启用")


class AgentToolCreate(AgentToolBase):
    """创建Agent工具模式"""
    pass


class AgentToolUpdate(BaseSchema):
    """更新Agent工具模式"""
    
    tool_config: Optional[Dict] = Field(None, description="工具配置")
    is_enabled: Optional[bool] = Field(None, description="是否启用")


class AgentToolResponse(AgentToolBase, IDSchema, TimestampSchema):
    """Agent工具响应模式"""
    
    agent_id: int = Field(..., description="Agent ID")


class AgentChat(BaseSchema):
    """Agent聊天模式"""
    
    message: str = Field(..., description="用户消息", min_length=1, max_length=10000)
    conversation_id: Optional[int] = Field(None, description="对话ID")
    stream: bool = Field(False, description="是否流式响应")
    
    @validator("message")
    def validate_message(cls, v):
        """验证消息"""
        if not v.strip():
            raise ValueError("消息不能为空")
        return v.strip()


class AgentChatResponse(BaseSchema):
    """Agent聊天响应模式"""
    
    message: str = Field(..., description="Agent回复")
    conversation_id: int = Field(..., description="对话ID")
    message_id: int = Field(..., description="消息ID")
    tokens_used: int = Field(..., description="使用的token数")
    response_time: float = Field(..., description="响应时间")
    cost: float = Field(..., description="费用")


class AgentStats(BaseSchema):
    """Agent统计模式"""
    
    total_conversations: int = Field(..., description="总对话数")
    total_messages: int = Field(..., description="总消息数")
    total_tokens_used: int = Field(..., description="总token使用量")
    total_cost: float = Field(..., description="总费用")
    average_response_time: float = Field(..., description="平均响应时间")
    success_rate: float = Field(..., description="成功率")
    daily_usage: List[Dict] = Field(..., description="每日使用统计")
    hourly_usage: List[Dict] = Field(..., description="每小时使用统计")


class AgentClone(BaseSchema):
    """克隆Agent模式"""
    
    name: str = Field(..., description="新Agent名称", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="新Agent描述", max_length=1000)
    visibility: AgentVisibility = Field(AgentVisibility.PRIVATE, description="可见性")


class AgentExport(BaseSchema):
    """导出Agent模式"""
    
    include_conversations: bool = Field(False, description="是否包含对话记录")
    include_stats: bool = Field(False, description="是否包含统计信息")
    format: str = Field("json", description="导出格式", pattern="^(json|yaml)$")


class AgentFilterParams(FilterParams):
    """Agent过滤参数"""
    
    type: Optional[AgentType] = Field(None, description="Agent类型过滤")
    visibility: Optional[AgentVisibility] = Field(None, description="可见性过滤")
    owner_id: Optional[int] = Field(None, description="所有者ID过滤")


class AgentImport(BaseSchema):
    """导入Agent模式"""
    
    data: Dict = Field(..., description="Agent数据")
    overwrite: bool = Field(False, description="是否覆盖同名Agent")


# Review相关的schemas
class ReviewBase(BaseSchema):
    """评论基础模式"""

    rating: float = Field(..., description="评分", ge=1.0, le=5.0)
    title: Optional[str] = Field(None, description="评论标题", max_length=200)
    content: Optional[str] = Field(None, description="评论内容", max_length=2000)
    is_verified_purchase: bool = Field(False, description="是否为验证购买")
    is_featured: bool = Field(False, description="是否为精选评论")


class ReviewCreate(ReviewBase):
    """创建评论模式"""
    pass


class ReviewUpdate(BaseSchema):
    """更新评论模式"""

    rating: Optional[float] = Field(None, description="评分", ge=1.0, le=5.0)
    title: Optional[str] = Field(None, description="评论标题", max_length=200)
    content: Optional[str] = Field(None, description="评论内容", max_length=2000)
    is_verified_purchase: Optional[bool] = Field(None, description="是否为验证购买")
    is_featured: Optional[bool] = Field(None, description="是否为精选评论")


class ReviewResponse(ReviewBase, IDSchema, TimestampSchema):
    """评论响应模式"""

    agent_id: int = Field(..., description="Agent ID")
    user_id: int = Field(..., description="用户ID")
    helpful_count: int = Field(0, description="有用数")

    # 用户信息
    user_username: Optional[str] = Field(None, description="用户名")
    user_full_name: Optional[str] = Field(None, description="用户全名")


class AnalyticsData(BaseSchema):
    """分析数据模式"""

    date: str = Field(..., description="日期")
    period_type: str = Field(..., description="周期类型")
    new_users: int = Field(0, description="新用户数")
    active_users: int = Field(0, description="活跃用户数")
    returning_users: int = Field(0, description="回访用户数")
    total_conversations: int = Field(0, description="总对话数")
    total_messages: int = Field(0, description="总消息数")
    total_tokens_used: int = Field(0, description="总token使用量")
    revenue: float = Field(0.0, description="收入")
    cost: float = Field(0.0, description="成本")
    average_response_time: float = Field(0.0, description="平均响应时间")
    success_rate: float = Field(0.0, description="成功率")
    satisfaction_score: float = Field(0.0, description="满意度评分")
    page_views: int = Field(0, description="页面浏览量")
    unique_visitors: int = Field(0, description="独立访客数")
    bounce_rate: float = Field(0.0, description="跳出率")


class TrafficData(BaseSchema):
    """流量数据模式"""

    date: str = Field(..., description="日期")
    page_views: int = Field(0, description="页面浏览量")
    unique_visitors: int = Field(0, description="独立访客数")
    bounce_rate: float = Field(0.0, description="跳出率")


class RevenueData(BaseSchema):
    """收入数据模式"""

    date: str = Field(..., description="日期")
    revenue: float = Field(0.0, description="收入")
    cost: float = Field(0.0, description="成本")
    profit: float = Field(0.0, description="利润")


# 前向引用解决
AgentDetail.model_rebuild()