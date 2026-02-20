#!/bin/bash

# Terminal Portfolio 一键部署脚本
# 用于在阿里云服务器上部署 m4tt72/terminal 项目

set -e

echo "🚀 开始部署 Terminal Portfolio..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker 未安装，请先安装 Docker${NC}"
    echo "安装命令: curl -fsSL https://get.docker.com | sh"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose 未安装，请先安装 Docker Compose${NC}"
    echo "安装命令: sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose"
    echo "          sudo chmod +x /usr/local/bin/docker-compose"
    exit 1
fi

echo -e "${GREEN}✅ Docker 和 Docker Compose 已安装${NC}"

# 创建项目目录
PROJECT_DIR="$HOME/terminal-website"
echo -e "${YELLOW}📁 创建项目目录: $PROJECT_DIR${NC}"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 克隆源码
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}📥 克隆 m4tt72/terminal 源码...${NC}"
    git clone https://github.com/m4tt72/terminal.git .
else
    echo -e "${GREEN}✅ 源码已存在，跳过克隆${NC}"
fi

# 复制配置文件
echo -e "${YELLOW}📝 创建配置文件...${NC}"

# 检查是否已有自定义 config.json
if [ -f "public/config.json.backup" ]; then
    echo -e "${GREEN}✅ 发现备份配置，使用现有配置${NC}"
else
    # 备份原始配置
    if [ -f "public/config.json" ]; then
        cp public/config.json public/config.json.original
    fi
    
    # 创建自定义配置
    cat > public/config.json << 'EOF'
{
  "bioTextLines": [
    "嗨！我是 Wang Jian（王俭），21岁的自学开发者",
    "专注于 DevOps 工程和自动化，目标是成为"最强程序员"",
    "热衷于 Linux 服务器维护、Docker 容器化和 Python 自动化",
    "对 AI 技术和系统优化充满热情，持续探索技术边界"
  ],
  "ps1_hostname": "WangJian",
  "ps1_username": "root",
  "repo": "https://github.com/YOUR_USERNAME",
  "social": {
    "github": "YOUR_USERNAME",
    "email": "your.email@example.com"
  },
  "commands": [
    {
      "name": "skills",
      "description": "显示我的技术技能栈",
      "usage": "skills",
      "output": "🛠️ 技能栈：\n\n• Linux - 服务器管理与维护\n• Docker - 容器化部署\n• Nginx - Web 服务器配置\n• Python - 自动化脚本开发\n• Traffic Analysis - 网络流量分析"
    },
    {
      "name": "projects",
      "description": "查看我的项目经验",
      "usage": "projects",
      "output": "📦 项目经验：\n\n🔧 Qinglong Auto-Watchdog\n一个自动监控和修复青龙面板内存泄漏的 Python 脚本\n• 自动检测内存使用情况\n• 智能重启服务避免 OOM\n• 保持系统稳定运行"
    },
    {
      "name": "services",
      "description": "我提供的技术服务",
      "usage": "services",
      "output": "💼 技术服务：\n\n🚨 Server Rescue (CPU/OOM fix)\n   服务器紧急救援，解决 CPU 占用和内存溢出问题\n\n⚙️ Script Setup\n   自动化脚本配置与部署\n\n🌐 Environment Deployment\n   完整的开发/生产环境部署服务"
    }
  ]
}
EOF
    
    echo -e "${YELLOW}⚠️  请编辑 public/config.json 文件，替换 YOUR_USERNAME 和 your.email@example.com${NC}"
    echo -e "${YELLOW}   编辑命令: nano public/config.json 或 vi public/config.json${NC}"
    
    read -p "是否现在编辑配置文件？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} public/config.json
    fi
fi

# 创建 docker-compose.yml
echo -e "${YELLOW}🐳 创建 docker-compose.yml...${NC}"
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  terminal:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: terminal-portfolio
    ports:
      - "3000:3000"
    restart: unless-stopped
EOF

# 检查 Dockerfile 是否存在
if [ ! -f "Dockerfile" ]; then
    echo -e "${YELLOW}📝 创建 Dockerfile...${NC}"
    cat > Dockerfile << 'EOF'
# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制源码
COPY . .

# 构建项目
RUN npm run build

# 运行阶段
FROM node:18-alpine

WORKDIR /app

# 从构建阶段复制构建产物
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# 安装生产依赖（包括 vite 用于 preview）
RUN npm install --production && npm install vite

# 暴露端口
EXPOSE 3000

# 启动应用
CMD ["npx", "vite", "preview", "--host", "0.0.0.0", "--port", "3000"]
EOF
fi

# 构建并启动
echo -e "${YELLOW}🔨 构建 Docker 镜像...${NC}"
docker-compose build

echo -e "${YELLOW}🚀 启动容器...${NC}"
docker-compose up -d

# 等待容器启动
echo -e "${YELLOW}⏳ 等待容器启动...${NC}"
sleep 5

# 检查容器状态
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ 部署成功！${NC}"
    echo ""
    echo -e "${GREEN}🌐 访问地址: http://$(hostname -I | awk '{print $1}'):3000${NC}"
    echo ""
    echo -e "${YELLOW}📋 常用命令:${NC}"
    echo "  查看日志: docker-compose logs -f"
    echo "  停止服务: docker-compose down"
    echo "  重启服务: docker-compose restart"
    echo "  重新构建: docker-compose build && docker-compose up -d"
    echo ""
    echo -e "${YELLOW}⚠️  别忘了在阿里云安全组中开放端口 3000！${NC}"
else
    echo -e "${RED}❌ 容器启动失败，请查看日志:${NC}"
    docker-compose logs
    exit 1
fi
