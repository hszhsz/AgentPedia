#!/bin/bash

# AgentPedia 后端启动脚本
# 用法: ./backend-start.sh

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

# 等待服务启动
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1

    log_info "等待 $service_name 启动..."

    while [ $attempt -le $max_attempts ]; do
        if curl -s $url > /dev/null 2>&1; then
            log_success "$service_name 启动成功"
            return 0
        fi

        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done

    log_error "$service_name 启动失败"
    return 1
}

# 创建必要的目录
setup_directories() {
    log_info "创建必要的目录..."
    mkdir -p logs
    mkdir -p uploads
    log_success "目录创建完成"
}

# 启动依赖服务
start_dependencies() {
    log_info "🔧 启动依赖服务..."

    # 检查Docker是否可用
    if command -v docker &> /dev/null && docker info > /dev/null 2>&1; then
        log_info "使用Docker启动依赖服务..."
        cd .. && docker compose up -d postgres redis mongodb elasticsearch
        sleep 15
        cd backend
        log_success "Docker依赖服务启动完成"
    else
        log_info "使用本地服务..."
        # 启动PostgreSQL
        if command -v brew &> /dev/null; then
            if ! brew services list | grep postgresql | grep started > /dev/null; then
                log_info "启动PostgreSQL..."
                brew services start postgresql@14
                sleep 3
            fi
            # 启动Redis
            if ! brew services list | grep redis | grep started > /dev/null; then
                log_info "启动Redis..."
                brew services start redis
                sleep 2
            fi
            log_success "本地服务启动完成"
        else
            log_warning "请手动启动PostgreSQL和Redis服务"
        fi
    fi
}

# 停止依赖服务
stop_dependencies() {
    log_info "🛑 停止依赖服务..."

    if command -v docker &> /dev/null && docker info > /dev/null 2>&1; then
        cd .. && docker compose down
        cd backend
        log_success "Docker服务已停止"
    else
        if command -v brew &> /dev/null; then
            brew services stop postgresql@14 2>/dev/null || true
            brew services stop redis 2>/dev/null || true
            log_success "本地服务已停止"
        fi
    fi
}

# 主函数
main() {
    local command=${1:-start}

    case $command in
        "start")
            log_info "🚀 启动AgentPedia后端..."

            # 检查必要命令
            check_command "uv"

            setup_directories
            start_dependencies

            # 等待数据库完全启动
            log_info "等待数据库完全启动..."
            sleep 10

            # 运行数据库迁移
            log_info "运行数据库迁移..."
            uv run alembic upgrade head
            log_success "数据库迁移完成"

            # 启动后端服务
            log_info "启动后端服务..."
            nohup uv run python src/agentpedia/main.py > logs/backend.log 2>&1 &
            BACKEND_PID=$!

            # 写入PID文件
            echo $BACKEND_PID > logs/backend.pid
            if [ $? -eq 0 ]; then
                log_success "后端服务启动中 (PID: $BACKEND_PID)"
            else
                log_error "无法写入后端PID文件"
                exit 1
            fi

            # 等待后端服务启动
            wait_for_service "http://localhost:8000/docs" "后端服务"

            log_success "✅ 后端启动完成！"
            echo ""
            echo "🔧 后端地址: http://localhost:8000"
            echo "📋 API文档: http://localhost:8000/docs"
            echo "📝 日志文件: logs/backend.log"
            echo ""
            echo "🛑 停止服务: ./backend-start.sh stop"
            ;;

        "stop")
            log_info "🛑 停止后端服务..."

            # 停止后端服务
            if [ -f "logs/backend.pid" ]; then
                BACKEND_PID=$(cat logs/backend.pid)
                if kill -0 $BACKEND_PID 2>/dev/null; then
                    kill $BACKEND_PID
                    log_success "后端服务已停止 (PID: $BACKEND_PID)"
                else
                    log_warning "后端进程 $BACKEND_PID 不存在"
                fi
                rm -f logs/backend.pid
            fi

            # 停止依赖服务
            stop_dependencies

            log_success "✅ 所有服务已停止"
            ;;

        "restart")
            log_info "🔄 重启后端服务..."
            ./backend-start.sh stop
            sleep 2
            ./backend-start.sh start
            ;;

        "logs")
            log_info "📝 查看后端日志..."
            tail -f logs/backend.log
            ;;

        "migrate")
            log_info "🗄️ 运行数据库迁移..."
            uv run alembic upgrade head
            log_success "数据库迁移完成"
            ;;

        "shell")
            log_info "🐚 启动Python Shell..."
            uv run python -i -c "
from agentpedia.core.database import AsyncSessionLocal
from agentpedia.models import *
print('AgentPedia Shell - 数据库会话: AsyncSessionLocal()')
print('示例用户: user = AsyncSessionLocal().execute(select(User).limit(1)).scalar_one_or_none()')
"
            ;;

        *)
            log_error "未知命令: $command"
            echo ""
            echo "用法:"
            echo "  ./backend-start.sh [命令]"
            echo ""
            echo "命令:"
            echo "  start    启动后端服务 (默认)"
            echo "  stop     停止后端服务"
            echo "  restart  重启后端服务"
            echo "  logs     查看日志"
            echo "  migrate  运行数据库迁移"
            echo "  shell    启动Python Shell"
            echo ""
            exit 1
            ;;
    esac
}

# 捕获 Ctrl+C 信号
trap 'log_info "收到中断信号，正在停止服务..."; ./backend-start.sh stop; exit 0' INT

# 执行主函数
main "$@"