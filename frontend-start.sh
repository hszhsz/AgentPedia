#!/bin/bash

# AgentPedia 前端启动脚本
# 用法: ./frontend-start.sh

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
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
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
    log_success "目录创建完成"
}

# 安装依赖
install_dependencies() {
    log_info "📦 检查前端依赖..."

    if [ ! -d "frontend" ]; then
        log_error "frontend 目录不存在"
        exit 1
    fi

    cd frontend

    # 检查 package.json 是否存在
    if [ ! -f "package.json" ]; then
        log_error "package.json 不存在"
        exit 1
    fi

    # 检查 node_modules 是否存在或是否需要更新
    if [ ! -d "node_modules" ] || [ "package.json" -nt "node_modules" ]; then
        log_info "安装前端依赖..."
        npm install
        log_success "依赖安装完成"
    else
        log_info "依赖已是最新"
    fi

    cd ..
}

# 停止前端服务
stop_frontend_service() {
    if [ -f "logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill $FRONTEND_PID
            log_success "前端服务已停止 (PID: $FRONTEND_PID)"
        else
            log_warning "前端进程 $FRONTEND_PID 不存在"
        fi
        rm -f logs/frontend.pid
    else
        # 尝试通过端口杀死进程
        FRONTEND_PIDS=$(lsof -ti:3000 2>/dev/null || true)
        if [ ! -z "$FRONTEND_PIDS" ]; then
            for pid in $FRONTEND_PIDS; do
                kill $pid 2>/dev/null || true
            done
            log_success "已停止占用端口3000的进程"
        fi
    fi
}

# 检查服务状态
check_status() {
    log_info "🔍 检查前端服务状态..."

    if [ -f "logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            log_success "前端服务正在运行 (PID: $FRONTEND_PID)"
            echo "📱 前端地址: http://localhost:3000"
            return 0
        else
            log_warning "PID文件存在但进程不存在"
            rm -f logs/frontend.pid
        fi
    fi

    # 检查端口是否被占用
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "端口3000被占用，但没有找到PID文件"
        local pid=$(lsof -ti:3000)
        echo "占用端口的进程: $pid"
    else
        log_info "前端服务未运行"
    fi

    return 1
}

# 主函数
main() {
    local command=${1:-start}

    case $command in
        "start")
            log_info "🚀 启动AgentPedia前端..."

            # 检查必要命令
            check_command "node"
            check_command "npm"

            setup_directories
            install_dependencies

            # 检查端口是否可用
            if ! check_port 3000; then
                log_error "端口3000被占用，请先停止占用该端口的服务"
                exit 1
            fi

            # 停止可能存在的旧服务
            stop_frontend_service

            # 启动前端服务
            log_info "启动前端服务..."
            cd frontend
            nohup npm run dev > ../logs/frontend.log 2>&1 &
            FRONTEND_PID=$!
            cd ..

            # 写入PID文件
            echo $FRONTEND_PID > logs/frontend.pid
            if [ $? -eq 0 ]; then
                log_success "前端服务启动中 (PID: $FRONTEND_PID)"
            else
                log_error "无法写入前端PID文件"
                exit 1
            fi

            # 等待前端服务启动
            wait_for_service "http://localhost:3000" "前端服务"

            log_success "✅ 前端启动完成！"
            echo ""
            echo "📱 前端地址: http://localhost:3000"
            echo "📝 日志文件: logs/frontend.log"
            echo ""
            echo "🛑 停止服务: ./frontend-start.sh stop"
            ;;

        "stop")
            log_info "🛑 停止前端服务..."
            stop_frontend_service
            log_success "✅ 前端服务已停止"
            ;;

        "restart")
            log_info "🔄 重启前端服务..."
            ./frontend-start.sh stop
            sleep 2
            ./frontend-start.sh start
            ;;

        "logs")
            log_info "📝 查看前端日志..."
            if [ -f "logs/frontend.log" ]; then
                tail -f logs/frontend.log
            else
                log_warning "日志文件不存在: logs/frontend.log"
            fi
            ;;

        "status")
            check_status
            ;;

        *)
            log_error "未知命令: $command"
            echo ""
            echo "用法:"
            echo "  ./frontend-start.sh [命令]"
            echo ""
            echo "命令:"
            echo "  start    启动前端服务 (默认)"
            echo "  stop     停止前端服务"
            echo "  restart  重启前端服务"
            echo "  logs     查看日志"
            echo "  status   查看服务状态"
            echo ""
            exit 1
            ;;
    esac
}

# 捕获 Ctrl+C 信号
trap 'log_info "收到中断信号，正在停止服务..."; ./frontend-start.sh stop; exit 0' INT

# 执行主函数
main "$@"