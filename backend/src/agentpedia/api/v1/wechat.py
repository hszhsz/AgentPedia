"""
微信登录相关API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from agentpedia.services.wechat_auth_service import wechat_auth_service
from agentpedia.schemas.wechat import (
    WechatLoginResponse,
    LoginStatusResponse,
    WechatCallbackRequest,
    TokenResponse,
    RefreshTokenRequest
)
from agentpedia.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/qrcode", response_model=WechatLoginResponse)
async def generate_login_qr_code():
    """生成微信登录二维码"""
    try:
        response = await wechat_auth_service.generate_login_qr_code()
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"生成登录二维码失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="生成登录二维码失败"
        )


@router.get("/status/{session_id}", response_model=LoginStatusResponse)
async def check_login_status(session_id: str):
    """检查登录状态"""
    try:
        status_data = await wechat_auth_service.check_login_status(session_id)
        return LoginStatusResponse(**status_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"检查登录状态失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="检查登录状态失败"
        )


@router.post("/callback", response_model=TokenResponse)
async def handle_wechat_callback(request: WechatCallbackRequest):
    """处理微信登录回调"""
    try:
        response = await wechat_auth_service.handle_callback(request)
        return TokenResponse(
            access_token=response["access_token"],
            refresh_token=response["refresh_token"],
            expires_in=1800
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理微信回调失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="处理微信回调失败"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(request: RefreshTokenRequest):
    """刷新访问令牌"""
    try:
        response = await wechat_auth_service.refresh_access_token(request.refresh_token)
        return TokenResponse(**response)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"刷新访问令牌失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="刷新访问令牌失败"
        )


@router.post("/logout")
async def logout():
    """用户登出"""
    try:
        # 这里应该从请求中获取用户信息
        # 暂时返回成功响应
        return {"message": "登出成功"}
    except Exception as e:
        logger.error(f"用户登出失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="用户登出失败"
        )