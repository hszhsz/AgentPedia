"""
微信登录相关的数据模式
"""
from typing import Optional
from pydantic import BaseModel, Field


class WechatLoginResponse(BaseModel):
    """微信登录响应"""
    session_id: str = Field(..., description="会话ID")
    qr_code: str = Field(..., description="二维码图片的base64编码")
    login_url: str = Field(..., description="登录URL")
    expires_in: int = Field(..., description="过期时间（秒）")


class WechatCallbackRequest(BaseModel):
    """微信回调请求"""
    code: str = Field(..., description="授权码")
    state: str = Field(..., description="状态参数")


class WechatUserInfo(BaseModel):
    """微信用户信息"""
    openid: str = Field(..., description="用户openid")
    nickname: Optional[str] = Field(None, description="昵称")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    unionid: Optional[str] = Field(None, description="用户unionid")
    sex: Optional[int] = Field(None, description="性别")
    language: Optional[str] = Field(None, description="语言")
    city: Optional[str] = Field(None, description="城市")
    province: Optional[str] = Field(None, description="省份")
    country: Optional[str] = Field(None, description="国家")


class LoginStatusResponse(BaseModel):
    """登录状态响应"""
    session_id: str = Field(..., description="会话ID")
    status: str = Field(..., description="登录状态: pending, success, failed")
    user_info: Optional[WechatUserInfo] = Field(None, description="用户信息")
    expires_at: Optional[str] = Field(None, description="过期时间")


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间（秒）")


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refresh_token: str = Field(..., description="刷新令牌")