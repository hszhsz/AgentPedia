"""
用户服务层
"""
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from agentpedia.core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from agentpedia.models.user import User, UserRole, UserStatus
from agentpedia.schemas.user import UserCreate, UserUpdate
from agentpedia.schemas.base import PaginationParams, FilterParams
from agentpedia.services.base import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """用户服务"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
    
    async def create_user(self, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查用户名和邮箱是否已存在
        existing_user = await self.get_by_username_or_email(
            user_data.username, user_data.email
        )
        if existing_user:
            if existing_user.username == user_data.username:
                raise ValueError("用户名已存在")
            if existing_user.email == user_data.email:
                raise ValueError("邮箱已存在")
        
        # 创建用户
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            bio=user_data.bio,
            avatar_url=user_data.avatar_url,
            timezone=user_data.timezone,
            language=user_data.language,
            theme=user_data.theme,
            role=UserRole.USER,
            status=UserStatus.PENDING,
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def authenticate_user(self, username: str, password: str, ip_address: str) -> Optional[User]:
        """用户认证"""
        user = await self.get_by_username_or_email(username, username)
        if not user:
            return None
        
        # 检查账户是否被锁定
        if user.is_locked:
            return None
        
        # 验证密码
        if not verify_password(password, user.hashed_password):
            user.increment_failed_login()
            await self.db.commit()
            return None
        
        # 检查用户状态
        if not user.is_active:
            return None
        
        # 更新登录信息
        user.update_login_info(ip_address)
        await self.db.commit()
        
        return user
    
    async def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        """根据用户名或邮箱获取用户"""
        stmt = select(User).where(
            or_(User.username == username, User.email == email),
            User.deleted_at.is_(None)
        )
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        stmt = select(User).where(
            User.username == username,
            User.deleted_at.is_(None)
        )
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        stmt = select(User).where(
            User.email == email,
            User.deleted_at.is_(None)
        )
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        user = await self.get(user_id)
        if not user:
            return None
        
        # 更新字段
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """修改密码"""
        user = await self.get(user_id)
        if not user:
            return False
        
        # 验证当前密码
        if not verify_password(current_password, user.hashed_password):
            return False
        
        # 更新密码
        user.hashed_password = get_password_hash(new_password)
        user.change_password()
        
        await self.db.commit()
        return True
    
    async def reset_password(self, email: str, new_password: str) -> bool:
        """重置密码"""
        user = await self.get_by_email(email)
        if not user:
            return False
        
        user.hashed_password = get_password_hash(new_password)
        user.change_password()
        user.unlock_account()  # 解锁账户
        
        await self.db.commit()
        return True
    
    async def verify_email(self, user_id: int) -> bool:
        """验证邮箱"""
        user = await self.get(user_id)
        if not user:
            return False
        
        user.verify_email()
        await self.db.commit()
        return True
    
    async def lock_user(self, user_id: int, duration_minutes: int = 30) -> bool:
        """锁定用户"""
        user = await self.get(user_id)
        if not user:
            return False
        
        user.lock_account(duration_minutes)
        await self.db.commit()
        return True
    
    async def unlock_user(self, user_id: int) -> bool:
        """解锁用户"""
        user = await self.get(user_id)
        if not user:
            return False
        
        user.unlock_account()
        await self.db.commit()
        return True
    
    async def activate_user(self, user_id: int) -> bool:
        """激活用户"""
        user = await self.get(user_id)
        if not user:
            return False
        
        user.status = UserStatus.ACTIVE
        await self.db.commit()
        return True
    
    async def deactivate_user(self, user_id: int) -> bool:
        """停用用户"""
        user = await self.get(user_id)
        if not user:
            return False
        
        user.status = UserStatus.INACTIVE
        await self.db.commit()
        return True
    
    async def suspend_user(self, user_id: int) -> bool:
        """暂停用户"""
        user = await self.get(user_id)
        if not user:
            return False
        
        user.status = UserStatus.SUSPENDED
        await self.db.commit()
        return True
    
    async def change_role(self, user_id: int, new_role: UserRole) -> bool:
        """修改用户角色"""
        user = await self.get(user_id)
        if not user:
            return False
        
        user.role = new_role
        await self.db.commit()
        return True
    
    async def get_users_with_filters(
        self,
        pagination: PaginationParams,
        filters: FilterParams
    ) -> Tuple[List[User], int]:
        """获取用户列表（带过滤和分页）"""
        # 构建查询条件
        conditions = [User.deleted_at.is_(None)]
        
        if filters.search:
            search_term = f"%{filters.search}%"
            conditions.append(
                or_(
                    User.username.ilike(search_term),
                    User.email.ilike(search_term),
                    User.full_name.ilike(search_term)
                )
            )
        
        if filters.status:
            conditions.append(User.status == filters.status)
        
        if filters.created_after:
            conditions.append(User.created_at >= filters.created_after)
        
        if filters.created_before:
            conditions.append(User.created_at <= filters.created_before)
        
        # 查询总数
        count_stmt = select(func.count(User.id)).where(and_(*conditions))
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar()
        
        # 查询数据
        stmt = (
            select(User)
            .where(and_(*conditions))
            .offset(pagination.offset)
            .limit(pagination.size)
            .order_by(User.created_at.desc())
        )
        result = self.db.execute(stmt)
        users = list(result.scalars())
        
        return users, total
    
    async def get_user_stats(self, user_id: int) -> Optional[dict]:
        """获取用户统计信息"""
        user = await self.get(user_id)
        if not user:
            return None
        
        # 这里应该查询相关的统计数据
        # 暂时返回模拟数据
        return {
            "total_agents": 0,
            "active_agents": 0,
            "total_conversations": 0,
            "total_messages": 0,
            "total_tokens_used": 0,
            "total_cost": 0.0,
            "api_keys_count": 0,
        }
    
    async def create_tokens(self, user: User) -> dict:
        """创建访问令牌和刷新令牌"""
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "username": user.username}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 3600,  # 1小时
        }