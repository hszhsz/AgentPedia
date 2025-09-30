"""
用户API路由
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from agentpedia.api.deps import (
    get_current_active_user,
    get_current_admin_user,
    get_user_service
)
from agentpedia.core.database import get_db
from agentpedia.core.logging import get_logger
from agentpedia.models.user import User, UserRole
from agentpedia.schemas.base import APIResponse, PaginatedResponse, PaginationParams, FilterParams
from agentpedia.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserProfile,
    UserLogin,
    UserRegister,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm,
    EmailVerification,
    TokenResponse,
    RefreshToken,
    UserStats
)
from agentpedia.services.user_service import UserService

router = APIRouter()
logger = get_logger(__name__)


@router.post("/register", response_model=APIResponse[UserResponse])
async def register_user(
    user_data: UserRegister,
    request: Request,
    user_service: UserService = Depends(get_user_service)
):
    """用户注册"""
    try:
        # 创建用户
        user = await user_service.create_user(UserCreate(**user_data.model_dump()))
        
        logger.info(
            "User registered successfully",
            user_id=user.id,
            username=user.username,
            ip_address=request.client.host
        )
        
        return APIResponse(
            success=True,
            data=UserResponse.model_validate(user),
            message="用户注册成功"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(
            "User registration failed",
            error=str(e),
            username=user_data.username,
            ip_address=request.client.host
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册失败"
        )


@router.post("/login", response_model=APIResponse[TokenResponse])
async def login_user(
    user_data: UserLogin,
    request: Request,
    user_service: UserService = Depends(get_user_service)
):
    """用户登录"""
    try:
        # 认证用户
        user = await user_service.authenticate_user(
            user_data.username,
            user_data.password,
            request.client.host
        )
        
        if not user:
            logger.warning(
                "Login attempt failed",
                username=user_data.username,
                ip_address=request.client.host
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        # 创建令牌
        tokens = await user_service.create_tokens(user)
        
        logger.info(
            "User logged in successfully",
            user_id=user.id,
            username=user.username,
            ip_address=request.client.host
        )
        
        return APIResponse(
            success=True,
            data=TokenResponse(**tokens),
            message="登录成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Login failed",
            error=str(e),
            username=user_data.username,
            ip_address=request.client.host
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录失败"
        )


@router.post("/refresh", response_model=APIResponse[TokenResponse])
async def refresh_token(
    token_data: RefreshToken,
    user_service: UserService = Depends(get_user_service)
):
    """刷新令牌"""
    # TODO: 实现刷新令牌逻辑
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能暂未实现"
    )


@router.get("/me", response_model=APIResponse[UserProfile])
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户信息"""
    return APIResponse(
        success=True,
        data=UserProfile.model_validate(current_user),
        message="获取用户信息成功"
    )


@router.put("/me", response_model=APIResponse[UserResponse])
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """更新当前用户信息"""
    try:
        updated_user = await user_service.update_user(current_user.id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        logger.info(
            "User profile updated",
            user_id=current_user.id,
            username=current_user.username
        )
        
        return APIResponse(
            success=True,
            data=UserResponse.model_validate(updated_user),
            message="用户信息更新成功"
        )
    
    except Exception as e:
        logger.error(
            "User profile update failed",
            error=str(e),
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新失败"
        )


@router.post("/change-password", response_model=APIResponse[dict])
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """修改密码"""
    try:
        success = await user_service.change_password(
            current_user.id,
            password_data.current_password,
            password_data.new_password
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前密码错误"
            )
        
        logger.info(
            "Password changed successfully",
            user_id=current_user.id,
            username=current_user.username
        )
        
        return APIResponse(
            success=True,
            data={},
            message="密码修改成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Password change failed",
            error=str(e),
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码修改失败"
        )


@router.post("/reset-password", response_model=APIResponse[dict])
async def reset_password_request(
    reset_data: PasswordReset,
    user_service: UserService = Depends(get_user_service)
):
    """请求重置密码"""
    # TODO: 实现密码重置逻辑（发送邮件等）
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能暂未实现"
    )


@router.post("/reset-password/confirm", response_model=APIResponse[dict])
async def reset_password_confirm(
    reset_data: PasswordResetConfirm,
    user_service: UserService = Depends(get_user_service)
):
    """确认重置密码"""
    # TODO: 实现密码重置确认逻辑
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能暂未实现"
    )


@router.post("/verify-email", response_model=APIResponse[dict])
async def verify_email(
    verification_data: EmailVerification,
    user_service: UserService = Depends(get_user_service)
):
    """验证邮箱"""
    # TODO: 实现邮箱验证逻辑
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能暂未实现"
    )


@router.get("/stats", response_model=APIResponse[UserStats])
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """获取用户统计信息"""
    try:
        stats = await user_service.get_user_stats(current_user.id)
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return APIResponse(
            success=True,
            data=UserStats(**stats),
            message="获取统计信息成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Get user stats failed",
            error=str(e),
            user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取统计信息失败"
        )


# 管理员接口
@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    pagination: PaginationParams = Depends(),
    filters: FilterParams = Depends(),
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """获取用户列表（管理员）"""
    try:
        users, total = await user_service.get_users_with_filters(pagination, filters)
        
        return PaginatedResponse(
            items=[UserResponse.model_validate(user) for user in users],
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=(total + pagination.size - 1) // pagination.size
        )
    
    except Exception as e:
        logger.error(
            "List users failed",
            error=str(e),
            admin_user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户列表失败"
        )


@router.get("/{user_id}", response_model=APIResponse[UserProfile])
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """获取指定用户信息（管理员）"""
    try:
        user = await user_service.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return APIResponse(
            success=True,
            data=UserProfile.model_validate(user),
            message="获取用户信息成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Get user failed",
            error=str(e),
            user_id=user_id,
            admin_user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )


@router.put("/{user_id}", response_model=APIResponse[UserResponse])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """更新指定用户信息（管理员）"""
    try:
        updated_user = await user_service.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        logger.info(
            "User updated by admin",
            user_id=user_id,
            admin_user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data=UserResponse.model_validate(updated_user),
            message="用户信息更新成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Update user failed",
            error=str(e),
            user_id=user_id,
            admin_user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户信息失败"
        )


@router.post("/{user_id}/activate", response_model=APIResponse[dict])
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """激活用户（管理员）"""
    try:
        success = await user_service.activate_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        logger.info(
            "User activated by admin",
            user_id=user_id,
            admin_user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data={},
            message="用户激活成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Activate user failed",
            error=str(e),
            user_id=user_id,
            admin_user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="激活用户失败"
        )


@router.post("/{user_id}/deactivate", response_model=APIResponse[dict])
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """停用用户（管理员）"""
    try:
        success = await user_service.deactivate_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        logger.info(
            "User deactivated by admin",
            user_id=user_id,
            admin_user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data={},
            message="用户停用成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Deactivate user failed",
            error=str(e),
            user_id=user_id,
            admin_user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="停用用户失败"
        )


@router.delete("/{user_id}", response_model=APIResponse[dict])
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """删除用户（管理员）"""
    try:
        deleted_user = await user_service.delete(user_id)
        if not deleted_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        logger.info(
            "User deleted by admin",
            user_id=user_id,
            admin_user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            data={},
            message="用户删除成功"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Delete user failed",
            error=str(e),
            user_id=user_id,
            admin_user_id=current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除用户失败"
        )