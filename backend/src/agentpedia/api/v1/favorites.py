"""
收藏功能API端点
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import logging

from agentpedia.api.deps import get_current_active_user
from agentpedia.core.logging import get_logger
from agentpedia.models.user import User
from agentpedia.models.favorite import FavoriteCreate, FavoriteResponse
from agentpedia.services.favorite_service import favorite_service

router = APIRouter()
logger = get_logger(__name__)


@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_active_user)
):
    """添加收藏"""
    try:
        # 验证用户ID匹配
        if favorite_data.user_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限为其他用户添加收藏"
            )
        
        # 添加收藏
        favorite = await favorite_service.add_favorite(favorite_data)
        
        logger.info(f"Favorite added: user_id={current_user.id}, agent_id={favorite_data.agent_id}")
        
        return favorite
    
    except Exception as e:
        logger.error(f"Add favorite failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="添加收藏失败"
        )


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(
    agent_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """移除收藏"""
    try:
        # 移除收藏
        success = await favorite_service.remove_favorite(str(current_user.id), agent_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="收藏记录不存在"
            )
        
        logger.info(f"Favorite removed: user_id={current_user.id}, agent_id={agent_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Remove favorite failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="移除收藏失败"
        )


@router.get("/", response_model=List[FavoriteResponse])
async def get_user_favorites(
    current_user: User = Depends(get_current_active_user)
):
    """获取用户收藏列表"""
    try:
        favorites = await favorite_service.get_user_favorites(str(current_user.id))
        return favorites
    
    except Exception as e:
        logger.error(f"Get user favorites failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取收藏列表失败"
        )


@router.get("/{agent_id}", response_model=bool)
async def is_favorite(
    agent_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """检查是否已收藏"""
    try:
        is_fav = await favorite_service.is_favorite(str(current_user.id), agent_id)
        return is_fav
    
    except Exception as e:
        logger.error(f"Check favorite failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="检查收藏状态失败"
        )