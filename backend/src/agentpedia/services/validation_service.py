"""
数据验证服务
确保Agent信息的质量和完整性
"""
import re
from typing import Dict, Any, List
from urllib.parse import urlparse
import logging
import httpx
from agentpedia.core.logging import get_logger

logger = get_logger(__name__)


class ValidationService:
    """数据验证服务"""
    
    def __init__(self):
        pass
    
    async def validate_agent_data(self, agent_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """验证Agent数据"""
        errors = {}
        
        # 验证基础信息
        basic_errors = await self._validate_basic_info(agent_data)
        if basic_errors:
            errors.update(basic_errors)
        
        # 验证URL
        url_errors = await self._validate_urls(agent_data)
        if url_errors:
            errors.update(url_errors)
        
        # 验证技术栈
        tech_errors = await self._validate_technical_stack(agent_data)
        if tech_errors:
            errors.update(tech_errors)
        
        # 验证商业信息
        business_errors = await self._validate_business_info(agent_data)
        if business_errors:
            errors.update(business_errors)
        
        return errors
    
    async def _validate_basic_info(self, agent_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """验证基础信息"""
        errors = {}
        
        # 验证名称
        name = agent_data.get("name", {})
        if not name or (not name.get("zh") and not name.get("en")):
            errors.setdefault("name", []).append("至少需要提供中文或英文名称")
        
        # 验证slug
        slug = agent_data.get("slug")
        if not slug:
            errors.setdefault("slug", []).append("slug不能为空")
        elif not re.match("^[a-z0-9\\-]+$", slug):
            errors.setdefault("slug", []).append("slug只能包含小写字母、数字和连字符")
        
        # 验证描述
        description = agent_data.get("description", {})
        short_desc = description.get("short", {})
        if not short_desc or (not short_desc.get("zh") and not short_desc.get("en")):
            errors.setdefault("description.short", []).append("至少需要提供中文或英文简短描述")
        
        return errors
    
    async def _validate_urls(self, agent_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """验证URL"""
        errors = {}
        
        # 验证官网URL
        official_url = agent_data.get("official_url")
        if not official_url:
            errors.setdefault("official_url", []).append("官网URL不能为空")
        elif not self._is_valid_url(official_url):
            errors.setdefault("official_url", []).append("官网URL格式不正确")
        
        # 验证Logo URL
        logo_url = agent_data.get("logo_url")
        if logo_url and not self._is_valid_url(logo_url):
            errors.setdefault("logo_url", []).append("Logo URL格式不正确")
        
        return errors
    
    def _is_valid_url(self, url: str) -> bool:
        """验证URL格式"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    async def _validate_technical_stack(self, agent_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """验证技术栈"""
        errors = {}
        
        technical_stack = agent_data.get("technical_stack", {})
        if not technical_stack:
            return errors
        
        # 验证基础模型
        base_models = technical_stack.get("base_model", [])
        if base_models:
            valid_models = [
                "GPT-4", "GPT-3.5", "Claude", "Gemini", "LLaMA", "PaLM", 
                "Mistral", "Qwen", "Baichuan", "ChatGLM", "其他"
            ]
            for model in base_models:
                if model not in valid_models:
                    errors.setdefault("technical_stack.base_model", []).append(f"不支持的基础模型: {model}")
        
        # 验证框架
        frameworks = technical_stack.get("frameworks", [])
        if frameworks:
            valid_frameworks = [
                "LangChain", "LangGraph", "AutoGen", "CrewAI", 
                "Semantic Kernel", "Transformers", "其他"
            ]
            for framework in frameworks:
                if framework not in valid_frameworks:
                    errors.setdefault("technical_stack.frameworks", []).append(f"不支持的框架: {framework}")
        
        return errors
    
    async def _validate_business_info(self, agent_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """验证商业信息"""
        errors = {}
        
        business_info = agent_data.get("business_info", {})
        if not business_info:
            return errors
        
        # 验证融资信息
        funding = business_info.get("funding", [])
        if funding:
            valid_rounds = [
                "种子轮", "天使轮", "Pre-A", "A轮", "B轮", "C轮", 
                "D轮", "战略投资", "IPO", "未披露"
            ]
            for fund in funding:
                round_type = fund.get("round")
                if round_type and round_type not in valid_rounds:
                    errors.setdefault("business_info.funding.round", []).append(f"不支持的融资轮次: {round_type}")
                
                amount = fund.get("amount")
                if amount and not re.match("^[0-9\\.]+[万千亿]?[美元人民币]?$|^未披露$", amount):
                    errors.setdefault("business_info.funding.amount", []).append(f"融资金额格式不正确: {amount}")
        
        return errors
    
    async def check_url_accessibility(self, url: str) -> bool:
        """检查URL可访问性"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.head(url, timeout=10.0)
                return response.status_code < 400
        except Exception as e:
            logger.warning(f"URL accessibility check failed for {url}: {e}")
            return False
    
    def calculate_data_quality_score(self, agent_data: Dict[str, Any]) -> float:
        """计算数据质量评分"""
        total_weight = 0
        score = 0
        
        # 基础信息完整性 (权重40%)
        basic_weight = 40
        basic_score = 0
        if agent_data.get("name"):
            basic_score += 25
        if agent_data.get("description", {}).get("short"):
            basic_score += 25
        if agent_data.get("description", {}).get("detailed"):
            basic_score += 25
        if agent_data.get("official_url"):
            basic_score += 25
        score += (basic_score / 100) * basic_weight
        total_weight += basic_weight
        
        # 技术信息完整性 (权重30%)
        tech_weight = 30
        tech_score = 0
        if agent_data.get("technical_stack"):
            tech_score += 100
        score += (tech_score / 100) * tech_weight
        total_weight += tech_weight
        
        # 商业信息完整性 (权重20%)
        business_weight = 20
        business_score = 0
        if agent_data.get("business_info"):
            business_score += 100
        score += (business_score / 100) * business_weight
        total_weight += business_weight
        
        # 其他信息完整性 (权重10%)
        other_weight = 10
        other_score = 0
        if agent_data.get("development_team"):
            other_score += 50
        if agent_data.get("features"):
            other_score += 50
        score += (other_score / 100) * other_weight
        total_weight += other_weight
        
        return round(score / total_weight * 100, 2) if total_weight > 0 else 0

# 创建全局服务实例
validation_service = ValidationService()