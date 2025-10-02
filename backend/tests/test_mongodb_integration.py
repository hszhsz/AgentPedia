"""
MongoDB集成测试
"""
import pytest
from datetime import datetime
from agentpedia.models.mongodb_models import (
    AgentModel, MultilingualText, MultilingualDescription, AgentStatus
)

def test_agent_model_creation():
    """测试Agent模型创建"""
    # 创建Agent模型实例
    agent = AgentModel(
        name=MultilingualText(
            zh="测试Agent",
            en="Test Agent"
        ),
        slug="test-agent",
        official_url="https://test-agent.com",
        description=MultilingualDescription(
            short=MultilingualText(
                zh="测试用Agent",
                en="Test Agent for testing"
            )
        ),
        status=AgentStatus.CONCEPT
    )
    
    # 验证模型创建成功
    assert agent.name.zh == "测试Agent"
    assert agent.name.en == "Test Agent"
    assert agent.slug == "test-agent"
    assert agent.official_url == "https://test-agent.com"
    assert agent.status == AgentStatus.CONCEPT
    
    # 验证时间戳已设置
    assert isinstance(agent.created_at, datetime)
    assert isinstance(agent.updated_at, datetime)

if __name__ == "__main__":
    test_agent_model_creation()
    print("All tests passed!")