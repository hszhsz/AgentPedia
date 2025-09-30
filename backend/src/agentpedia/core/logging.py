"""
结构化日志配置
"""
import logging
import sys
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory

from agentpedia.core.config import get_settings

settings = get_settings()


def configure_logging() -> None:
    """配置结构化日志"""
    
    # 配置标准库日志
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # 配置structlog
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    if settings.LOG_FORMAT == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    """获取结构化日志器"""
    return structlog.get_logger(name)


class RequestLoggingMiddleware:
    """请求日志中间件"""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("request")
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request_id = scope.get("request_id", "unknown")
        method = scope["method"]
        path = scope["path"]
        
        # 记录请求开始
        self.logger.info(
            "Request started",
            request_id=request_id,
            method=method,
            path=path,
        )
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                self.logger.info(
                    "Request completed",
                    request_id=request_id,
                    method=method,
                    path=path,
                    status_code=status_code,
                )
            await send(message)
        
        await self.app(scope, receive, send_wrapper)


class PerformanceLoggingMiddleware:
    """性能日志中间件"""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("performance")
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        import time
        start_time = time.time()
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                process_time = time.time() - start_time
                
                # 记录慢请求
                if process_time > 1.0:  # 超过1秒的请求
                    self.logger.warning(
                        "Slow request detected",
                        method=scope["method"],
                        path=scope["path"],
                        process_time=process_time,
                    )
                
                # 添加性能头
                headers = list(message.get("headers", []))
                headers.append((b"x-process-time", str(process_time).encode()))
                message["headers"] = headers
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)


def log_function_call(func_name: str, **kwargs: Any) -> None:
    """记录函数调用"""
    logger = get_logger("function_call")
    logger.info(f"Function called: {func_name}", **kwargs)


def log_error(error: Exception, context: Dict[str, Any] = None) -> None:
    """记录错误"""
    logger = get_logger("error")
    logger.error(
        "Error occurred",
        error_type=type(error).__name__,
        error_message=str(error),
        context=context or {},
        exc_info=True,
    )


def log_security_event(event_type: str, **kwargs: Any) -> None:
    """记录安全事件"""
    logger = get_logger("security")
    logger.warning(f"Security event: {event_type}", **kwargs)


def log_business_event(event_type: str, **kwargs: Any) -> None:
    """记录业务事件"""
    logger = get_logger("business")
    logger.info(f"Business event: {event_type}", **kwargs)