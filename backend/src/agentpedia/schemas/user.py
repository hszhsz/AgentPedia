"""
用户相关的Pydantic模式
"""
from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, validator

from agentpedia.models.user import UserRole, UserStatus
from agentpedia.schemas.base import BaseSchema, IDSchema, TimestampSchema


class UserBase(BaseSchema):
    """用户基础模式"""
    
    username: str = Field(..., description="用户名", min_length=3, max_length=50)
    email: EmailStr = Field(..., description="邮箱")
    full_name: Optional[str] = Field(None, description="全名", max_length=100)
    bio: Optional[str] = Field(None, description="个人简介", max_length=500)
    avatar_url: Optional[str] = Field(None, description="头像URL", max_length=500)
    timezone: str = Field("UTC", description="时区", max_length=50)
    language: str = Field("en", description="语言", max_length=10)
    theme: str = Field("light", description="主题", max_length=20)
    
    @validator("username")
    def validate_username(cls, v):
        """验证用户名"""
        if not v.isalnum() and "_" not in v and "-" not in v:
            raise ValueError("用户名只能包含字母、数字、下划线和连字符")
        return v.lower()
    
    @validator("theme")
    def validate_theme(cls, v):
        """验证主题"""
        if v not in ["light", "dark", "auto"]:
            raise ValueError("主题必须是 light、dark 或 auto")
        return v


class UserCreate(UserBase):
    """创建用户模式"""
    
    password: str = Field(..., description="密码", min_length=8, max_length=128)
    confirm_password: str = Field(..., description="确认密码")
    
    @validator("confirm_password")
    def passwords_match(cls, v, values):
        """验证密码确认"""
        if "password" in values and v != values["password"]:
            raise ValueError("密码确认不匹配")
        return v
    
    @validator("password")
    def validate_password(cls, v):
        """验证密码强度"""
        if len(v) < 8:
            raise ValueError("密码长度至少8位")
        
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError("密码必须包含大写字母、小写字母和数字")
        
        return v


class UserUpdate(BaseSchema):
    """更新用户模式"""
    
    full_name: Optional[str] = Field(None, description="全名", max_length=100)
    bio: Optional[str] = Field(None, description="个人简介", max_length=500)
    avatar_url: Optional[str] = Field(None, description="头像URL", max_length=500)
    timezone: Optional[str] = Field(None, description="时区", max_length=50)
    language: Optional[str] = Field(None, description="语言", max_length=10)
    theme: Optional[str] = Field(None, description="主题", max_length=20)
    
    @validator("theme")
    def validate_theme(cls, v):
        """验证主题"""
        if v is not None and v not in ["light", "dark", "auto"]:
            raise ValueError("主题必须是 light、dark 或 auto")
        return v


class UserResponse(UserBase, IDSchema, TimestampSchema):
    """用户响应模式"""
    
    role: UserRole = Field(..., description="用户角色")
    status: UserStatus = Field(..., description="用户状态")
    is_email_verified: bool = Field(..., description="邮箱是否已验证")
    email_verified_at: Optional[datetime] = Field(None, description="邮箱验证时间")
    last_login_at: Optional[datetime] = Field(None, description="最后登录时间")
    login_count: int = Field(..., description="登录次数")


class UserProfile(UserResponse):
    """用户详细资料模式"""
    
    last_login_ip: Optional[str] = Field(None, description="最后登录IP")
    password_changed_at: datetime = Field(..., description="密码修改时间")
    failed_login_attempts: int = Field(..., description="失败登录尝试次数")
    locked_until: Optional[datetime] = Field(None, description="锁定到期时间")


class UserLogin(BaseSchema):
    """用户登录模式"""
    
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")
    remember_me: bool = Field(False, description="记住我")


class UserRegister(UserCreate):
    """用户注册模式"""
    
    agree_terms: bool = Field(..., description="同意服务条款")
    
    @validator("agree_terms")
    def must_agree_terms(cls, v):
        """必须同意服务条款"""
        if not v:
            raise ValueError("必须同意服务条款")
        return v


class PasswordChange(BaseSchema):
    """修改密码模式"""
    
    current_password: str = Field(..., description="当前密码")
    new_password: str = Field(..., description="新密码", min_length=8, max_length=128)
    confirm_password: str = Field(..., description="确认新密码")
    
    @validator("confirm_password")
    def passwords_match(cls, v, values):
        """验证密码确认"""
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("密码确认不匹配")
        return v
    
    @validator("new_password")
    def validate_password(cls, v):
        """验证密码强度"""
        if len(v) < 8:
            raise ValueError("密码长度至少8位")
        
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError("密码必须包含大写字母、小写字母和数字")
        
        return v


class PasswordReset(BaseSchema):
    """重置密码模式"""
    
    email: EmailStr = Field(..., description="邮箱")


class PasswordResetConfirm(BaseSchema):
    """确认重置密码模式"""
    
    token: str = Field(..., description="重置令牌")
    new_password: str = Field(..., description="新密码", min_length=8, max_length=128)
    confirm_password: str = Field(..., description="确认新密码")
    
    @validator("confirm_password")
    def passwords_match(cls, v, values):
        """验证密码确认"""
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("密码确认不匹配")
        return v


class EmailVerification(BaseSchema):
    """邮箱验证模式"""
    
    token: str = Field(..., description="验证令牌")


class TokenResponse(BaseSchema):
    """令牌响应模式"""
    
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间（秒）")


class RefreshToken(BaseSchema):
    """刷新令牌模式"""
    
    refresh_token: str = Field(..., description="刷新令牌")


class UserStats(BaseSchema):
    """用户统计模式"""
    
    total_agents: int = Field(..., description="Agent总数")
    active_agents: int = Field(..., description="活跃Agent数")
    total_conversations: int = Field(..., description="对话总数")
    total_messages: int = Field(..., description="消息总数")
    total_tokens_used: int = Field(..., description="总token使用量")
    total_cost: float = Field(..., description="总费用")
    api_keys_count: int = Field(..., description="API密钥数量")