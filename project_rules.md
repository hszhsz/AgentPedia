# AgentPedia 项目开发规范

## 1. 依赖管理与启动方式

### 1.1 后端依赖管理
统一使用 `uv` 作为 Python 依赖管理工具
- 使用 `uv add <package>` 添加依赖
- 使用 `uv sync` 同步依赖
- 使用 `uv run <script>` 运行 Python 脚本
- 后端启动命令：`uv run src/main.py` 或相应的启动脚本

### 1.2 前端构建工具
必须使用 `Next.js` 进行前端开发，采用 App Router 架构
- 开发环境启动：`npm run dev`
- 生产环境构建：`npm run build`
- 生产环境启动：`npm start`
- 预览生产构建：`npm run preview`

### 1.3 服务启动统一入口
通过 `bootstrap.sh` 脚本启动前后端服务
- 开发环境启动：`./bootstrap.sh dev`
- 生产环境启动：`./bootstrap.sh prod`
- 脚本需处理前后端服务的依赖检查、启动顺序和日志输出

## 2. 测试规范

### 2.1 单元测试要求
- 所有功能代码必须包含对应的单元测试
- 后端测试使用 `pytest` 框架，存放于 `tests/unit/` 目录
- 前端测试使用 `Jest` 和 `@testing-library/react` 框架，存放于 `src/tests/` 目录
- 测试覆盖率要求达到 80% 以上

### 2.2 测试执行规范
- 每次提交代码前必须运行所有单元测试
- 每次修改代码后必须确保所有单元测试通过
- 后端测试命令：`uv run pytest`
- 前端测试命令：`npm test`

### 2.3 测试自动化
- 配置 Git hooks，在提交前自动运行相关测试
- CI/CD 流程中必须包含测试步骤，测试不通过则阻断构建