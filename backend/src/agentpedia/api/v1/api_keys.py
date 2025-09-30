"""
API密钥相关的API路由
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from agentpedia.api.deps import get_current_user, get_db
from agentpedia.models.api_key import APIKeyStatus
from agentpedia.models.user import User
from agentpedia.schemas.base import APIResponse
from agentpedia.schemas.api_key import (
    APIKeyCreate, APIKeyUpdate, APIKeyResponse, APIKeyCreateResponse,
    APIKeyStats, APIKeyUsage, RateLimitInfo
)
from agentpedia.services.api_key_service import APIKeyService
from agentpedia.core.exceptions import NotFoundError, PermissionError, ValidationError

router = APIRouter()


@router.post("/", response_model=APIResponse[APIKeyCreateResponse])
async def create_api_key(
    key_data: APIKeyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建API密钥"""
    try:
        service = APIKeyService(db)
        api_key, key = await service.create_api_key(key_data, current_user.id)
        
        # 创建响应，包含完整密钥
        response_data = APIKeyCreateResponse.model_validate(api_key)
        response_data.key = key
        
        return APIResponse(
            success=True,
            data=response_data,
            message="API密钥创建成功，请妥善保存密钥，此密钥不会再次显示"
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=APIResponse[List[APIKeyResponse]])
async def get_api_keys(
    status_filter: Optional[APIKeyStatus] = Query(None, alias="status", description="密钥状态"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的API密钥列表"""
    try:
        service = APIKeyService(db)
        api_keys = await service.get_user_api_keys(
            user_id=current_user.id,
            status=status_filter,
            skip=skip,
            limit=limit
        )
        return APIResponse(
            success=True,
            data=[APIKeyResponse.model_validate(key) for key in api_keys],
            message="获取API密钥列表成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/stats", response_model=APIResponse[APIKeyStats])
async def get_api_key_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取API密钥统计信息"""
    try:
        service = APIKeyService(db)
        stats = await service.get_api_key_stats(current_user.id)
        return APIResponse(
            success=True,
            data=APIKeyStats(**stats),
            message="获取统计信息成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{key_id}", response_model=APIResponse[APIKeyResponse])
async def get_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取API密钥详情"""
    try:
        service = APIKeyService(db)
        api_key = await service.get_api_key_by_id(key_id, current_user.id)
        return APIResponse(
            success=True,
            data=APIKeyResponse.model_validate(api_key),
            message="获取API密钥详情成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{key_id}", response_model=APIResponse[APIKeyResponse])
async def update_api_key(
    key_id: int,
    key_data: APIKeyUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新API密钥"""
    try:
        service = APIKeyService(db)
        api_key = await service.update_api_key(key_id, key_data, current_user.id)
        return APIResponse(
            success=True,
            data=APIKeyResponse.model_validate(api_key),
            message="API密钥更新成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{key_id}/activate", response_model=APIResponse[APIKeyResponse])
async def activate_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """激活API密钥"""
    try:
        service = APIKeyService(db)
        api_key = await service.activate_api_key(key_id, current_user.id)
        return APIResponse(
            success=True,
            data=APIKeyResponse.model_validate(api_key),
            message="API密钥激活成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{key_id}/deactivate", response_model=APIResponse[APIKeyResponse])
async def deactivate_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """停用API密钥"""
    try:
        service = APIKeyService(db)
        api_key = await service.deactivate_api_key(key_id, current_user.id)
        return APIResponse(
            success=True,
            data=APIKeyResponse.model_validate(api_key),
            message="API密钥停用成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{key_id}/revoke", response_model=APIResponse[APIKeyResponse])
async def revoke_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """撤销API密钥"""
    try:
        service = APIKeyService(db)
        api_key = await service.revoke_api_key(key_id, current_user.id)
        return APIResponse(
            success=True,
            data=APIKeyResponse.model_validate(api_key),
            message="API密钥撤销成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{key_id}", response_model=APIResponse[bool])
async def delete_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除API密钥"""
    try:
        service = APIKeyService(db)
        result = await service.delete_api_key(key_id, current_user.id)
        return APIResponse(
            success=True,
            data=result,
            message="API密钥删除成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{key_id}/extend", response_model=APIResponse[APIKeyResponse])
async def extend_api_key_expiry(
    key_id: int,
    days: int = Query(..., ge=1, le=365, description="延长天数"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """延长API密钥过期时间"""
    try:
        service = APIKeyService(db)
        api_key = await service.extend_expiry(key_id, current_user.id, days)
        return APIResponse(
            success=True,
            data=APIKeyResponse.model_validate(api_key),
            message=f"API密钥过期时间延长{days}天"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{key_id}/usage", response_model=APIResponse[APIKeyUsage])
async def get_api_key_usage(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取API密钥使用情况"""
    try:
        service = APIKeyService(db)
        api_key = await service.get_api_key_by_id(key_id, current_user.id)
        
        # 检查速率限制
        rate_limit_info = await service.check_rate_limit(key_id)
        
        usage_data = APIKeyUsage(
            key_id=api_key.id,
            key_name=api_key.name,
            usage_count=api_key.usage_count,
            last_used_at=api_key.last_used_at,
            rate_limit_remaining=rate_limit_info
        )
        
        return APIResponse(
            success=True,
            data=usage_data,
            message="获取使用情况成功"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )