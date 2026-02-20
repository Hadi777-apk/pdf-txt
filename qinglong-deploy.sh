#!/bin/bash

# 青龙面板 Docker 部署脚本

echo "========================================="
echo "青龙面板 Docker 部署"
echo "========================================="

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装"
    exit 1
fi

echo "✅ Docker 环境检查通过"

# 启动服务
echo "📦 启动青龙面板..."
docker-compose up -d

# 等待容器启动
echo "⏳ 等待容器启动..."
sleep 5

# 检查状态
if docker ps | grep -q qinglong; then
    echo "✅ 青龙面板启动成功"
    echo ""
    echo "========================================="
    echo "📝 访问信息"
    echo "========================================="
    echo "访问地址: http://8.153.206.100:5700"
    echo "首次访问会进行初始化配置"
    echo ""
    echo "常用命令:"
    echo "  查看日志: docker-compose logs -f qinglong"
    echo "  停止服务: docker-compose down"
    echo "  重启服务: docker-compose restart qinglong"
    echo "  进入容器: docker exec -it qinglong bash"
else
    echo "❌ 启动失败，请检查日志"
    docker-compose logs qinglong
    exit 1
fi
