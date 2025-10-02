"""
RBAC相关的Pydantic模式
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from agentpedia.models.permission import PermissionResource, PermissionAction
from agentpedia.schemas.base import BaseSchema, IDSchema, TimestampSchema


class PermissionBase(BaseSchema):
    """权限基础模式"""
    name: str = Field(..., description="权限名称", max_length=100)
    code: str = Field(..., description="权限代码", max_length=100)
    resource: str = Field(..., description="资源")
    action: str = Field(..., description="动作")
    description: Optional[str] = Field(None, description="权限描述")
    is_system: bool = Field(False, description="是否为系统权限")


class PermissionCreate(PermissionBase):
    """创建权限模式"""
    pass


class PermissionUpdate(BaseSchema):
    """更新权限模式"""
    name: Optional[str] = Field(None, description="权限名称", max_length=100)
    description: Optional[str] = Field(None, description="权限描述")


class PermissionResponse(PermissionBase, IDSchema, TimestampSchema):
    """权限响应模式"""
    pass


class RoleBase(BaseSchema):
    """角色基础模式"""
    name: str = Field(..., description="角色名称", max_length=50)
    code: str = Field(..., description="角色代码", max_length=50)
    display_name: str = Field(..., description="显示名称", max_length=100)
    description: Optional[str] = Field(None, description="角色描述")
    level: int = Field(0, description="角色级别")
    is_system: bool = Field(False, description="是否为系统角色")
    is_active: bool = Field(True, description="是否启用")
    max_api_keys: int = Field(5, description="最大API密钥数量")
    max_agents: int = Field(10, description="最大Agent数量")


class RoleCreate(RoleBase):
    """创建角色模式"""
    permission_codes: Optional[List[str]] = Field(None, description="权限代码列表")


class RoleUpdate(BaseSchema):
    """更新角色模式"""
    name: Optional[str] = Field(None, description="角色名称", max_length=50)
    display_name: Optional[str] = Field(None, description="显示名称", max_length=100)
    description: Optional[str] = Field(None, description="角色描述")
    level: Optional[int] = Field(None, description="角色级别")
    is_active: Optional[bool] = Field(None, description="是否启用")
    max_api_keys: Optional[int] = Field(None, description="最大API密钥数量")
    max_agents: Optional[int] = Field(None, description="最大Agent数量")


class RoleResponse(RoleBase, IDSchema, TimestampSchema):
    """角色响应模式"""
    permissions: List[PermissionResponse] = Field(default_factory=list, description="权限列表")


class RoleWithPermissions(RoleResponse):
    """包含详细权限信息的角色模式"""
    pass


class UserRoleAssignmentBase(BaseSchema):
    """用户角色分配基础模式"""
    user_id: int = Field(..., description="用户ID")
    role_id: int = Field(..., description="角色ID")
    expires_at: Optional[datetime] = Field(None, description="过期时间")
    reason: Optional[str] = Field(None, description="授权原因")


class UserRoleAssignmentCreate(UserRoleAssignmentBase):
    """创建用户角色分配模式"""
    granted_by: Optional[int] = Field(None, description="授权人ID")


class UserRoleAssignmentUpdate(BaseSchema):
    """更新用户角色分配模式"""
    expires_at: Optional[datetime] = Field(None, description="过期时间")
    is_active: Optional[bool] = Field(None, description="是否有效")
    reason: Optional[str] = Field(None, description="授权原因")


class UserRoleAssignmentResponse(UserRoleAssignmentBase, IDSchema, TimestampSchema):
    """用户角色分配响应模式"""
    granted_by: Optional[int] = Field(None, description="授权人ID")
    granted_at: datetime = Field(..., description="授权时间")
    is_active: bool = Field(True, description="是否有效")


class UserRoleAssignmentWithDetails(UserRoleAssignmentResponse):
    """包含详细信息的用户角色分配模式"""
    user: Optional[dict] = Field(None, description="用户信息")
    role: Optional[RoleResponse] = Field(None, description="角色信息")
    granter: Optional[dict] = Field(None, description="授权人信息")


class UserPermissionCheck(BaseSchema):
    """用户权限检查模式"""
    resource: str = Field(..., description="资源")
    action: str = Field(..., description="动作")


class UserPermissionCheckRequest(UserPermissionCheck):
    """用户权限检查请求模式"""
    user_id: int = Field(..., description="用户ID")


class UserPermissionCheckResponse(BaseSchema):
    """用户权限检查响应模式"""
    has_permission: bool = Field(..., description="是否有权限")
    user_id: int = Field(..., description="用户ID")
    resource: str = Field(..., description="资源")
    action: str = Field(..., description="动作")
    permissions: List[str] = Field(default_factory=list, description="用户拥有的权限列表")


class UserRoleGrant(BaseSchema):
    """用户角色授权模式"""
    role_code: str = Field(..., description="角色代码")
    user_id: int = Field(..., description="用户ID")
    expires_at: Optional[datetime] = Field(None, description="过期时间")
    reason: Optional[str] = Field(None, description="授权原因")


class UserRoleRevoke(BaseSchema):
    """用户角色撤销模式"""
    role_code: str = Field(..., description="角色代码")
    user_id: int = Field(..., description="用户ID")


class UserPermissionsResponse(BaseSchema):
    """用户权限列表响应模式"""
    user_id: int = Field(..., description="用户ID")
    permissions: List[str] = Field(..., description="权限列表")
    roles: List[RoleResponse] = Field(default_factory=list, description="角色列表")


class UserRoleHierarchy(BaseSchema):
    """用户角色层级模式"""
    user_id: int = Field(..., description="用户ID")
    highest_role: Optional[RoleResponse] = Field(None, description="最高级别角色")
    all_roles: List[RoleResponse] = Field(default_factory=list, description="所有角色")
    effective_permissions: List[str] = Field(default_factory=list, description="有效权限")


class SystemRoleStats(BaseSchema):
    """系统角色统计模式"""
    total_roles: int = Field(..., description="总角色数")
    active_roles: int = Field(..., description="活跃角色数")
    total_permissions: int = Field(..., description="总权限数")
    system_roles: int = Field(..., description="系统角色数")
    custom_roles: int = Field(..., description="自定义角色数")


class PermissionGroup(BaseSchema):
    """权限分组模式"""
    resource: str = Field(..., description="资源")
    permissions: List[PermissionResponse] = Field(..., description="权限列表")


class RoleManagementStats(BaseSchema):
    """角色管理统计模式"""
    role_code: str = Field(..., description="角色代码")
    role_name: str = Field(..., description="角色名称")
    user_count: int = Field(..., description="用户数量")
    permission_count: int = Field(..., description="权限数量")
    created_at: datetime = Field(..., description="创建时间")
    last_assigned: Optional[datetime] = Field(None, description="最后分配时间")