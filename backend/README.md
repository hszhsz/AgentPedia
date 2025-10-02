# AgentPedia Backend

AgentPedia - AI Agent Management Platform Backend

## 开发环境设置

### 使用 uv 管理依赖

1. 安装依赖：
```bash
uv sync
```

2. 运行开发服务器：
```bash
uv run src/agentpedia/main.py
```

3. 初始化示例数据：
```bash
uv run scripts/init_sample_data.py
```

3. 运行测试：
```bash
uv run pytest
```

### 使用本地虚拟环境(.venv)运行测试

如果你使用的是 `.venv` 虚拟环境（如本仓库的启动脚本创建）：

1. 激活虚拟环境：
```bash
source .venv/bin/activate
```

2. 安装依赖（若虚拟环境没有 pip，可用 `python -m ensurepip --upgrade` 安装）：
```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

3. 运行测试（确保 `src` 在 Python 路径中）：
```bash
PYTHONPATH=./src pytest -q
```

## 项目结构

- `src/agentpedia/` - 主要应用代码
- `tests/` - 测试代码
- `alembic/` - 数据库迁移文件
- `scripts/` - 数据初始化脚本

## 环境变量

复制 `.env.example` 到 `.env` 并配置相应的环境变量。