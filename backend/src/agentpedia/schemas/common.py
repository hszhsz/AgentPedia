"""
通用响应Schema
"""
from typing import Any, Optional, List
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """通用API响应模型"""
    success: bool = True
    message: str = "操作成功"
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    code: int = 200

    class Config:
        json_encoders = {
            # 如果需要特殊编码
        }


class PaginatedResponse(BaseModel):
    """分页响应模型"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        json_encoders = {
            # 如果需要特殊编码
        }


class ErrorDetail(BaseModel):
    """错误详情模型"""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = False
    message: str = "操作失败"
    errors: Optional[List[ErrorDetail]] = None
    code: int = 400

    class Config:
        json_encoders = {
            # 如果需要特殊编码
        }


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str
    version: str
    environment: str
    services: Optional[dict] = None

    class Config:
        json_encoders = {
            # 如果需要特殊编码
        }