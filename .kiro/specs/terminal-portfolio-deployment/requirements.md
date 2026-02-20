# 需求文档

## 简介

本项目旨在为 DevOps 工程师 Wang Jian（王健）在阿里云服务器上部署一个黑客终端风格的个人网站。该网站基于开源项目 m4tt72/terminal，通过 Docker 容器化部署，展示个人技能、项目经验和服务能力。

## 术语表

- **Terminal_Website**: 基于 m4tt72/terminal 的黑客终端风格个人网站系统
- **Docker_Compose**: Docker 容器编排工具
- **Config_File**: 终端网站的配置文件（config.json）
- **Container**: Docker 容器实例
- **Host_System**: 阿里云服务器（宿主机系统）

## 需求

### 需求 1：Docker Compose 配置生成

**用户故事：** 作为部署者，我想要生成 docker-compose.yml 配置文件，以便能够通过 Docker Compose 快速启动终端网站容器。

#### 验收标准

1. THE Docker_Compose 配置文件 SHALL 使用官方镜像 `m4tt72/terminal`
2. THE Docker_Compose 配置文件 SHALL 将容器端口 3000 映射到宿主机端口 3000
3. THE Docker_Compose 配置文件 SHALL 挂载本地 config.json 文件到容器内的 `/usr/src/app/public/config.json` 路径
4. THE Docker_Compose 配置文件 SHALL 配置容器在退出时自动重启（restart policy）
5. THE Docker_Compose 配置文件 SHALL 使用有效的 YAML 语法格式

### 需求 2：终端配置文件生成

**用户故事：** 作为网站所有者，我想要生成个性化的 config.json 配置文件，以便终端网站能够展示我的个人信息、技能和项目。

#### 验收标准

1. THE Config_File SHALL 设置终端提示符为 `root@WangJian:~$`
2. THE Config_File SHALL 包含个人简介，描述自学开发之路和对 AI/Linux 的热情
3. THE Config_File SHALL 包含 GitHub 和 Email 社交链接占位符
4. THE Config_File SHALL 定义 `skills` 命令，列出技能：Linux、Docker、Nginx、Python、Traffic Analysis
5. THE Config_File SHALL 定义 `projects` 命令，描述 "Qinglong Auto-Watchdog" 项目（修复内存泄漏的脚本）
6. THE Config_File SHALL 定义 `services` 命令，列出三项服务：Server Rescue (CPU/OOM fix)、Script Setup、Environment Deployment
7. THE Config_File SHALL 使用有效的 JSON 语法格式
8. WHEN 配置文件被容器加载 THEN Terminal_Website SHALL 正确解析并显示所有配置的命令和信息

### 需求 3：部署指南文档生成

**用户故事：** 作为部署者，我想要获得完整的部署指南，以便能够通过复制粘贴命令快速完成部署。

#### 验收标准

1. THE 部署指南 SHALL 包含创建项目目录的 Linux 命令
2. THE 部署指南 SHALL 包含创建 docker-compose.yml 文件的命令
3. THE 部署指南 SHALL 包含创建 config.json 文件的命令
4. THE 部署指南 SHALL 包含启动 Docker 容器的命令
5. THE 部署指南 SHALL 包含验证容器运行状态的命令
6. THE 部署指南 SHALL 包含访问网站的 URL 说明
7. WHEN 用户按顺序执行所有命令 THEN Container SHALL 成功启动并在端口 3000 上提供服务
8. THE 部署指南中的所有命令 SHALL 可以直接复制粘贴到终端执行

### 需求 4：配置内容个性化

**用户故事：** 作为网站所有者，我想要配置文件准确反映我的个人信息和专业背景，以便访问者了解我的技能和经验。

#### 验收标准

1. THE Config_File SHALL 在个人简介中提及年龄为 21 岁
2. THE Config_File SHALL 在个人简介中提及角色为 DevOps Engineer & Automation Specialist
3. THE Config_File SHALL 在个人简介中提及目标是成为"最强程序员"
4. THE Config_File SHALL 在技能列表中包含所有五项专长技能
5. THE Config_File SHALL 在项目描述中说明 Qinglong Auto-Watchdog 的核心功能（修复内存泄漏）
6. THE Config_File SHALL 在服务列表中准确描述三项提供的服务

### 需求 5：文件结构和路径管理

**用户故事：** 作为部署者，我想要清晰的文件组织结构，以便于管理和维护部署配置。

#### 验收标准

1. THE 部署指南 SHALL 指定创建专用项目目录（如 `~/terminal-website`）
2. THE docker-compose.yml 文件 SHALL 位于项目根目录
3. THE config.json 文件 SHALL 位于项目根目录
4. THE Docker_Compose 配置 SHALL 使用相对路径引用 config.json 文件
5. WHEN 用户在项目目录中执行 `docker-compose up -d` THEN Container SHALL 正确找到并挂载 config.json 文件

### 需求 6：容器生命周期管理

**用户故事：** 作为系统管理员，我想要容器能够自动重启和优雅停止，以便确保服务的高可用性。

#### 验收标准

1. WHEN Host_System 重启 THEN Container SHALL 自动启动
2. WHEN Container 异常退出 THEN Container SHALL 自动重启
3. THE 部署指南 SHALL 包含停止容器的命令（`docker-compose down`）
4. THE 部署指南 SHALL 包含查看容器日志的命令（`docker-compose logs`）
5. THE 部署指南 SHALL 包含重启容器的命令（`docker-compose restart`）

### 需求 7：端口和网络配置

**用户故事：** 作为部署者，我想要明确的端口配置说明，以便正确配置防火墙和访问网站。

#### 验收标准

1. THE Docker_Compose 配置 SHALL 明确指定端口映射为 `3000:3000`
2. THE 部署指南 SHALL 说明需要在阿里云安全组中开放端口 3000
3. THE 部署指南 SHALL 提供访问 URL 格式：`http://<服务器IP>:3000`
4. WHEN 端口 3000 在防火墙中开放 THEN 外部用户 SHALL 能够通过浏览器访问 Terminal_Website

### 需求 8：命令输出格式化

**用户故事：** 作为网站访问者，我想要在终端中看到格式良好的命令输出，以便清晰地了解信息。

#### 验收标准

1. WHEN 用户在终端中执行 `skills` 命令 THEN Terminal_Website SHALL 以列表形式显示所有技能
2. WHEN 用户在终端中执行 `projects` 命令 THEN Terminal_Website SHALL 显示项目名称和详细描述
3. WHEN 用户在终端中执行 `services` 命令 THEN Terminal_Website SHALL 以列表形式显示所有服务项
4. THE Config_File SHALL 使用适当的换行符和格式化字符以确保输出可读性
