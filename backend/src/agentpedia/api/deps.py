"""
API依赖项
"""
from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from agentpedia.core.config import settings
from agentpedia.core.security import get_password_hash
from agentpedia.models.user import User, UserRole, UserStatus
from agentpedia.core.database import get_db
from agentpedia.models.user import User
from agentpedia.services.user_service import UserService

# security = HTTPBearer()  # 禁用安全检查
# optional_security = HTTPBearer(auto_error=False)  # 禁用安全检查


async def get_current_user(
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    # 直接返回Mock管理员用户，不检查权限
    from agentpedia.models.user import LoginMethod
    from datetime import datetime

    mock = User(
        id=2,
        username="mock_admin",
        email="mock@example.com",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewxBobJOiZLWLH/K",  # pre-hashed "mockpass"
        login_method=LoginMethod.EMAIL,
        nickname="Mock Admin",
        full_name="Mock Admin",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
        is_email_verified=True,
        email_verified_at=datetime.utcnow(),
        login_count=1,
        password_changed_at=datetime.utcnow(),
        timezone="UTC",
        language="en",
        theme="light",
    )
    return mock


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前管理员用户"""
    # 直接返回管理员用户，不检查权限
    return current_user


async def get_optional_current_user(
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """获取可选的当前用户（用于公开接口）"""
    # 直接返回Mock管理员用户，不检查权限
    from agentpedia.models.user import LoginMethod
    from datetime import datetime

    return User(
        id=2,
        username="mock_admin",
        email="mock@example.com",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewxBobJOiZLWLH/K",  # pre-hashed "mockpass"
        login_method=LoginMethod.EMAIL,
        nickname="Mock Admin",
        full_name="Mock Admin",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
        is_email_verified=True,
        email_verified_at=datetime.utcnow(),
        login_count=1,
        password_changed_at=datetime.utcnow(),
        timezone="UTC",
        language="en",
        theme="light",
    )


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """获取用户服务"""
    return UserService(db)


async def get_agent_service(db: AsyncSession = Depends(get_db)):
    """获取Agent服务"""
    from agentpedia.services.agent_service import AgentService
    return AgentService(db)


async def get_conversation_service(db: AsyncSession = Depends(get_db)):
    """获取对话服务"""
    from agentpedia.services.conversation_service import ConversationService
    return ConversationService(db)


async def get_api_key_service(db: AsyncSession = Depends(get_db)):
    """获取API密钥服务"""
    from agentpedia.services.api_key_service import APIKeyService
    return APIKeyService(db)