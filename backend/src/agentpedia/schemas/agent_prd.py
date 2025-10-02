"""
根据PRD文档要求的Agent Schema定义
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MultilingualText(BaseModel):
    """多语言文本字段"""
    zh: Optional[str] = Field(None, description="中文文本")
    en: Optional[str] = Field(None, description="英文文本")


class MultilingualDescription(BaseModel):
    """多语言描述字段"""
    short: Optional[MultilingualText] = Field(None, description="简短描述")
    detailed: Optional[MultilingualText] = Field(None, description="详细描述")


class DevelopmentTeam(BaseModel):
    """开发团队信息"""
    name: MultilingualText = Field(..., description="团队名称")
    location: Optional[str] = Field(None, description="所在地")
    members: Optional[List[str]] = Field(None, description="核心成员")
    website: Optional[str] = Field(None, description="团队官网")
    description: Optional[MultilingualText] = Field(None, description="团队描述")


class TechnicalStack(BaseModel):
    """技术栈信息"""
    base_model: Optional[List[str]] = Field(None, description="基础模型")
    frameworks: Optional[List[str]] = Field(None, description="框架")
    programming_languages: Optional[List[str]] = Field(None, description="编程语言")
    deployment: Optional[List[str]] = Field(None, description="部署方式")
    description: Optional[MultilingualText] = Field(None, description="技术栈描述")


class FundingInfo(BaseModel):
    """融资信息"""
    round: str = Field(..., description="融资轮次")
    amount: str = Field(..., description="融资金额")
    investors: Optional[List[str]] = Field(None, description="投资方")
    date: str = Field(..., description="融资时间")


class BusinessInfo(BaseModel):
    """商业信息"""
    funding: Optional[List[FundingInfo]] = Field(None, description="融资情况")
    business_model: Optional[MultilingualText] = Field(None, description="商业模式")
    user_scale: Optional[Dict[str, Any]] = Field(None, description="用户规模")
    partners: Optional[List[str]] = Field(None, description="合作伙伴")


class AgentStatus(str):
    """Agent状态枚举"""
    CONCEPT = "concept"
    ALPHA = "alpha"
    BETA = "beta"
    RELEASED = "released"
    DISCONTINUED = "discontinued"


class AgentBase(BaseModel):
    """Agent基础模型"""
    name: MultilingualText = Field(..., description="项目名称")
    slug: str = Field(..., description="URL友好名称")
    logo_url: Optional[str] = Field(None, description="Logo地址")
    official_url: str = Field(..., description="官网地址")
    description: MultilingualDescription = Field(..., description="项目描述")
    development_team: Optional[DevelopmentTeam] = Field(None, description="开发团队")
    technical_stack: Optional[TechnicalStack] = Field(None, description="技术栈")
    features: Optional[List[MultilingualText]] = Field(None, description="功能特点")
    business_info: Optional[BusinessInfo] = Field(None, description="商业信息")
    status: AgentStatus = Field(..., description="项目状态")
    tags: Optional[List[str]] = Field(None, description="标签")
    related_agents: Optional[List[str]] = Field(None, description="相关Agent ID列表")
    metrics: Optional[Dict[str, Any]] = Field(None, description="统计数据")
    timeline: Optional[List[Dict[str, Any]]] = Field(None, description="时间线")


class AgentCreate(AgentBase):
    """创建Agent模型"""
    pass


class AgentUpdate(BaseModel):
    """更新Agent模型"""
    name: Optional[MultilingualText] = Field(None, description="项目名称")
    slug: Optional[str] = Field(None, description="URL友好名称")
    logo_url: Optional[str] = Field(None, description="Logo地址")
    official_url: Optional[str] = Field(None, description="官网地址")
    description: Optional[MultilingualDescription] = Field(None, description="项目描述")
    development_team: Optional[DevelopmentTeam] = Field(None, description="开发团队")
    technical_stack: Optional[TechnicalStack] = Field(None, description="技术栈")
    features: Optional[List[MultilingualText]] = Field(None, description="功能特点")
    business_info: Optional[BusinessInfo] = Field(None, description="商业信息")
    status: Optional[AgentStatus] = Field(None, description="项目状态")
    tags: Optional[List[str]] = Field(None, description="标签")
    related_agents: Optional[List[str]] = Field(None, description="相关Agent ID列表")
    metrics: Optional[Dict[str, Any]] = Field(None, description="统计数据")
    timeline: Optional[List[Dict[str, Any]]] = Field(None, description="时间线")


class AgentInDB(AgentBase):
    """数据库中的Agent模型"""
    id: str = Field(..., description="Agent ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    last_scraped_at: Optional[datetime] = Field(None, description="最后爬取时间")
    created_by: Optional[str] = Field(None, description="创建者")
    is_verified: bool = Field(default=False, description="是否经过验证")


class AgentResponse(AgentInDB):
    """Agent响应模型"""
    pass


class AgentSearchQuery(BaseModel):
    """Agent搜索查询模型"""
    query: str = Field(..., description="搜索关键词")
    language: Optional[str] = Field("zh", description="搜索语言")
    filters: Optional[Dict[str, Any]] = Field(None, description="额外过滤条件")


class AgentFilterParams(BaseModel):
    """Agent过滤参数"""
    status: Optional[AgentStatus] = Field(None, description="状态过滤")
    tags: Optional[List[str]] = Field(None, description="标签过滤")
    technical_stack: Optional[List[str]] = Field(None, description="技术栈过滤")
    search: Optional[str] = Field(None, description="搜索关键词")
    sort_by: Optional[str] = Field("created_at", description="排序字段")
    sort_order: Optional[str] = Field("desc", description="排序顺序")


class AgentListResponse(BaseModel):
    """Agent列表响应模型"""
    items: List[AgentResponse] = Field(..., description="Agent列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    size: int = Field(..., description="每页大小")
    pages: int = Field(..., description="总页数")