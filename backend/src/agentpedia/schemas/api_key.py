"""
API密钥相关的Pydantic schemas
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from agentpedia.models.api_key import APIKeyStatus, APIKeyScope
from agentpedia.schemas.base import BaseSchema, TimestampSchema, IDSchema


class APIKeyBase(BaseSchema):
    """API密钥基础schema"""
    name: str = Field(..., min_length=1, max_length=100, description="密钥名称")
    description: Optional[str] = Field(None, max_length=500, description="密钥描述")
    scopes: List[APIKeyScope] = Field(default=[APIKeyScope.READ], description="权限范围")
    rate_limit_per_minute: int = Field(default=60, ge=1, le=10000, description="每分钟请求限制")
    rate_limit_per_hour: int = Field(default=1000, ge=1, le=100000, description="每小时请求限制")
    rate_limit_per_day: int = Field(default=10000, ge=1, le=1000000, description="每天请求限制")
    expires_at: Optional[datetime] = Field(None, description="过期时间")

    @validator('rate_limit_per_hour')
    def validate_hour_limit(cls, v, values):
        """验证小时限制"""
        if 'rate_limit_per_minute' in values:
            min_limit = values['rate_limit_per_minute']
            if v < min_limit:
                raise ValueError('每小时限制不能小于每分钟限制')
        return v

    @validator('rate_limit_per_day')
    def validate_day_limit(cls, v, values):
        """验证天限制"""
        if 'rate_limit_per_hour' in values:
            hour_limit = values['rate_limit_per_hour']
            if v < hour_limit:
                raise ValueError('每天限制不能小于每小时限制')
        return v


class APIKeyCreate(APIKeyBase):
    """创建API密钥schema"""
    pass


class APIKeyUpdate(BaseSchema):
    """更新API密钥schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="密钥名称")
    description: Optional[str] = Field(None, max_length=500, description="密钥描述")
    scopes: Optional[List[APIKeyScope]] = Field(None, description="权限范围")
    rate_limit_per_minute: Optional[int] = Field(None, ge=1, le=10000, description="每分钟请求限制")
    rate_limit_per_hour: Optional[int] = Field(None, ge=1, le=100000, description="每小时请求限制")
    rate_limit_per_day: Optional[int] = Field(None, ge=1, le=1000000, description="每天请求限制")
    expires_at: Optional[datetime] = Field(None, description="过期时间")


class APIKeyResponse(APIKeyBase, IDSchema, TimestampSchema):
    """API密钥响应schema"""
    user_id: int = Field(..., description="用户ID")
    prefix: str = Field(..., description="密钥前缀")
    status: APIKeyStatus = Field(..., description="密钥状态")
    usage_count: int = Field(default=0, description="使用次数")
    last_used_at: Optional[datetime] = Field(None, description="最后使用时间")
    last_used_ip: Optional[str] = Field(None, description="最后使用IP")

    class Config:
        from_attributes = True


class APIKeyCreateResponse(APIKeyResponse):
    """创建API密钥响应schema（包含完整密钥）"""
    key: str = Field(..., description="完整API密钥（仅在创建时返回）")


class APIKeyStats(BaseSchema):
    """API密钥统计schema"""
    total_keys: int = Field(..., description="总密钥数")
    active_keys: int = Field(..., description="活跃密钥数")
    expired_keys: int = Field(..., description="过期密钥数")
    revoked_keys: int = Field(..., description="已撤销密钥数")
    total_usage: int = Field(..., description="总使用次数")


class APIKeyUsage(BaseSchema):
    """API密钥使用情况schema"""
    key_id: int = Field(..., description="密钥ID")
    key_name: str = Field(..., description="密钥名称")
    usage_count: int = Field(..., description="使用次数")
    last_used_at: Optional[datetime] = Field(None, description="最后使用时间")
    rate_limit_remaining: dict = Field(..., description="剩余请求限制")


class RateLimitInfo(BaseSchema):
    """速率限制信息schema"""
    limit_per_minute: int = Field(..., description="每分钟限制")
    limit_per_hour: int = Field(..., description="每小时限制")
    limit_per_day: int = Field(..., description="每天限制")
    remaining_per_minute: int = Field(..., description="每分钟剩余")
    remaining_per_hour: int = Field(..., description="每小时剩余")
    remaining_per_day: int = Field(..., description="每天剩余")
    reset_time_minute: datetime = Field(..., description="分钟重置时间")
    reset_time_hour: datetime = Field(..., description="小时重置时间")
    reset_time_day: datetime = Field(..., description="天重置时间")