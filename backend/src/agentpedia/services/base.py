"""
基础服务类
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from agentpedia.models.base import BaseModel as DBBaseModel

ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """基础服务类"""
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        初始化基础服务
        
        Args:
            model: 数据模型类
            db: 数据库会话
        """
        self.model = model
        self.db = db
    
    async def get(self, id: Any) -> Optional[ModelType]:
        """根据ID获取单个对象"""
        stmt = select(self.model).where(
            self.model.id == id,
            self.model.deleted_at.is_(None)
        )
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[ModelType]:
        """获取多个对象"""
        conditions = [self.model.deleted_at.is_(None)]
        
        # 添加过滤条件
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                conditions.append(getattr(self.model, key) == value)
        
        stmt = (
            select(self.model)
            .where(and_(*conditions))
            .offset(skip)
            .limit(limit)
            .order_by(self.model.created_at.desc())
        )
        result = self.db.execute(stmt)
        return list(result.scalars())
    
    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """创建对象"""
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """更新对象"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def delete(self, id: Any) -> Optional[ModelType]:
        """软删除对象"""
        db_obj = await self.get(id)
        if db_obj:
            db_obj.soft_delete()
            await self.db.commit()
        return db_obj
    
    async def hard_delete(self, id: Any) -> bool:
        """硬删除对象"""
        db_obj = await self.get(id)
        if db_obj:
            self.db.delete(db_obj)
            await self.db.commit()
            return True
        return False
    
    async def count(self, **filters) -> int:
        """统计对象数量"""
        conditions = [self.model.deleted_at.is_(None)]
        
        # 添加过滤条件
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                conditions.append(getattr(self.model, key) == value)
        
        stmt = select(func.count(self.model.id)).where(and_(*conditions))
        result = self.db.execute(stmt)
        return result.scalar()
    
    async def exists(self, id: Any) -> bool:
        """检查对象是否存在"""
        obj = await self.get(id)
        return obj is not None
    
    async def get_or_create(
        self,
        defaults: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> tuple[ModelType, bool]:
        """获取或创建对象"""
        # 查找现有对象
        conditions = [self.model.deleted_at.is_(None)]
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                conditions.append(getattr(self.model, key) == value)
        
        stmt = select(self.model).where(and_(*conditions))
        result = self.db.execute(stmt)
        obj = result.scalar_one_or_none()
        
        if obj:
            return obj, False
        
        # 创建新对象
        create_data = kwargs.copy()
        if defaults:
            create_data.update(defaults)
        
        obj = self.model(**create_data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        
        return obj, True
    
    async def bulk_create(self, objs_in: List[CreateSchemaType]) -> List[ModelType]:
        """批量创建对象"""
        db_objs = []
        for obj_in in objs_in:
            obj_data = obj_in.model_dump()
            db_obj = self.model(**obj_data)
            db_objs.append(db_obj)
        
        self.db.add_all(db_objs)
        await self.db.commit()
        
        for db_obj in db_objs:
            await self.db.refresh(db_obj)
        
        return db_objs
    
    async def bulk_update(
        self,
        updates: List[Dict[str, Any]]
    ) -> List[ModelType]:
        """批量更新对象"""
        updated_objs = []
        
        for update_data in updates:
            obj_id = update_data.pop("id")
            db_obj = await self.get(obj_id)
            if db_obj:
                for field, value in update_data.items():
                    if hasattr(db_obj, field):
                        setattr(db_obj, field, value)
                updated_objs.append(db_obj)
        
        await self.db.commit()
        
        for db_obj in updated_objs:
            await self.db.refresh(db_obj)
        
        return updated_objs
    
    async def bulk_delete(self, ids: List[Any]) -> int:
        """批量软删除对象"""
        count = 0
        for obj_id in ids:
            db_obj = await self.get(obj_id)
            if db_obj:
                db_obj.soft_delete()
                count += 1
        
        await self.db.commit()
        return count