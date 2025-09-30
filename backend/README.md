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

3. 运行测试：
```bash
uv run pytest
```

## 项目结构

- `src/agentpedia/` - 主要应用代码
- `tests/` - 测试代码
- `alembic/` - 数据库迁移文件

## 环境变量

复制 `.env.example` 到 `.env` 并配置相应的环境变量。