#!/bin/bash

# AgentPedia 统一启动脚本
# 用法: ./bootstrap.sh [dev|prod|test]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 未安装，请先安装 $1"
        exit 1
    fi
}

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        log_warning "端口 $port 已被占用"
        return 1
    fi
    return 0
}

# 等待服务启动
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1

    log_info "等待 $service_name 启动..."

    while [ $attempt -le $max_attempts ]; do
        # 尝试连接服务并检查HTTP状态码
        response=$(curl -s -w "%{http_code}" -o /dev/null "$url" 2>/dev/null)
        curl_exit_code=$?

        if [ $curl_exit_code -eq 0 ] && [ "$response" = "200" ]; then
            log_success "$service_name 启动成功"
            return 0
        fi

        echo -n "."
        if [ $attempt -eq 1 ]; then
            echo ""
            log_info "正在检查 $service_name (URL: $url)..."
        fi

        sleep 2
        attempt=$((attempt + 1))
    done

    echo ""
    log_error "$service_name 启动失败 (尝试了 $max_attempts 次)"
    if [ $curl_exit_code -ne 0 ]; then
        log_error "连接错误: curl 退出码 $curl_exit_code"
    else
        log_error "HTTP错误: 状态码 $response"
    fi
    return 1
}

# 创建必要的目录
setup_directories() {
    log_info "创建必要的目录..."
    mkdir -p logs
    mkdir -p backend/logs
    mkdir -p frontend/logs
    log_success "目录创建完成"
}

# 安装依赖
install_dependencies() {
    log_info "检查并安装依赖..."

    # 检查必要的命令
    check_command "uv"
    check_command "node"
    check_command "npm"

    # 安装后端依赖
    if [ -f "backend/pyproject.toml" ]; then
        log_info "安装后端依赖..."
        cd backend && uv sync && cd ..
        log_success "后端依赖安装完成"
    else
        log_warning "未找到 backend/pyproject.toml，跳过后端依赖安装"
    fi

    # 安装前端依赖
    if [ -f "frontend/package.json" ]; then
        log_info "安装前端依赖..."
        cd frontend && npm install && cd ..
        log_success "前端依赖安装完成"
    else
        log_warning "未找到 frontend/package.json，跳过前端依赖安装"
    fi
}

# 运行测试
run_tests() {
    log_info "运行测试..."
    
    # 后端测试
    if [ -f "backend/pyproject.toml" ]; then
        log_info "运行后端测试..."
        cd backend && uv run pytest -v && cd ..
        log_success "后端测试通过"
    fi
    
    # 前端测试
    if [ -f "frontend/package.json" ]; then
        log_info "运行前端测试..."
        cd frontend && npm test -- --watchAll=false && cd ..
        log_success "前端测试通过"
    fi
}

# 清理现有的AgentPedia容器
cleanup_existing_containers() {
    log_info "🧹 检查并清理现有的AgentPedia容器..."

    local containers=("agentpedia-postgres" "agentpedia-redis" "agentpedia-mongodb" "agentpedia-elasticsearch")
    local containers_removed=false

    for container in "${containers[@]}"; do
        if docker ps -a --format "table {{.Names}}" | grep -q "^${container}$"; then
            log_info "发现现有容器 $container，正在清理..."
            if docker ps --format "table {{.Names}}" | grep -q "^${container}$"; then
                docker stop "$container" >/dev/null 2>&1 || log_warning "无法停止容器 $container"
            fi
            docker rm "$container" >/dev/null 2>&1 || log_warning "无法删除容器 $container"
            containers_removed=true
        fi
    done

    if [ "$containers_removed" = true ]; then
        log_success "现有容器清理完成"
    else
        log_info "未发现冲突的容器"
    fi
}

# 启动Docker依赖服务
start_docker_services() {
    log_info "🐳 启动Docker依赖服务..."

    # 检查Docker是否运行
    if ! command -v docker &> /dev/null; then
        log_warning "Docker未安装，使用本地服务..."
        start_local_services
        return
    fi

    if ! docker info > /dev/null 2>&1; then
        log_warning "Docker未运行，使用本地服务..."
        start_local_services
        return
    fi

    # 清理可能冲突的现有容器
    cleanup_existing_containers

    # 启动基础服务
    log_info "启动PostgreSQL、Redis、MongoDB、Elasticsearch..."
    docker compose up -d postgres redis mongodb elasticsearch

    # 等待服务健康检查通过
    log_info "等待服务启动..."
    sleep 15

    # 检查服务状态
    for service in postgres redis mongodb elasticsearch; do
        if docker compose ps $service | grep -q "Up (healthy)"; then
            log_success "$service 服务启动成功"
        else
            log_warning "$service 服务可能还在启动中"
        fi
    done

    log_success "Docker依赖服务启动完成"
}

# 启动本地服务（作为Docker的备选方案）
start_local_services() {
    log_info "🔧 启动本地服务..."

    # 检查并启动数据库服务
    if command -v brew &> /dev/null; then
        log_info "检查数据库服务..."
        if ! brew services list | grep postgresql | grep started > /dev/null; then
            log_info "启动PostgreSQL服务..."
            brew services start postgresql@14
            sleep 3
        fi
        log_success "PostgreSQL服务运行中"

        # 检查并启动Redis服务
        log_info "检查Redis服务..."
        if ! brew services list | grep redis | grep started > /dev/null; then
            log_info "启动Redis服务..."
            brew services start redis
            sleep 2
        fi
        log_success "Redis服务运行中"
    else
        log_warning "Homebrew未安装，请手动启动PostgreSQL和Redis服务"
    fi

    log_success "本地服务启动完成"
}

# 停止Docker依赖服务
stop_docker_services() {
    log_info "🐳 停止Docker依赖服务..."

    if command -v docker &> /dev/null && docker info > /dev/null 2>&1; then
        docker compose down
        log_success "Docker依赖服务已停止"
    else
        log_info "停止本地服务..."
        if command -v brew &> /dev/null; then
            brew services stop postgresql@14 2>/dev/null || true
            brew services stop redis 2>/dev/null || true
            log_success "本地服务已停止"
        fi
    fi
}

# 启动开发环境
start_dev() {
    log_info "🚀 启动开发环境..."

    setup_directories
    install_dependencies

    # 检查端口
    if ! check_port 8000; then
        log_error "后端端口 8000 被占用，请释放端口后重试"
        exit 1
    fi

    # 检查常用的前端端口
    FRONTEND_PORT_CHECK=true
    for port in 5173 3000 3001 3002; do
        if check_port $port; then
            FRONTEND_PORT_CHECK=false
            break
        fi
    done

    if [ "$FRONTEND_PORT_CHECK" = true ]; then
        log_warning "常用前端端口 (3000, 3001, 3002, 5173) 都被占用，前端服务可能会自动选择其他端口"
    fi

    # 启动Docker依赖服务
    start_docker_services

    # 等待数据库完全启动
    log_info "等待数据库完全启动..."
    sleep 15

    # 运行数据库迁移
    log_info "运行数据库迁移..."
    cd backend && uv run alembic upgrade head && cd ..
    log_success "数据库迁移完成"
    
    # 启动后端服务
    if [ -f "backend/src/agentpedia/main.py" ]; then
        log_info "启动后端服务..."
        # 确保logs目录存在
        mkdir -p logs

        # 先停止可能存在的旧进程
        if [ -f "logs/backend.pid" ]; then
            OLD_PID=$(cat logs/backend.pid)
            if ps -p $OLD_PID > /dev/null 2>&1; then
                kill $OLD_PID 2>/dev/null || true
                sleep 2
            fi
        fi

        # 清理占用8000端口的进程
        log_info "清理占用后端端口的进程..."
        PORT_PIDS=$(lsof -ti :8000 2>/dev/null || true)
        if [ -n "$PORT_PIDS" ]; then
            echo $PORT_PIDS | xargs kill -9 2>/dev/null || true
            sleep 2
        fi

        # 启动后端服务并获取PID
        cd backend
        nohup uv run python src/agentpedia/main.py > ../logs/backend.log 2>&1 &
        cd ..

        # 等待进程启动并获取正确的PID
        sleep 2
        BACKEND_PID=$(pgrep -f "uv run python src/agentpedia/main.py" | head -1)

        if [ -n "$BACKEND_PID" ]; then
            echo $BACKEND_PID > logs/backend.pid
            if [ $? -eq 0 ]; then
                log_success "后端服务启动中 (PID: $BACKEND_PID)"
            else
                log_error "无法写入后端PID文件"
                exit 1
            fi
        else
            log_error "无法获取后端服务PID"
            exit 1
        fi
        
        # 等待后端服务启动
        wait_for_service "http://localhost:8000/health" "后端服务"
    else
        log_warning "未找到 backend/src/agentpedia/main.py，跳过后端服务启动"
    fi
    
    # 启动前端服务
    if [ -f "frontend/package.json" ]; then
        log_info "启动前端服务..."
        cd frontend && nohup npm run dev > ../logs/frontend.log 2>&1 &
        FRONTEND_PID=$!
        cd ..

        # 确保logs目录存在并写入PID文件
        mkdir -p logs
        echo $FRONTEND_PID > logs/frontend.pid
        if [ $? -eq 0 ]; then
            log_success "前端服务启动中 (PID: $FRONTEND_PID)"
        else
            log_error "无法写入前端PID文件"
            exit 1
        fi
        
        # 等待前端服务启动
        # 等待一下让前端服务确定使用的端口
        sleep 3
        # 从日志中获取实际使用的端口
        FRONTEND_PORT=$(grep -o "Local:.*http://localhost:[0-9]*" ../logs/frontend.log | head -1 | grep -o "[0-9]*" || echo "5173")
        if [ -z "$FRONTEND_PORT" ]; then
            FRONTEND_PORT=5173
        fi
        log_info "前端服务运行在端口: $FRONTEND_PORT"
        wait_for_service "http://localhost:$FRONTEND_PORT" "前端服务"
    else
        log_warning "未找到 frontend/package.json，跳过前端服务启动"
    fi
    
    # 获取实际的前端端口
    FRONTEND_ACTUAL_PORT=""
    MAX_WAIT=20
    WAIT_COUNT=0

    log_info "检测前端服务端口..."
    while [ $WAIT_COUNT -lt $MAX_WAIT ] && [ -z "$FRONTEND_ACTUAL_PORT" ]; do
        sleep 1
        # 检查多种可能的端口格式 (Next.js, Vite等)
        FRONTEND_ACTUAL_PORT=$(grep -a "Local:" logs/frontend.log 2>/dev/null | grep -o "http://localhost:[0-9]*" | head -1 | grep -o "[0-9]*" || \
                             grep -a "using available port" logs/frontend.log 2>/dev/null | grep -o "using available port [0-9]*" | head -1 | grep -o "[0-9]*" || \
                             grep -a "ready in" logs/frontend.log 2>/dev/null | grep -o "http://localhost:[0-9]*" | head -1 | grep -o "[0-9]*" || \
                             echo "")
        WAIT_COUNT=$((WAIT_COUNT + 1))
    done

    if [ -z "$FRONTEND_ACTUAL_PORT" ]; then
        # 如果从日志中找不到端口，尝试常用的前端端口
        for port in 3000 3001 3002 3003 5173 5174; do
            if curl -s -w "%{http_code}" -o /dev/null "http://localhost:$port" 2>/dev/null | grep -q "200"; then
                FRONTEND_ACTUAL_PORT=$port
                log_info "通过检测发现前端运行在端口: $FRONTEND_ACTUAL_PORT"
                break
            fi
        done
    fi

    if [ -z "$FRONTEND_ACTUAL_PORT" ]; then
        FRONTEND_ACTUAL_PORT=5173
        log_warning "无法确定前端端口，使用默认端口: $FRONTEND_ACTUAL_PORT"
    else
        log_success "检测到前端端口: $FRONTEND_ACTUAL_PORT"
    fi

    # 验证两个服务都正常响应
    log_info "🔍 验证服务状态..."

    # 检查后端服务
    BACKEND_STATUS=$(curl -s -w "%{http_code}" -o /dev/null "http://localhost:8000/health" 2>/dev/null || echo "000")
    # 检查前端服务
    FRONTEND_STATUS=$(curl -s -w "%{http_code}" -o /dev/null "http://localhost:$FRONTEND_ACTUAL_PORT" 2>/dev/null || echo "000")

    if [ "$BACKEND_STATUS" = "200" ] && [ "$FRONTEND_STATUS" = "200" ]; then
        # 优雅的成功通知
        echo ""
        echo -e "${GREEN}🎉 启动成功！${NC}"
        echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║${NC}                           🚀 AgentPedia 启动成功！                           ${GREEN}║${NC}"
        echo -e "${GREEN}║${NC}                    前端:${FRONTEND_ACTUAL_PORT}  |  后端:8000                    ${GREEN}║${NC}"
        echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "📱 ${BLUE}前端服务${NC}:   ${YELLOW}http://localhost:$FRONTEND_ACTUAL_PORT${NC}"
        echo -e "🔧 ${BLUE}后端服务${NC}:   ${YELLOW}http://localhost:8000${NC}"
        echo -e "📋 ${BLUE}API 文档${NC}:  ${YELLOW}http://localhost:8000/api/v1/docs${NC}"
        echo ""
        echo -e "${GREEN}✨ 所有服务已成功启动并运行在指定端口上！${NC}"
        echo ""
        echo -e "📝 ${BLUE}日志文件${NC}:"
        echo -e "   ${GRAY}•${NC} 后端: logs/backend.log"
        echo -e "   ${GRAY}•${NC} 前端: logs/frontend.log"
        echo ""
        echo -e "🛑 ${BLUE}停止服务${NC}: ${YELLOW}./bootstrap.sh stop${NC}"
        echo ""
    else
        echo ""
        log_warning "服务启动可能存在问题，请检查日志："
        echo -e "   ${GRAY}•${NC} 后端状态码: $BACKEND_STATUS"
        echo -e "   ${GRAY}•${NC} 前端状态码: $FRONTEND_STATUS"
        echo ""
        echo -e "📝 ${BLUE}日志文件${NC}:"
        echo -e "   ${GRAY}•${NC} 后端: logs/backend.log"
        echo -e "   ${GRAY}•${NC} 前端: logs/frontend.log"
        echo ""
    fi
}

# 启动生产环境
start_prod() {
    log_info "🚀 启动生产环境..."
    
    setup_directories
    install_dependencies
    run_tests
    
    # 构建前端
    if [ -f "frontend/package.json" ]; then
        log_info "构建前端应用..."
        cd frontend && npm run build && cd ..
        log_success "前端构建完成"
        
        log_info "启动生产服务..."
        cd frontend && nohup npm start > logs/production.log 2>&1 &
        PROD_PID=$!
        cd ..

        # 确保logs目录存在并写入PID文件
        mkdir -p logs
        echo $PROD_PID > logs/production.pid
        if [ $? -eq 0 ]; then
            log_success "生产服务启动中 (PID: $PROD_PID)"
        else
            log_error "无法写入生产PID文件"
            exit 1
        fi
  
        wait_for_service "http://localhost:3000" "生产服务"

        # 验证生产服务
        PROD_STATUS=$(curl -s -w "%{http_code}" -o /dev/null "http://localhost:3000" 2>/dev/null || echo "000")

        if [ "$PROD_STATUS" = "200" ]; then
            echo ""
            echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
            echo -e "${GREEN}║${NC}                      🌟 生产环境启动成功！                            ${GREEN}║${NC}"
            echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
            echo ""
            echo -e "${BLUE}🌐 应用地址${NC}:   ${YELLOW}http://localhost:3000${NC}"
            echo -e "${BLUE}📝 日志文件${NC}:   ${YELLOW}logs/production.log${NC}"
            echo ""
            echo -e "${GREEN}✨ 生产环境已成功部署并运行！${NC}"
            echo ""
        else
            echo ""
            log_warning "生产环境启动可能存在问题，状态码: $PROD_STATUS"
            echo -e "📝 ${BLUE}日志文件${NC}: logs/production.log"
            echo ""
        fi
    else
        log_warning "未找到前端构建文件，跳过生产服务启动"
    fi
}

# 运行测试环境
start_test() {
    log_info "🧪 运行测试环境..."
    
    setup_directories
    install_dependencies
    run_tests
    
    log_success "✅ 所有测试通过！"
}

# 停止服务
stop_services() {
    log_info "🛑 停止所有服务..."

    # 停止后端服务
    if [ -f "logs/backend.pid" ]; then
        BACKEND_PID=$(cat logs/backend.pid)
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill $BACKEND_PID
            log_success "后端服务已停止 (PID: $BACKEND_PID)"
        else
            log_warning "后端进程 $BACKEND_PID 不存在，清理陈旧的PID文件"
        fi
        rm -f logs/backend.pid
    fi

    # 停止前端服务
    if [ -f "logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill $FRONTEND_PID
            log_success "前端服务已停止 (PID: $FRONTEND_PID)"
        else
            log_warning "前端进程 $FRONTEND_PID 不存在，清理陈旧的PID文件"
        fi
        rm -f logs/frontend.pid
    fi

    # 停止生产服务
    if [ -f "logs/production.pid" ]; then
        PROD_PID=$(cat logs/production.pid)
        if kill -0 $PROD_PID 2>/dev/null; then
            kill $PROD_PID
            log_success "生产服务已停止 (PID: $PROD_PID)"
        else
            log_warning "生产进程 $PROD_PID 不存在，清理陈旧的PID文件"
        fi
        rm -f logs/production.pid
    fi

    # 停止Docker依赖服务
    stop_docker_services

    log_success "✅ 所有服务已停止"
}

# 显示帮助信息
show_help() {
    echo "AgentPedia 启动脚本"
    echo ""
    echo "用法:"
    echo "  ./bootstrap.sh [命令]"
    echo ""
    echo "命令:"
    echo "  dev     启动开发环境 (默认)"
    echo "  prod    启动生产环境"
    echo "  test    运行测试"
    echo "  stop    停止所有服务"
    echo "  help    显示帮助信息"
    echo ""
    echo "示例:"
    echo "  ./bootstrap.sh dev     # 启动开发环境"
    echo "  ./bootstrap.sh prod    # 启动生产环境"
    echo "  ./bootstrap.sh test    # 运行测试"
    echo "  ./bootstrap.sh stop    # 停止服务"
}

# 主函数
main() {
    local command=${1:-dev}
    
    case $command in
        "dev")
            start_dev
            ;;
        "prod")
            start_prod
            ;;
        "test")
            start_test
            ;;
        "stop")
            stop_services
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "未知命令: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 捕获 Ctrl+C 信号
trap 'log_info "收到中断信号，正在停止服务..."; stop_services; exit 0' INT

# 执行主函数
main "$@"