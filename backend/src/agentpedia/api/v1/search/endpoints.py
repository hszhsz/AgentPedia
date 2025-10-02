"""
搜索API端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from agentpedia.core.database import get_db
from agentpedia.services.search_service import search_service, SearchType, SortType
from agentpedia.schemas.agent_prd import AgentSearchQuery, AgentFilterParams
from agentpedia.schemas.common import ResponseModel
from agentpedia.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/agents", response_model=ResponseModel)
async def search_agents(
    q: str = Query(..., description="搜索关键词"),
    search_type: SearchType = Query(SearchType.HYBRID, description="搜索类型"),
    sort_by: SortType = Query(SortType.RELEVANCE, description="排序方式"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页大小"),
    language: str = Query("zh", description="搜索语言"),
    status: Optional[str] = Query(None, description="状态过滤"),
    tags: Optional[str] = Query(None, description="标签过滤，逗号分隔"),
    technical_stack: Optional[str] = Query(None, description="技术栈过滤，逗号分隔"),
    db = Depends(get_db)
):
    """搜索Agent"""
    try:
        # 构建过滤条件
        filters = {}
        if status:
            filters["status"] = status
        if tags:
            filters["tags"] = [tag.strip() for tag in tags.split(",") if tag.strip()]
        if technical_stack:
            filters["technical_stack"] = [tech.strip() for tech in technical_stack.split(",") if tech.strip()]

        # 执行搜索
        result = await search_service.search_agents(
            query=q,
            search_type=search_type,
            filters=filters,
            sort_by=sort_by,
            page=page,
            size=size,
            language=language
        )

        return ResponseModel(
            success=True,
            message="搜索成功",
            data=result
        )

    except Exception as e:
        logger.error(f"搜索失败: {e}")
        raise HTTPException(status_code=500, detail="搜索失败")


@router.get("/suggestions", response_model=ResponseModel)
async def get_search_suggestions(
    q: str = Query(..., description="搜索前缀"),
    size: int = Query(5, ge=1, le=20, description="建议数量"),
    language: str = Query("zh", description="搜索语言"),
    db = Depends(get_db)
):
    """获取搜索建议"""
    try:
        suggestions = await search_service.get_search_suggestions(
            query=q,
            size=size,
            language=language
        )

        return ResponseModel(
            success=True,
            message="获取建议成功",
            data=suggestions
        )

    except Exception as e:
        logger.error(f"获取搜索建议失败: {e}")
        raise HTTPException(status_code=500, detail="获取搜索建议失败")


@router.get("/popular", response_model=ResponseModel)
async def get_popular_agents(
    limit: int = Query(10, ge=1, le=50, description="推荐数量"),
    time_range: Optional[int] = Query(None, description="时间范围（天数）"),
    db = Depends(get_db)
):
    """获取热门Agent"""
    try:
        agents = await search_service.get_popular_agents(
            limit=limit,
            time_range=time_range
        )

        return ResponseModel(
            success=True,
            message="获取热门Agent成功",
            data=agents
        )

    except Exception as e:
        logger.error(f"获取热门Agent失败: {e}")
        raise HTTPException(status_code=500, detail="获取热门Agent失败")


@router.post("/reindex", response_model=ResponseModel)
async def reindex_all_agents(db = Depends(get_db)):
    """重新索引所有Agent到Elasticsearch"""
    try:
        count = await search_service.reindex_all_agents()

        return ResponseModel(
            success=True,
            message=f"成功重新索引 {count} 个Agent",
            data={"indexed_count": count}
        )

    except Exception as e:
        logger.error(f"重新索引失败: {e}")
        raise HTTPException(status_code=500, detail="重新索引失败")


@router.get("/types", response_model=ResponseModel)
async def get_search_types():
    """获取支持的搜索类型"""
    search_types = [
        {"value": search_type.value, "label": search_type.value}
        for search_type in SearchType
    ]

    return ResponseModel(
        success=True,
        message="获取搜索类型成功",
        data=search_types
    )


@router.get("/sort-types", response_model=ResponseModel)
async def get_sort_types():
    """获取支持的排序类型"""
    sort_types = [
        {"value": sort_type.value, "label": sort_type.value}
        for sort_type in SortType
    ]

    return ResponseModel(
        success=True,
        message="获取排序类型成功",
        data=sort_types
    )