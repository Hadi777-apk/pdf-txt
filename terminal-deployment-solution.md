# m4tt72/terminal Docker 部署解决方案

## 问题分析

你遇到的问题是 config.json 挂载路径不正确。这个项目使用 Vite + Svelte 构建，构建后的静态文件在 `dist/` 目录，而 config.json 需要在构建后的静态资源中被正确读取。

## 方案 1：使用官方镜像（推荐尝试的正确路径）

根据 Vite 项目的标准结构，config.json 应该在 public 目录，构建后会被复制到 dist 根目录。

### docker-compose.yml (方案 1)

```yaml
version: '3.8'

services:
  terminal:
    image: ghcr.io/m4tt72/terminal:latest
    container_name: terminal-portfolio
    ports:
      - "3000:3000"
    volumes:
      # 尝试挂载到构建后的静态文件目录
      - ./config.json:/app/dist/config.json:ro
    restart: unless-stopped
```

### 如果方案 1 不工作，尝试这些路径：

```yaml
# 尝试 1: 挂载到 dist 目录
- ./config.json:/app/dist/config.json:ro

# 尝试 2: 挂载到 public 目录（如果容器保留了源码）
- ./config.json:/app/public/config.json:ro

# 尝试 3: 挂载到根目录
- ./config.json:/app/config.json:ro

# 尝试 4: 如果使用 nginx 提供服务
- ./config.json:/usr/share/nginx/html/config.json:ro
```

## 方案 2：从源码构建（最稳妥的方案）

这个方案直接从 GitHub 克隆源码，将你的 config.json 复制进去，然后构建镜像。

### 步骤 1: 创建项目目录结构

```bash
mkdir -p ~/terminal-website
cd ~/terminal-website
```

### 步骤 2: 克隆源码

```bash
git clone https://github.com/m4tt72/terminal.git .
```

### 步骤 3: 创建你的 config.json

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

### 步骤 4: 创建 Dockerfile（如果项目没有）

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

# 安装生产依赖
RUN npm install --production

# 暴露端口
EXPOSE 3000

# 启动应用
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]
EOF
```

### 步骤 5: 创建 docker-compose.yml

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

### 步骤 6: 构建并启动

```bash
# 构建镜像
docker-compose build

# 启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 方案 3：最简单的覆盖方案

如果你只想快速测试，可以直接在容器启动后进入容器查看实际路径：

```bash
# 启动容器
docker run -d --name terminal-test -p 3000:3000 ghcr.io/m4tt72/terminal:latest

# 进入容器
docker exec -it terminal-test sh

# 查找 config.json 的位置
find / -name "config.json" 2>/dev/null

# 查看应用目录结构
ls -la /app/
ls -la /app/dist/
ls -la /app/public/

# 退出容器
exit

# 停止并删除测试容器
docker stop terminal-test && docker rm terminal-test
```

找到正确路径后，更新你的 docker-compose.yml。

## 验证部署

部署成功后，访问 `http://你的服务器IP:3000`，在终端中输入：

```bash
help        # 查看所有命令
skills      # 查看技能
projects    # 查看项目
services    # 查看服务
```

如果显示的是你自定义的内容，说明配置成功！

## 故障排查

### 1. 容器无法启动
```bash
docker-compose logs
```

### 2. 配置未生效
```bash
# 进入容器检查文件
docker exec -it terminal-portfolio sh
cat /app/dist/config.json  # 或其他可能的路径
```

### 3. 端口被占用
```bash
# 检查端口
netstat -tuln | grep 3000
# 或
lsof -i :3000
```

## 推荐方案

**我强烈推荐使用方案 2（从源码构建）**，因为：
1. 完全可控，不依赖官方镜像的内部结构
2. 可以直接修改 public/config.json，确保配置被正确打包
3. 构建过程透明，易于调试
4. 可以自定义 Dockerfile 优化镜像大小

如果你想快速测试，先用方案 3 找到正确路径，然后用方案 1。
