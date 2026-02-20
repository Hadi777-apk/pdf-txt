# 电影导航网站阿里云部署 - 设计文档

## 1. 架构概述

### 1.1 部署架构
```
本地环境 (Windows)                    阿里云服务器 (Linux)
┌─────────────────────┐              ┌──────────────────────┐
│ movie-nav/          │              │                      │
│  ├─ index.html      │   SSH/SCP    │  Nginx               │
│  ├─ style.css       │ ──────────>  │    ↓                 │
│  └─ script.js       │              │  /var/www/html/      │
└─────────────────────┘              │  或                  │
                                     │  /usr/share/nginx/   │
                                     └──────────────────────┘
                                              ↓
                                     阿里云安全组 (80端口)
                                              ↓
                                     公网访问: http://8.153.206.100
```

### 1.2 技术栈
- **本地环境**：Windows, PowerShell/CMD
- **传输工具**：SCP, SFTP, 或 WinSCP
- **服务器**：Linux (待确认发行版)
- **Web 服务器**：Nginx
- **协议**：HTTP (端口 80)

## 2. 详细设计

### 2.1 连通性诊断方案

#### 2.1.1 SSH 连接测试
**目标**：建立稳定的 SSH 连接

**方法 1：使用 PowerShell SSH 客户端**
```powershell
# 测试 SSH 连接
ssh -v root@8.153.206.100

# 如果使用密钥
ssh -i path\to\key.pem root@8.153.206.100
```

**方法 2：使用 PuTTY（Windows 图形化工具）**
- Host: 8.153.206.100
- Port: 22
- Connection type: SSH
- 保存会话以便重用

**连接稳定性优化**：
```
# 在 SSH 配置中添加保活设置
ServerAliveInterval 60
ServerAliveCountMax 3
```

#### 2.1.2 端口检测方案

**外部检测（从本地 Windows）**：
```powershell
# 方法 1: 使用 Test-NetConnection
Test-NetConnection -ComputerName 8.153.206.100 -Port 80

# 方法 2: 使用 telnet (需要先启用)
telnet 8.153.206.100 80

# 方法 3: 使用 curl
curl -I http://8.153.206.100
```

**内部检测（在服务器上）**：
```bash
# 检查 Nginx 是否监听 80 端口
netstat -tunlp | grep :80
# 或
ss -tunlp | grep :80

# 检查 Nginx 进程
ps aux | grep nginx

# 本地测试访问
curl -I http://localhost
curl -I http://127.0.0.1
```

### 2.2 Nginx 配置方案

#### 2.2.1 配置文件定位
**常见位置**：
- 主配置：`/etc/nginx/nginx.conf`
- 站点配置：`/etc/nginx/sites-available/default` (Debian/Ubuntu)
- 站点配置：`/etc/nginx/conf.d/default.conf` (CentOS/RHEL)

**定位命令**：
```bash
# 查找 Nginx 配置文件
nginx -t

# 查看主配置文件
cat /etc/nginx/nginx.conf

# 查找所有配置文件
find /etc/nginx -name "*.conf"
```

#### 2.2.2 配置验证和修改

**步骤 1：备份原配置**
```bash
# 备份主配置
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup.$(date +%Y%m%d)

# 备份站点配置
cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup.$(date +%Y%m%d)
```

**步骤 2：检查当前 root 路径**
```bash
# 查看默认站点的 root 配置
grep -r "root" /etc/nginx/sites-available/default
# 或
grep -r "root" /etc/nginx/conf.d/default.conf
```

**步骤 3：推荐的 Nginx 配置**
```nginx
server {
    listen 80;
    listen [::]:80;
    
    server_name 8.153.206.100;
    
    # 网站根目录
    root /var/www/html;
    index index.html;
    
    # 日志配置
    access_log /var/log/nginx/movie-nav-access.log;
    error_log /var/log/nginx/movie-nav-error.log;
    
    # 主要位置块
    location / {
        try_files $uri $uri/ =404;
    }
    
    # CSS 文件
    location ~* \.css$ {
        add_header Content-Type text/css;
        expires 7d;
    }
    
    # JS 文件
    location ~* \.js$ {
        add_header Content-Type application/javascript;
        expires 7d;
    }
    
    # 安全头部
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**步骤 4：验证和重载**
```bash
# 测试配置语法
nginx -t

# 如果测试通过，重载配置
nginx -s reload

# 或重启 Nginx
systemctl restart nginx
```

### 2.3 文件传输方案

#### 2.3.1 方案 A：使用 SCP（命令行）
```powershell
# 从 Windows PowerShell 执行
cd C:\Users\Administrator\.gemini\antigravity\scratch\movie-nav

# 传输单个文件
scp index.html root@8.153.206.100:/var/www/html/
scp style.css root@8.153.206.100:/var/www/html/
scp script.js root@8.153.206.100:/var/www/html/

# 或一次性传输所有文件
scp *.html *.css *.js root@8.153.206.100:/var/www/html/
```

#### 2.3.2 方案 B：使用 WinSCP（图形化工具）
1. 下载并安装 WinSCP
2. 创建新连接：
   - 协议：SFTP
   - 主机：8.153.206.100
   - 端口：22
   - 用户名：root
3. 拖拽文件到 `/var/www/html/`

#### 2.3.3 方案 C：使用 SFTP
```powershell
# 启动 SFTP 会话
sftp root@8.153.206.100

# 在 SFTP 提示符下
cd /var/www/html
lcd C:\Users\Administrator\.gemini\antigravity\scratch\movie-nav
put index.html
put style.css
put script.js
quit
```

#### 2.3.4 文件权限设置
```bash
# 在服务器上执行
cd /var/www/html

# 设置文件权限
chmod 644 index.html style.css script.js

# 设置目录权限
chmod 755 /var/www/html

# 设置所有者（如果需要）
chown -R www-data:www-data /var/www/html  # Debian/Ubuntu
# 或
chown -R nginx:nginx /var/www/html  # CentOS/RHEL
```

### 2.4 防火墙和安全组配置

#### 2.4.1 服务器防火墙检查

**检查 iptables**：
```bash
# 查看 iptables 规则
iptables -L -n -v

# 如果 80 端口被阻止，添加规则
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
iptables-save > /etc/iptables/rules.v4
```

**检查 firewalld**：
```bash
# 查看 firewalld 状态
systemctl status firewalld

# 查看开放的端口
firewall-cmd --list-all

# 如果需要开放 80 端口
firewall-cmd --permanent --add-service=http
firewall-cmd --reload
```

**检查 UFW (Ubuntu)**：
```bash
# 查看 UFW 状态
ufw status

# 允许 80 端口
ufw allow 80/tcp
```

#### 2.4.2 阿里云安全组配置

**检查步骤**（需要在阿里云控制台操作）：

1. 登录阿里云控制台
2. 进入 ECS 实例管理
3. 找到实例 (8.153.206.100)
4. 点击"安全组配置"
5. 检查入方向规则

**必需的安全组规则**：
```
规则方向：入方向
授权策略：允许
协议类型：TCP
端口范围：80/80
授权对象：0.0.0.0/0
优先级：1
描述：允许 HTTP 访问
```

**如果规则不存在，添加规则**：
- 点击"添加安全组规则"
- 按上述参数配置
- 保存

### 2.5 部署验证方案

#### 2.5.1 服务器端验证
```bash
# 1. 检查文件是否存在
ls -lh /var/www/html/

# 2. 检查文件内容
head -n 20 /var/www/html/index.html

# 3. 检查 Nginx 状态
systemctl status nginx

# 4. 检查 Nginx 错误日志
tail -f /var/log/nginx/error.log

# 5. 本地测试访问
curl http://localhost
curl -I http://localhost

# 6. 检查响应头
curl -I http://localhost | grep "HTTP\|Content-Type"
```

#### 2.5.2 客户端验证
```powershell
# 从 Windows 测试
curl http://8.153.206.100

# 或在浏览器中访问
# http://8.153.206.100
```

#### 2.5.3 功能验证清单
- [ ] 网站首页能够加载
- [ ] CSS 样式正确应用（玻璃拟态效果）
- [ ] JavaScript 功能正常
- [ ] 所有链接可点击
- [ ] 移动端响应式布局正常
- [ ] 浏览器控制台无错误

## 3. 故障排查指南

### 3.1 SSH 连接问题

**问题**：连接超时
```bash
# 解决方案：
1. 检查服务器 SSH 服务状态
   systemctl status sshd
2. 检查防火墙是否阻止 22 端口
3. 检查阿里云安全组是否允许 22 端口
```

**问题**：认证失败
```bash
# 解决方案：
1. 确认用户名和密码正确
2. 检查 SSH 密钥权限（如果使用密钥）
3. 查看 SSH 日志：tail -f /var/log/auth.log
```

### 3.2 Nginx 问题

**问题**：Nginx 未运行
```bash
# 解决方案：
systemctl start nginx
systemctl enable nginx  # 设置开机自启
```

**问题**：配置错误
```bash
# 解决方案：
nginx -t  # 查看具体错误
# 根据错误提示修复配置
# 恢复备份：cp /etc/nginx/nginx.conf.backup /etc/nginx/nginx.conf
```

**问题**：403 Forbidden
```bash
# 解决方案：
1. 检查文件权限：ls -l /var/www/html/
2. 检查 SELinux：getenforce
   如果是 Enforcing：setenforce 0
3. 检查 Nginx 用户权限
```

**问题**：404 Not Found
```bash
# 解决方案：
1. 确认文件路径正确
2. 检查 Nginx root 配置
3. 确认 index.html 存在
```

### 3.3 网络访问问题

**问题**：本地能访问，外部不能
```bash
# 解决方案：
1. 检查服务器防火墙
2. 检查阿里云安全组规则
3. 确认 Nginx 监听 0.0.0.0:80 而不是 127.0.0.1:80
```

**问题**：CSS/JS 加载失败
```bash
# 解决方案：
1. 检查文件路径是否正确
2. 检查 MIME 类型配置
3. 查看浏览器控制台错误
4. 检查 Nginx access.log 和 error.log
```

## 4. 性能优化建议

### 4.1 Nginx 优化
```nginx
# 启用 gzip 压缩
gzip on;
gzip_types text/css application/javascript text/html;
gzip_min_length 1000;

# 设置缓存
location ~* \.(css|js|jpg|jpeg|png|gif|ico)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 4.2 静态资源优化
- 压缩 CSS 和 JS 文件
- 优化图片大小
- 使用 CDN（可选）

## 5. 安全加固建议

### 5.1 基础安全
```bash
# 1. 修改 SSH 默认端口（可选）
# 编辑 /etc/ssh/sshd_config
# Port 2222

# 2. 禁用 root 密码登录（推荐使用密钥）
# PermitRootLogin prohibit-password

# 3. 配置防火墙只允许必要端口
```

### 5.2 Nginx 安全头部
```nginx
# 已在配置中包含
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

## 6. 未来扩展

### 6.1 HTTPS 配置（可选）
- 使用 Let's Encrypt 免费证书
- 配置 SSL/TLS
- 强制 HTTPS 重定向

### 6.2 域名绑定（可选）
- 在域名提供商配置 A 记录
- 修改 Nginx server_name
- 配置 DNS 解析

### 6.3 监控和日志
- 配置日志轮转
- 设置监控告警
- 使用 Nginx 状态模块

## 7. 正确性属性

### 7.1 部署正确性属性

**属性 1：文件完整性**
- **描述**：所有本地文件必须成功传输到服务器
- **验证**：服务器上的文件数量和大小与本地一致

**属性 2：Nginx 配置有效性**
- **描述**：Nginx 配置必须通过语法检查
- **验证**：`nginx -t` 返回成功

**属性 3：端口可达性**
- **描述**：80 端口必须从外部可访问
- **验证**：从外部网络 `curl http://8.153.206.100` 返回 200

**属性 4：内容正确性**
- **描述**：访问网站返回正确的 HTML 内容
- **验证**：响应包含预期的 HTML 标签和内容

**属性 5：资源加载**
- **描述**：所有静态资源（CSS、JS）必须正确加载
- **验证**：浏览器开发者工具显示所有资源 200 状态

## 8. 测试策略

### 8.1 单元测试
- SSH 连接测试
- 端口可达性测试
- 文件传输验证
- Nginx 配置验证

### 8.2 集成测试
- 端到端部署流程测试
- 完整的访问路径测试

### 8.3 验收测试
- 用户访问场景测试
- 多设备兼容性测试
- 性能基准测试

## 9. 部署检查清单

### 9.1 部署前检查
- [ ] 本地文件准备完毕
- [ ] SSH 连接信息确认
- [ ] 备份现有配置

### 9.2 部署中检查
- [ ] SSH 连接成功
- [ ] Nginx 配置正确
- [ ] 文件传输完成
- [ ] 权限设置正确
- [ ] Nginx 重载成功

### 9.3 部署后检查
- [ ] 服务器本地访问正常
- [ ] 外部访问正常
- [ ] 所有资源加载正常
- [ ] 功能测试通过
- [ ] 日志无错误

## 10. 回滚方案

如果部署失败，执行以下回滚步骤：

```bash
# 1. 恢复 Nginx 配置
cp /etc/nginx/nginx.conf.backup /etc/nginx/nginx.conf
nginx -s reload

# 2. 删除新上传的文件（如果需要）
rm /var/www/html/index.html
rm /var/www/html/style.css
rm /var/www/html/script.js

# 3. 恢复原有文件（如果有备份）
# cp /backup/old-site/* /var/www/html/
```
