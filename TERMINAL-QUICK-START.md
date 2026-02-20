# Terminal Portfolio 快速部署指南

## 🎯 问题解决方案

你遇到的 config.json 挂载路径问题，最稳妥的解决方案是**从源码构建**，这样可以确保配置文件被正确打包到镜像中。

## 🚀 方法 1：一键部署脚本（推荐）

### 在服务器上执行：

```bash
# 1. 下载部署脚本
curl -O https://你的服务器/terminal-deploy.sh

# 或者直接创建脚本文件
cat > deploy.sh << 'EOF'
[复制 terminal-deploy.sh 的内容]
EOF

# 2. 添加执行权限
chmod +x deploy.sh

# 3. 运行部署脚本
./deploy.sh
```

脚本会自动：
- ✅ 检查 Docker 和 Docker Compose
- ✅ 克隆 m4tt72/terminal 源码
- ✅ 创建你的个性化 config.json
- ✅ 构建 Docker 镜像
- ✅ 启动容器

## 🛠️ 方法 2：手动部署（完全可控）

### 步骤 1: 创建项目目录并克隆源码

```bash
mkdir -p ~/terminal-website
cd ~/terminal-website
git clone https://github.com/m4tt72/terminal.git .
```

### 步骤 2: 创建你的 config.json

```bash
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
```

**⚠️ 重要：** 编辑 config.json，替换 `YOUR_USERNAME` 和 `your.email@example.com`

```bash
nano public/config.json
# 或
vi public/config.json
```

### 步骤 3: 创建 Dockerfile

```bash
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
```

### 步骤 4: 创建 docker-compose.yml

```bash
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
```

### 步骤 5: 构建并启动

```bash
# 构建镜像
docker-compose build

# 启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 🔍 方法 3：调试官方镜像路径（如果你想用官方镜像）

如果你坚持使用官方镜像，先找到正确的路径：

```bash
# 启动测试容器
docker run -d --name terminal-test -p 3000:3000 ghcr.io/m4tt72/terminal:latest

# 进入容器查看目录结构
docker exec -it terminal-test sh

# 在容器内执行
ls -la /app/
ls -la /app/dist/
find / -name "config.json" 2>/dev/null

# 退出容器
exit

# 停止测试容器
docker stop terminal-test && docker rm terminal-test
```

找到正确路径后，更新 docker-compose.yml：

```yaml
version: '3.8'

services:
  terminal:
    image: ghcr.io/m4tt72/terminal:latest
    container_name: terminal-portfolio
    ports:
      - "3000:3000"
    volumes:
      # 使用你找到的正确路径
      - ./config.json:/app/dist/config.json:ro
    restart: unless-stopped
```

## 📋 常用管理命令

```bash
# 查看容器状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 停止容器
docker-compose down

# 重启容器
docker-compose restart

# 重新构建并启动
docker-compose build && docker-compose up -d

# 进入容器调试
docker exec -it terminal-portfolio sh
```

## 🌐 访问网站

部署成功后，在浏览器访问：

```
http://你的服务器IP:3000
```

在终端中输入以下命令测试：

```bash
help        # 查看所有命令
skills      # 查看你的技能
projects    # 查看你的项目
services    # 查看你的服务
theme ls    # 查看可用主题
```

## 🔒 阿里云安全组配置

别忘了在阿里云控制台开放端口 3000：

1. 登录阿里云控制台
2. 进入 ECS 实例管理
3. 点击"安全组" → "配置规则"
4. 添加入站规则：
   - 端口范围：3000/3000
   - 授权对象：0.0.0.0/0
   - 协议类型：TCP

## 🎨 自定义主题

在终端中输入：

```bash
theme ls              # 列出所有主题
theme set gruvboxdark # 设置主题
```

## 🐛 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker-compose logs

# 检查端口占用
netstat -tuln | grep 3000
```

### 配置未生效

```bash
# 进入容器检查配置文件
docker exec -it terminal-portfolio sh
cat /app/dist/config.json
```

### 重新部署

```bash
# 完全清理并重新部署
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## ✅ 为什么推荐从源码构建？

1. **完全可控** - 不依赖官方镜像的内部结构
2. **配置可靠** - config.json 直接打包到镜像中
3. **易于调试** - 构建过程透明，问题容易定位
4. **可定制化** - 可以修改源码、添加功能
5. **版本固定** - 不受官方镜像更新影响

## 📞 需要帮助？

如果遇到问题，提供以下信息：

```bash
# 系统信息
uname -a
docker --version
docker-compose --version

# 容器日志
docker-compose logs

# 容器状态
docker-compose ps
```

祝部署顺利！🎉
