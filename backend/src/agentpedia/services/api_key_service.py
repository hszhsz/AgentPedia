"""
API密钥服务类
"""
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from agentpedia.models.api_key import APIKey, APIKeyStatus, APIKeyScope
from agentpedia.models.user import User
from agentpedia.schemas.api_key import APIKeyCreate, APIKeyUpdate
from agentpedia.services.base import BaseService
from agentpedia.core.exceptions import NotFoundError, PermissionError, ValidationError


class APIKeyService(BaseService[APIKey, APIKeyCreate, APIKeyUpdate]):
    """API密钥服务类"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(APIKey, db)
    
    def _generate_api_key(self) -> tuple[str, str, str]:
        """生成API密钥"""
        # 生成32字节的随机密钥
        key_bytes = secrets.token_bytes(32)
        key = secrets.token_urlsafe(32)
        
        # 生成前缀（前8个字符）
        prefix = key[:8]
        
        # 生成哈希
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        return key, prefix, key_hash
    
    async def create_api_key(self, key_data: APIKeyCreate, user_id: int) -> tuple[APIKey, str]:
        """创建API密钥"""
        # 检查用户是否存在
        user = await self.db.get(User, user_id)
        if not user:
            raise NotFoundError("用户不存在")
        
        # 检查用户的API密钥数量限制
        existing_keys_query = select(func.count(APIKey.id)).where(
            and_(
                APIKey.user_id == user_id,
                APIKey.status != APIKeyStatus.REVOKED
            )
        )
        existing_keys_result = await self.db.execute(existing_keys_query)
        existing_count = existing_keys_result.scalar() or 0
        
        # 限制每个用户最多10个活跃密钥
        if existing_count >= 10:
            raise ValidationError("API密钥数量已达上限（10个）")
        
        # 生成密钥
        key, prefix, key_hash = self._generate_api_key()
        
        # 创建API密钥记录
        api_key_dict = key_data.model_dump()
        api_key_dict.update({
            'user_id': user_id,
            'key_hash': key_hash,
            'prefix': prefix,
            'status': APIKeyStatus.ACTIVE
        })
        
        api_key = APIKey(**api_key_dict)
        self.db.add(api_key)
        await self.db.commit()
        await self.db.refresh(api_key)
        
        return api_key, key
    
    async def get_user_api_keys(
        self,
        user_id: int,
        status: Optional[APIKeyStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[APIKey]:
        """获取用户的API密钥列表"""
        query = select(APIKey).where(APIKey.user_id == user_id)
        
        if status:
            query = query.where(APIKey.status == status)
        
        query = query.order_by(APIKey.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars())
    
    async def get_api_key_by_id(self, key_id: int, user_id: int) -> APIKey:
        """根据ID获取API密钥"""
        query = select(APIKey).where(
            and_(
                APIKey.id == key_id,
                APIKey.user_id == user_id
            )
        )
        
        result = await self.db.execute(query)
        api_key = result.scalar_one_or_none()
        
        if not api_key:
            raise NotFoundError("API密钥不存在或无权访问")
        
        return api_key
    
    async def get_api_key_by_key(self, key: str) -> Optional[APIKey]:
        """根据密钥字符串获取API密钥"""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        query = select(APIKey).where(APIKey.key_hash == key_hash)
        result = await self.db.execute(query)
        
        return result.scalar_one_or_none()
    
    async def update_api_key(self, key_id: int, key_data: APIKeyUpdate, user_id: int) -> APIKey:
        """更新API密钥"""
        api_key = await self.get_api_key_by_id(key_id, user_id)
        
        # 更新数据
        update_data = key_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(api_key, field, value)
        
        await self.db.commit()
        await self.db.refresh(api_key)
        
        return api_key
    
    async def activate_api_key(self, key_id: int, user_id: int) -> APIKey:
        """激活API密钥"""
        api_key = await self.get_api_key_by_id(key_id, user_id)
        
        if api_key.status == APIKeyStatus.REVOKED:
            raise ValidationError("已撤销的密钥无法激活")
        
        api_key.status = APIKeyStatus.ACTIVE
        await self.db.commit()
        await self.db.refresh(api_key)
        
        return api_key
    
    async def deactivate_api_key(self, key_id: int, user_id: int) -> APIKey:
        """停用API密钥"""
        api_key = await self.get_api_key_by_id(key_id, user_id)
        
        api_key.status = APIKeyStatus.INACTIVE
        await self.db.commit()
        await self.db.refresh(api_key)
        
        return api_key
    
    async def revoke_api_key(self, key_id: int, user_id: int) -> APIKey:
        """撤销API密钥"""
        api_key = await self.get_api_key_by_id(key_id, user_id)
        
        api_key.status = APIKeyStatus.REVOKED
        await self.db.commit()
        await self.db.refresh(api_key)
        
        return api_key
    
    async def delete_api_key(self, key_id: int, user_id: int) -> bool:
        """删除API密钥"""
        api_key = await self.get_api_key_by_id(key_id, user_id)
        
        self.db.delete(api_key)
        await self.db.commit()
        
        return True
    
    async def update_usage(self, key_id: int, ip_address: str) -> bool:
        """更新API密钥使用情况"""
        api_key = await self.db.get(APIKey, key_id)
        if not api_key:
            return False
        
        api_key.usage_count += 1
        api_key.last_used_at = datetime.utcnow()
        api_key.last_used_ip = ip_address
        
        await self.db.commit()
        return True
    
    async def check_rate_limit(self, key_id: int) -> Dict[str, Any]:
        """检查速率限制"""
        api_key = await self.db.get(APIKey, key_id)
        if not api_key:
            return {'allowed': False, 'reason': 'API密钥不存在'}
        
        if api_key.status != APIKeyStatus.ACTIVE:
            return {'allowed': False, 'reason': 'API密钥未激活'}
        
        # 检查过期时间
        if api_key.expires_at and api_key.expires_at < datetime.utcnow():
            return {'allowed': False, 'reason': 'API密钥已过期'}
        
        # 这里应该实现实际的速率限制检查逻辑
        # 可以使用Redis或内存缓存来跟踪请求频率
        # 暂时返回允许
        return {
            'allowed': True,
            'rate_limit_per_minute': api_key.rate_limit_per_minute,
            'rate_limit_per_hour': api_key.rate_limit_per_hour,
            'rate_limit_per_day': api_key.rate_limit_per_day
        }
    
    async def extend_expiry(self, key_id: int, user_id: int, days: int) -> APIKey:
        """延长API密钥过期时间"""
        api_key = await self.get_api_key_by_id(key_id, user_id)
        
        if api_key.expires_at:
            # 如果已经有过期时间，在此基础上延长
            api_key.expires_at += timedelta(days=days)
        else:
            # 如果没有过期时间，从现在开始计算
            api_key.expires_at = datetime.utcnow() + timedelta(days=days)
        
        await self.db.commit()
        await self.db.refresh(api_key)
        
        return api_key
    
    async def get_api_key_stats(self, user_id: int) -> Dict[str, Any]:
        """获取用户的API密钥统计信息"""
        # 总密钥数
        total_query = select(func.count(APIKey.id)).where(APIKey.user_id == user_id)
        total_result = await self.db.execute(total_query)
        total_keys = total_result.scalar() or 0
        
        # 活跃密钥数
        active_query = select(func.count(APIKey.id)).where(
            and_(
                APIKey.user_id == user_id,
                APIKey.status == APIKeyStatus.ACTIVE
            )
        )
        active_result = await self.db.execute(active_query)
        active_keys = active_result.scalar() or 0
        
        # 过期密钥数
        expired_query = select(func.count(APIKey.id)).where(
            and_(
                APIKey.user_id == user_id,
                APIKey.expires_at < datetime.utcnow()
            )
        )
        expired_result = await self.db.execute(expired_query)
        expired_keys = expired_result.scalar() or 0
        
        # 已撤销密钥数
        revoked_query = select(func.count(APIKey.id)).where(
            and_(
                APIKey.user_id == user_id,
                APIKey.status == APIKeyStatus.REVOKED
            )
        )
        revoked_result = await self.db.execute(revoked_query)
        revoked_keys = revoked_result.scalar() or 0
        
        # 总使用次数
        usage_query = select(func.sum(APIKey.usage_count)).where(APIKey.user_id == user_id)
        usage_result = await self.db.execute(usage_query)
        total_usage = usage_result.scalar() or 0
        
        return {
            'total_keys': total_keys,
            'active_keys': active_keys,
            'expired_keys': expired_keys,
            'revoked_keys': revoked_keys,
            'total_usage': total_usage
        }
    
    async def validate_api_key(self, key: str) -> Optional[APIKey]:
        """验证API密钥"""
        api_key = await self.get_api_key_by_key(key)
        
        if not api_key:
            return None
        
        # 检查状态
        if api_key.status != APIKeyStatus.ACTIVE:
            return None
        
        # 检查过期时间
        if api_key.expires_at and api_key.expires_at < datetime.utcnow():
            return None
        
        return api_key