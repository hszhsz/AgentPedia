"""
基于角色的访问控制(RBAC)服务
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload

from agentpedia.core.database import AsyncSessionLocal
from agentpedia.models.permission import (
    Role, Permission, UserRoleAssignment, PermissionResource, PermissionAction
)
from agentpedia.models.user import User
from agentpedia.core.logging import get_logger

logger = get_logger(__name__)


class RBACService:
    """RBAC服务类"""

    def __init__(self):
        self._default_permissions: Dict[str, List[str]] = {
            "super_admin": ["*"],
            "admin": [
                "user.create", "user.read", "user.update", "user.delete",
                "user.manage", "role.create", "role.read", "role.update", "role.delete",
                "permission.create", "permission.read", "permission.update", "permission.delete",
                "agent.create", "agent.read", "agent.update", "agent.delete", "agent.manage",
                "api_key.create", "api_key.read", "api_key.update", "api_key.delete",
                "conversation.read", "conversation.manage", "favorite.read", "favorite.manage",
                "usage_log.read", "audit_log.read", "system.manage"
            ],
            "moderator": [
                "agent.read", "agent.update", "conversation.read", "conversation.manage",
                "api_key.read", "favorite.read", "favorite.manage", "usage_log.read"
            ],
            "developer": [
                "agent.create", "agent.read", "agent.update", "agent.delete",
                "api_key.create", "api_key.read", "api_key.delete",
                "conversation.read", "favorite.create", "favorite.read", "favorite.delete",
                "usage_log.read"
            ],
            "pro_user": [
                "agent.create", "agent.read", "agent.update", "agent.delete",
                "api_key.create", "api_key.read", "api_key.delete",
                "conversation.create", "conversation.read", "conversation.update",
                "favorite.create", "favorite.read", "favorite.delete",
                "usage_log.read"
            ],
            "user": [
                "agent.create", "agent.read", "agent.update", "agent.delete",
                "api_key.create", "api_key.read", "api_key.delete",
                "conversation.create", "conversation.read", "conversation.update",
                "favorite.create", "favorite.read", "favorite.delete",
                "usage_log.read"
            ],
            "verified_user": [
                "agent.read", "conversation.create", "conversation.read",
                "favorite.create", "favorite.read", "favorite.delete",
                "usage_log.read"
            ],
            "viewer": [
                "agent.read", "conversation.read", "usage_log.read"
            ]
        }

    async def create_permission(
        self,
        name: str,
        resource: PermissionResource,
        action: PermissionAction,
        description: str = None,
        is_system: bool = False
    ) -> Permission:
        """创建权限"""
        async with AsyncSessionLocal() as session:
            # 检查权限是否已存在
            code = Permission.generate_code(resource, action)
            result = await session.execute(
                select(Permission).where(Permission.code == code)
            )
            existing = result.scalar_one_or_none()

            if existing:
                return existing

            permission = Permission(
                name=name,
                code=code,
                resource=resource.value,
                action=action.value,
                description=description,
                is_system=is_system
            )

            session.add(permission)
            await session.commit()
            await session.refresh(permission)

            logger.info(f"Created permission: {code}")
            return permission

    async def create_role(
        self,
        name: str,
        code: str,
        display_name: str,
        description: str = None,
        level: int = 0,
        is_system: bool = False,
        max_api_keys: int = 5,
        max_agents: int = 10,
        permission_codes: List[str] = None
    ) -> Role:
        """创建角色"""
        async with AsyncSessionLocal() as session:
            # 检查角色是否已存在
            result = await session.execute(
                select(Role).where(Role.code == code)
            )
            existing = result.scalar_one_or_none()

            if existing:
                return existing

            role = Role(
                name=name,
                code=code,
                display_name=display_name,
                description=description,
                level=level,
                is_system=is_system,
                max_api_keys=max_api_keys,
                max_agents=max_agents
            )

            session.add(role)
            await session.flush()  # 获取角色ID

            # 添加权限
            if permission_codes:
                for perm_code in permission_codes:
                    permission = await self.get_permission_by_code(perm_code)
                    if permission:
                        role.permissions.append(permission)

            await session.commit()
            await session.refresh(role)

            logger.info(f"Created role: {code}")
            return role

    async def get_permission_by_code(self, code: str) -> Optional[Permission]:
        """根据代码获取权限"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Permission).where(Permission.code == code)
            )
            return result.scalar_one_or_none()

    async def get_role_by_code(self, code: str) -> Optional[Role]:
        """根据代码获取角色"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Role).options(selectinload(Role.permissions)).where(Role.code == code)
            )
            return result.scalar_one_or_none()

    async def assign_role_to_user(
        self,
        user_id: int,
        role_code: str,
        granted_by: int = None,
        expires_at: datetime = None,
        reason: str = None
    ) -> Optional[UserRoleAssignment]:
        """为用户分配角色"""
        async with AsyncSessionLocal() as session:
            # 获取角色
            role = await self.get_role_by_code(role_code)
            if not role:
                raise ValueError(f"Role not found: {role_code}")

            # 检查是否已有该角色
            result = await session.execute(
                select(UserRoleAssignment).where(
                    and_(
                        UserRoleAssignment.user_id == user_id,
                        UserRoleAssignment.role_id == role.id,
                        UserRoleAssignment.is_active == True
                    )
                )
            )
            existing = result.scalar_one_or_none()

            if existing and existing.is_valid():
                return existing

            # 创建新的角色分配
            assignment = UserRoleAssignment(
                user_id=user_id,
                role_id=role.id,
                granted_by=granted_by,
                expires_at=expires_at,
                reason=reason
            )

            session.add(assignment)
            await session.commit()
            await session.refresh(assignment)

            logger.info(f"Assigned role {role_code} to user {user_id}")
            return assignment

    async def revoke_role_from_user(
        self,
        user_id: int,
        role_code: str,
        revoked_by: int = None
    ) -> bool:
        """撤销用户角色"""
        async with AsyncSessionLocal() as session:
            role = await self.get_role_by_code(role_code)
            if not role:
                raise ValueError(f"Role not found: {role_code}")

            result = await session.execute(
                select(UserRoleAssignment).where(
                    and_(
                        UserRoleAssignment.user_id == user_id,
                        UserRoleAssignment.role_id == role.id,
                        UserRoleAssignment.is_active == True
                    )
                )
            )
            assignment = result.scalar_one_or_none()

            if not assignment:
                return False

            assignment.is_active = False
            await session.commit()

            logger.info(f"Revoked role {role_code} from user {user_id}")
            return True

    async def get_user_permissions(self, user_id: int) -> List[str]:
        """获取用户所有权限"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(UserRoleAssignment)
                .options(selectinload(UserRoleAssignment.role).selectinload(Role.permissions))
                .where(
                    and_(
                        UserRoleAssignment.user_id == user_id,
                        UserRoleAssignment.is_active == True,
                        or_(
                            UserRoleAssignment.expires_at.is_(None),
                            UserRoleAssignment.expires_at > datetime.utcnow()
                        )
                    )
                )
            )
            assignments = result.scalars().all()

            permissions = []
            for assignment in assignments:
                if assignment.role.is_active:
                    for permission in assignment.role.permissions:
                        if permission.code not in permissions:
                            permissions.append(permission.code)

            return permissions

    async def check_user_permission(
        self,
        user_id: int,
        resource: PermissionResource,
        action: PermissionAction
    ) -> bool:
        """检查用户权限"""
        permissions = await self.get_user_permissions(user_id)
        permission_code = Permission.generate_code(resource, action)
        return permission_code in permissions or "*" in permissions

    async def initialize_default_permissions(self):
        """初始化默认权限"""
        logger.info("Initializing default permissions")

        # 为所有资源和动作组合创建权限
        resources = list(PermissionResource)
        actions = list(PermissionAction)

        for resource in resources:
            for action in actions:
                code = Permission.generate_code(resource, action)
                name = f"{resource.value} {action.value}"
                description = f"权限：{resource.value} {action.value}"

                await self.create_permission(
                    name=name,
                    resource=resource,
                    action=action,
                    description=description,
                    is_system=True
                )

        logger.info("Default permissions initialized")

    async def initialize_default_roles(self):
        """初始化默认角色"""
        logger.info("Initializing default roles")

        role_configs = {
            "super_admin": {
                "display_name": "超级管理员",
                "description": "系统超级管理员，拥有所有权限",
                "level": 100,
                "max_api_keys": 100,
                "max_agents": 1000
            },
            "admin": {
                "display_name": "管理员",
                "description": "系统管理员，管理用户和系统配置",
                "level": 90,
                "max_api_keys": 50,
                "max_agents": 500
            },
            "moderator": {
                "display_name": "版主",
                "description": "内容管理员，管理内容和用户行为",
                "level": 80,
                "max_api_keys": 20,
                "max_agents": 100
            },
            "developer": {
                "display_name": "开发者",
                "description": "开发者，可以创建和管理Agent",
                "level": 70,
                "max_api_keys": 10,
                "max_agents": 50
            },
            "pro_user": {
                "display_name": "专业用户",
                "description": "专业用户，拥有更多高级功能",
                "level": 60,
                "max_api_keys": 8,
                "max_agents": 30
            },
            "user": {
                "display_name": "普通用户",
                "description": "普通用户，基本功能权限",
                "level": 50,
                "max_api_keys": 5,
                "max_agents": 10
            },
            "verified_user": {
                "display_name": "已验证用户",
                "description": "已验证邮箱的用户",
                "level": 40,
                "max_api_keys": 3,
                "max_agents": 5
            },
            "viewer": {
                "display_name": "只读用户",
                "description": "只读用户，只能查看内容",
                "level": 30,
                "max_api_keys": 1,
                "max_agents": 3
            }
        }

        for role_code, config in role_configs.items():
            await self.create_role(
                name=role_code,
                code=role_code,
                display_name=config["display_name"],
                description=config["description"],
                level=config["level"],
                is_system=True,
                max_api_keys=config["max_api_keys"],
                max_agents=config["max_agents"],
                permission_codes=self._default_permissions.get(role_code, [])
            )

        logger.info("Default roles initialized")

    async def cleanup_expired_assignments(self):
        """清理过期的角色分配"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(UserRoleAssignment).where(
                    and_(
                        UserRoleAssignment.is_active == True,
                        UserRoleAssignment.expires_at < datetime.utcnow()
                    )
                )
            )
            expired = result.scalars().all()

            for assignment in expired:
                assignment.is_active = False

            if expired:
                await session.commit()
                logger.info(f"Cleaned up {len(expired)} expired role assignments")


# 创建全局RBAC服务实例
rbac_service = RBACService()