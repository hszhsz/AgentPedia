import sys
from pathlib import Path
import pytest

# 允许直接从src导入而不安装包
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

try:
    # 导入待测端点与依赖的schemas
    from agentpedia.api.v1 import agents as agents_api
    from agentpedia.schemas.base import PaginationParams
    from agentpedia.schemas.agent import (
        AgentFilterParams,
        AgentCreate,
        AgentUpdate,
        AgentChat,
        AgentResponse,
        AgentDetail,
        AgentChatResponse,
    )
    from agentpedia.models.user import User
    from agentpedia.models.agent import AgentVisibility, ModelProvider, AgentStatus
except Exception:
    pytest.skip("后端依赖未安装或模型不可用，跳过 agents 接口测试", allow_module_level=True)


class DummyAgentService:
    """用于端点测试的轻量级AgentService Stub"""

    def __init__(self):
        # 使用内存数据模拟
        self._agents = {}
        self._next_id = 1

    async def get_agents_with_filters(self, pagination, filters, user_id):
        items = list(self._agents.values())
        total = len(items)
        start = pagination.offset
        end = start + pagination.size
        return items[start:end], total

    async def create_agent(self, agent_data: AgentCreate, user_id: int):
        aid = self._next_id
        self._next_id += 1
        agent = {
            "id": aid,
            "name": agent_data.name,
            "description": agent_data.description,
            "type": agent_data.type,
            "visibility": agent_data.visibility,
            "model_provider": agent_data.model_provider,
            "model_name": agent_data.model_name,
            "model_version": agent_data.model_version,
            "system_prompt": agent_data.system_prompt,
            "temperature": agent_data.temperature,
            "max_tokens": agent_data.max_tokens,
            "top_p": agent_data.top_p,
            "frequency_penalty": agent_data.frequency_penalty,
            "presence_penalty": agent_data.presence_penalty,
            "enable_memory": agent_data.enable_memory,
            "enable_tools": agent_data.enable_tools,
            "enable_web_search": agent_data.enable_web_search,
            # 端点响应附加字段
            "status": AgentStatus.DRAFT,
            "owner_id": user_id,
            "usage_count": 0,
            "total_tokens_used": 0,
            "average_response_time": 0.0,
            "success_rate": 0.0,
        }
        self._agents[aid] = agent
        return agent

    async def get_user_agents(self, user_id, pagination, filters):
        items = [a for a in self._agents.values() if a["owner_id"] == user_id]
        total = len(items)
        start = pagination.offset
        end = start + pagination.size
        return items[start:end], total

    async def get_with_tools(self, agent_id: int):
        return self._agents.get(agent_id)

    async def update_agent(self, agent_id: int, agent_data: AgentUpdate, user_id: int):
        if agent_id not in self._agents:
            return None
        agent = self._agents[agent_id]
        for k, v in agent_data.model_dump(exclude_unset=True).items():
            agent[k] = v
        return agent

    async def delete_agent(self, agent_id: int, user_id: int) -> bool:
        return self._agents.pop(agent_id, None) is not None


def make_user(user_id: int = 1) -> User:
    # 构造一个最小可用的User对象（直接实例化模型）
    u = User(
        id=user_id,
        username="mock_user",
        email="mock@example.com",
    )
    # 确保端点中的属性访问存在
    u.is_active = True
    return u


@pytest.mark.asyncio
async def test_list_agents_returns_paginated_response():
    pagination = PaginationParams(page=1, size=10)
    filters = AgentFilterParams()
    current_user = None  # 公共列表允许可选用户
    agent_service = DummyAgentService()

    # 预填充两条数据
    await agent_service.create_agent(
        AgentCreate(
            name="A1",
            description="desc",
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-3.5-turbo",
            visibility=AgentVisibility.PUBLIC,
        ),
        user_id=1,
    )
    await agent_service.create_agent(
        AgentCreate(
            name="A2",
            description="desc",
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-3.5-turbo",
            visibility=AgentVisibility.PRIVATE,
        ),
        user_id=2,
    )

    resp = await agents_api.list_agents(
        pagination=pagination,
        filters=filters,
        current_user=current_user,
        agent_service=agent_service,
    )

    assert resp.items and resp.total == 2
    assert resp.page == 1 and resp.size == 10


@pytest.mark.asyncio
async def test_create_and_get_my_agents_flow():
    current_user = make_user(10)
    agent_service = DummyAgentService()
    pagination = PaginationParams(page=1, size=5)
    filters = AgentFilterParams()

    create_data = AgentCreate(
        name="MyAgent",
        description="mine",
        model_provider=ModelProvider.OPENAI,
        model_name="gpt-4o-mini",
        visibility=AgentVisibility.PRIVATE,
    )

    create_resp = await agents_api.create_agent(
        agent_data=create_data,
        current_user=current_user,
        agent_service=agent_service,
    )
    assert create_resp.success is True
    created = create_resp.data
    assert isinstance(created, AgentResponse)
    assert created.name == "MyAgent"
    assert created.owner_id == 10

    my_list = await agents_api.list_my_agents(
        pagination=pagination,
        filters=filters,
        current_user=current_user,
        agent_service=agent_service,
    )
    assert my_list.total == 1
    assert my_list.items[0].name == "MyAgent"


@pytest.mark.asyncio
async def test_get_update_delete_agent():
    current_user = make_user(5)
    agent_service = DummyAgentService()

    # 创建一条
    create_resp = await agents_api.create_agent(
        agent_data=AgentCreate(
            name="AgentX",
            description="x",
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-3.5-turbo",
            visibility=AgentVisibility.PRIVATE,
        ),
        current_user=current_user,
        agent_service=agent_service,
    )
    agent_id = create_resp.data.id

    # 获取详情（包含工具）
    detail_resp = await agents_api.get_agent(
        agent_id=agent_id,
        current_user=current_user,
        agent_service=agent_service,
    )
    assert detail_resp.success is True
    detail = detail_resp.data
    assert isinstance(detail, AgentDetail)
    assert detail.id == agent_id

    # 更新
    update_resp = await agents_api.update_agent(
        agent_id=agent_id,
        agent_data=AgentUpdate(description="updated"),
        current_user=current_user,
        agent_service=agent_service,
    )
    assert update_resp.success is True
    assert update_resp.data.description == "updated"

    # 删除
    del_resp = await agents_api.delete_agent(
        agent_id=agent_id,
        current_user=current_user,
        agent_service=agent_service,
    )
    assert del_resp.success is True


@pytest.mark.asyncio
async def test_chat_with_agent_returns_mock_response():
    current_user = make_user(7)
    agent_service = DummyAgentService()

    # 准备一个Agent
    created = await agents_api.create_agent(
        agent_data=AgentCreate(
            name="ChatAgent",
            description="chat",
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-4o-mini",
            visibility=AgentVisibility.PRIVATE,
        ),
        current_user=current_user,
        agent_service=agent_service,
    )
    agent_id = created.data.id

    # 调用聊天
    chat_resp = await agents_api.chat_with_agent(
        agent_id=agent_id,
        chat_data=AgentChat(message="Hello"),
        current_user=current_user,
        agent_service=agent_service,
    )
    assert chat_resp.success is True
    assert isinstance(chat_resp.data, AgentChatResponse)
    assert chat_resp.data.message