"""
Redis连接和缓存管理
"""
import json
from typing import Any, Optional, Union

import redis.asyncio as redis
from redis.asyncio import Redis

from agentpedia.core.config import get_settings

settings = get_settings()


class RedisManager:
    """Redis管理器"""
    
    def __init__(self):
        self.redis_client: Optional[Redis] = None
    
    async def init_redis(self) -> None:
        """初始化Redis连接"""
        self.redis_client = redis.from_url(
            settings.get_redis_url(),
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )
    
    async def close_redis(self) -> None:
        """关闭Redis连接"""
        if self.redis_client:
            await self.redis_client.close()
    
    async def get(self, key: str) -> Optional[str]:
        """获取缓存值"""
        if not self.redis_client:
            return None
        return await self.redis_client.get(key)
    
    async def set(
        self,
        key: str,
        value: Union[str, dict, list],
        expire: Optional[int] = None
    ) -> bool:
        """设置缓存值"""
        if not self.redis_client:
            return False
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        
        return await self.redis_client.set(key, value, ex=expire)
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.redis_client:
            return False
        return bool(await self.redis_client.delete(key))
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self.redis_client:
            return False
        return bool(await self.redis_client.exists(key))
    
    async def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间"""
        if not self.redis_client:
            return False
        return await self.redis_client.expire(key, seconds)
    
    async def get_json(self, key: str) -> Optional[Union[dict, list]]:
        """获取JSON格式的缓存值"""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return None
    
    async def set_json(
        self,
        key: str,
        value: Union[dict, list],
        expire: Optional[int] = None
    ) -> bool:
        """设置JSON格式的缓存值"""
        json_value = json.dumps(value, ensure_ascii=False)
        return await self.set(key, json_value, expire)
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """递增计数器"""
        if not self.redis_client:
            return 0
        return await self.redis_client.incr(key, amount)
    
    async def decr(self, key: str, amount: int = 1) -> int:
        """递减计数器"""
        if not self.redis_client:
            return 0
        return await self.redis_client.decr(key, amount)
    
    async def sadd(self, key: str, *values: Any) -> int:
        """添加到集合"""
        if not self.redis_client:
            return 0
        return await self.redis_client.sadd(key, *values)
    
    async def srem(self, key: str, *values: Any) -> int:
        """从集合中移除"""
        if not self.redis_client:
            return 0
        return await self.redis_client.srem(key, *values)
    
    async def smembers(self, key: str) -> set:
        """获取集合所有成员"""
        if not self.redis_client:
            return set()
        return await self.redis_client.smembers(key)
    
    async def sismember(self, key: str, value: Any) -> bool:
        """检查是否为集合成员"""
        if not self.redis_client:
            return False
        return await self.redis_client.sismember(key, value)
    
    async def lpush(self, key: str, *values: Any) -> int:
        """从左侧推入列表"""
        if not self.redis_client:
            return 0
        return await self.redis_client.lpush(key, *values)
    
    async def rpush(self, key: str, *values: Any) -> int:
        """从右侧推入列表"""
        if not self.redis_client:
            return 0
        return await self.redis_client.rpush(key, *values)
    
    async def lpop(self, key: str) -> Optional[str]:
        """从左侧弹出列表元素"""
        if not self.redis_client:
            return None
        return await self.redis_client.lpop(key)
    
    async def rpop(self, key: str) -> Optional[str]:
        """从右侧弹出列表元素"""
        if not self.redis_client:
            return None
        return await self.redis_client.rpop(key)
    
    async def lrange(self, key: str, start: int = 0, end: int = -1) -> list:
        """获取列表范围"""
        if not self.redis_client:
            return []
        return await self.redis_client.lrange(key, start, end)


# 创建全局Redis管理器实例
redis_manager = RedisManager()


async def get_redis() -> RedisManager:
    """获取Redis管理器"""
    return redis_manager


# 缓存装饰器
def cache_result(expire: int = 300, key_prefix: str = ""):
    """缓存结果装饰器"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # 尝试从缓存获取
            cached_result = await redis_manager.get_json(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行函数并缓存结果
            result = await func(*args, **kwargs)
            if result is not None:
                await redis_manager.set_json(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator