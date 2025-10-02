"""
AgentPedia 主应用入口
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_client import make_asgi_app

from agentpedia.api.v1.api import api_router
from agentpedia.core.config import get_settings
from agentpedia.core.database import close_db, init_db, AsyncSessionLocal
from agentpedia.core.logging import (
    PerformanceLoggingMiddleware,
    RequestLoggingMiddleware,
    configure_logging,
    get_logger,
)
from agentpedia.core.redis import redis_manager
from agentpedia.core.mongodb import mongodb_manager
from agentpedia.core.security import get_password_hash
from sqlalchemy import select
from agentpedia.models.user import User, UserRole, UserStatus

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("Starting AgentPedia application")
    
    # 配置日志
    configure_logging()
    
    # 初始化数据库
    await init_db()
    logger.info("Database initialized")
    
    # 初始化Redis
    await redis_manager.init_redis()
    logger.info("Redis initialized")
    
    # 初始化MongoDB
    await mongodb_manager.init_mongodb()
    logger.info("MongoDB initialized")
    
    # 初始化MongoDB服务
    from agentpedia.services.mongodb_agent_service import mongodb_agent_service
    from agentpedia.services.favorite_service import favorite_service
    await mongodb_agent_service.init_service()
    await favorite_service.init_service()
    logger.info("MongoDB services initialized")

    # 在开发/测试环境下，预置一个Mock管理员用户以支持无鉴权访问
    if settings.MOCK_AUTH_ENABLED:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(User).where(User.username == "mock_admin")
                )
                mock = result.scalar_one_or_none()
                if not mock:
                    mock = User(
                        username="mock_admin",
                        email="mock@example.com",
                        hashed_password=get_password_hash("mockpass"),
                        role=UserRole.ADMIN,
                        status=UserStatus.ACTIVE,
                        full_name="Mock Admin",
                    )
                    session.add(mock)
                    await session.commit()
                    logger.info("Seeded mock admin user")
        except Exception as e:
            logger.warning("Seeding mock user failed", error=str(e))
    
    yield
    
    # 关闭时执行
    logger.info("Shutting down AgentPedia application")
    
    # 关闭数据库连接
    await close_db()
    logger.info("Database connections closed")
    
    # 关闭Redis连接
    await redis_manager.close_redis()
    logger.info("Redis connections closed")
    
    # 关闭MongoDB连接
    await mongodb_manager.close_mongodb()
    logger.info("MongoDB connections closed")


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="AI Agent Management Platform",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,
    )
    
    # 添加CORS中间件
    cors_origins = settings.get_cors_origins()
    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # 添加受信任主机中间件
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
    )
    
    # 添加自定义中间件
    app.add_middleware(PerformanceLoggingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    
    # 添加API路由
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # 添加健康检查端点
    @app.get("/health")
    async def health_check():
        """健康检查"""
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
        }
    
    # 添加指标端点（如果启用）
    if settings.ENABLE_METRICS:
        metrics_app = make_asgi_app()
        app.mount("/metrics", metrics_app)
    
    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "agentpedia.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )