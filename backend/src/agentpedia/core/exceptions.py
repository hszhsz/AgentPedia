"""
自定义异常类
"""


class AgentPediaException(Exception):
    """AgentPedia基础异常类"""
    
    def __init__(self, message: str = "An error occurred", code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundError(AgentPediaException):
    """资源未找到异常"""
    
    def __init__(self, message: str = "Resource not found", code: str = "NOT_FOUND"):
        super().__init__(message, code)


class PermissionError(AgentPediaException):
    """权限不足异常"""
    
    def __init__(self, message: str = "Permission denied", code: str = "PERMISSION_DENIED"):
        super().__init__(message, code)


class ValidationError(AgentPediaException):
    """验证错误异常"""
    
    def __init__(self, message: str = "Validation failed", code: str = "VALIDATION_ERROR"):
        super().__init__(message, code)


class AuthenticationError(AgentPediaException):
    """认证失败异常"""
    
    def __init__(self, message: str = "Authentication failed", code: str = "AUTHENTICATION_ERROR"):
        super().__init__(message, code)


class AuthorizationError(AgentPediaException):
    """授权失败异常"""
    
    def __init__(self, message: str = "Authorization failed", code: str = "AUTHORIZATION_ERROR"):
        super().__init__(message, code)


class ConfigurationError(AgentPediaException):
    """配置错误异常"""
    
    def __init__(self, message: str = "Configuration error", code: str = "CONFIGURATION_ERROR"):
        super().__init__(message, code)


class ExternalServiceError(AgentPediaException):
    """外部服务错误异常"""
    
    def __init__(self, message: str = "External service error", code: str = "EXTERNAL_SERVICE_ERROR"):
        super().__init__(message, code)


class RateLimitError(AgentPediaException):
    """限流异常"""
    
    def __init__(self, message: str = "Rate limit exceeded", code: str = "RATE_LIMIT_ERROR"):
        super().__init__(message, code)


class DatabaseError(AgentPediaException):
    """数据库错误异常"""
    
    def __init__(self, message: str = "Database error", code: str = "DATABASE_ERROR"):
        super().__init__(message, code)


class BusinessLogicError(AgentPediaException):
    """业务逻辑错误异常"""
    
    def __init__(self, message: str = "Business logic error", code: str = "BUSINESS_LOGIC_ERROR"):
        super().__init__(message, code)