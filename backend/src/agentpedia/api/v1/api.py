"""
API v1路由汇总
"""
from fastapi import APIRouter

from agentpedia.api.v1 import users, agents, agents_prd, conversations, api_keys, favorites, wechat
from agentpedia.api.v1 import search

api_router = APIRouter()

# 认证相关路由
api_router.include_router(wechat.router, prefix="/wechat", tags=["wechat"])

# 用户相关路由
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Agent相关路由
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(agents_prd.router, prefix="/agents-prd", tags=["agents-prd"])

# 对话相关路由
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])

# API密钥相关路由
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"])

# 收藏相关路由
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])

# 搜索相关路由
api_router.include_router(search.router, prefix="/search", tags=["search"])

# TODO: 添加其他路由
# api_router.include_router(usage_logs.router, prefix="/usage-logs", tags=["usage-logs"])