import sys
from pathlib import Path
import pytest

# 将src加入路径以便无需安装包即可导入
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

try:
    from agentpedia.main import create_app
except Exception:
    pytest.skip("后端依赖未安装，跳过应用健康检查测试", allow_module_level=True)


@pytest.mark.asyncio
async def test_health_endpoint_returns_expected_fields():
    app = create_app()
    # 直接查找并调用路由的处理函数，避免外部HTTP依赖
    health_route = None
    for route in app.routes:
        if getattr(route, "path", None) == "/health":
            health_route = route
            break
    assert health_route is not None
    data = await health_route.endpoint()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data


@pytest.mark.asyncio
async def test_docs_route_registered():
    app = create_app()
    # 验证文档路由已注册，而非实际发HTTP请求
    docs_paths = {r.path for r in app.routes if hasattr(r, "path")}
    assert "/api/v1/docs" in docs_paths