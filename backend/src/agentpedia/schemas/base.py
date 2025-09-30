"""
基础Pydantic模式
"""
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

# 泛型类型变量
T = TypeVar("T")


class BaseSchema(BaseModel):
    """基础模式类"""
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
    )


class TimestampSchema(BaseSchema):
    """时间戳模式"""
    
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class IDSchema(BaseSchema):
    """ID模式"""
    
    id: int = Field(..., description="ID", gt=0)


class PaginationParams(BaseSchema):
    """分页参数"""
    
    page: int = Field(1, description="页码", ge=1)
    size: int = Field(20, description="每页大小", ge=1, le=100)
    
    @property
    def offset(self) -> int:
        """计算偏移量"""
        return (self.page - 1) * self.size


class SortParams(BaseSchema):
    """排序参数"""
    
    sort_by: str = Field("created_at", description="排序字段")
    sort_order: str = Field("desc", description="排序方向", pattern="^(asc|desc)$")


class FilterParams(BaseSchema):
    """过滤参数"""
    
    search: Optional[str] = Field(None, description="搜索关键词")
    status: Optional[str] = Field(None, description="状态过滤")
    created_after: Optional[datetime] = Field(None, description="创建时间起始")
    created_before: Optional[datetime] = Field(None, description="创建时间结束")


class PaginatedResponse(BaseSchema, Generic[T]):
    """分页响应"""
    
    items: List[T] = Field(..., description="数据列表")
    total: int = Field(..., description="总数量", ge=0)
    page: int = Field(..., description="当前页码", ge=1)
    size: int = Field(..., description="每页大小", ge=1)
    pages: int = Field(..., description="总页数", ge=0)
    has_next: bool = Field(..., description="是否有下一页")
    has_prev: bool = Field(..., description="是否有上一页")
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int
    ) -> "PaginatedResponse[T]":
        """创建分页响应"""
        pages = (total + size - 1) // size if total > 0 else 0
        
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )


class APIResponse(BaseSchema, Generic[T]):
    """API响应"""
    
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")
    error_code: Optional[str] = Field(None, description="错误代码")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="响应时间")
    
    @classmethod
    def success_response(
        cls,
        data: Optional[T] = None,
        message: str = "操作成功"
    ) -> "APIResponse[T]":
        """创建成功响应"""
        return cls(
            success=True,
            message=message,
            data=data
        )
    
    @classmethod
    def error_response(
        cls,
        message: str,
        error_code: Optional[str] = None,
        data: Optional[T] = None
    ) -> "APIResponse[T]":
        """创建错误响应"""
        return cls(
            success=False,
            message=message,
            error_code=error_code,
            data=data
        )


class HealthCheck(BaseSchema):
    """健康检查响应"""
    
    status: str = Field(..., description="服务状态")
    version: str = Field(..., description="版本号")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="检查时间")
    database: bool = Field(..., description="数据库连接状态")
    redis: bool = Field(..., description="Redis连接状态")
    uptime: float = Field(..., description="运行时间（秒）")


class ErrorDetail(BaseSchema):
    """错误详情"""
    
    field: str = Field(..., description="错误字段")
    message: str = Field(..., description="错误消息")
    code: Optional[str] = Field(None, description="错误代码")


class ValidationError(BaseSchema):
    """验证错误响应"""
    
    success: bool = Field(False, description="是否成功")
    message: str = Field("验证失败", description="错误消息")
    errors: List[ErrorDetail] = Field(..., description="错误详情列表")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="错误时间")