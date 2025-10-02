#!/usr/bin/env python3
"""
简单的模型测试脚本
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agentpedia.models.mongodb_models import (
    AgentModel, MultilingualText, MultilingualDescription, AgentStatus
)
from datetime import datetime

def test_agent_model():
    """测试Agent模型"""
    print("Testing Agent Model Creation...")
    
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
    
    print("All tests passed!")
    print(f"Agent created at: {agent.created_at}")
    print(f"Agent name (zh): {agent.name.zh}")
    print(f"Agent name (en): {agent.name.en}")

if __name__ == "__main__":
    test_agent_model()