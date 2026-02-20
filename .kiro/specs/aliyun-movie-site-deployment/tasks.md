# 电影导航网站阿里云部署 - 任务清单

## 阶段 1：环境准备和连通性验证

- [ ] 1.1 验证本地文件完整性
  - 确认 `C:\Users\Administrator\.gemini\antigravity\scratch\movie-nav` 目录存在
  - 确认包含 `index.html`, `style.css`, `script.js`
  - 检查文件内容完整性

- [ ] 1.2 测试 SSH 连接
  - 使用 `ssh root@8.153.206.100` 测试连接
  - 记录连接延迟和稳定性
  - 如果连接不稳定，尝试使用 PuTTY 或配置 ServerAliveInterval

- [ ] 1.3 检查服务器基本信息
  - 执行 `uname -a` 确认操作系统
  - 执行 `cat /etc/os-release` 确认发行版
  - 执行 `nginx -v` 确认 Nginx 版本

## 阶段 2：Nginx 配置诊断

- [ ] 2.1 定位 Nginx 配置文件
  - 执行 `nginx -t` 查看配置文件路径
  - 记录主配置文件位置
  - 记录站点配置文件位置

- [ ] 2.2 备份现有配置
  - 备份 `/etc/nginx/nginx.conf`
  - 备份站点配置文件（default 或 default.conf）
  - 确认备份文件创建成功

- [ ] 2.3 检查当前 root 路径
  - 查看配置文件中的 `root` 指令
  - 确认是 `/var/www/html` 还是 `/usr/share/nginx/html`
  - 检查该目录是否存在且可写

- [ ] 2.4 验证 Nginx 运行状态
  - 执行 `systemctl status nginx` 检查服务状态
  - 执行 `ps aux | grep nginx` 确认进程运行
  - 如果未运行，启动 Nginx 服务

## 阶段 3：端口和网络诊断

- [ ] 3.1 检查 Nginx 端口监听
  - 执行 `netstat -tunlp | grep :80` 或 `ss -tunlp | grep :80`
  - 确认 Nginx 监听在 0.0.0.0:80
  - 记录监听状态

- [ ] 3.2 服务器本地访问测试
  - 执行 `curl -I http://localhost`
  - 执行 `curl -I http://127.0.0.1`
  - 检查返回的 HTTP 状态码

- [ ] 3.3 检查服务器防火墙
  - 检查 iptables：`iptables -L -n -v`
  - 检查 firewalld：`systemctl status firewalld` 和 `firewall-cmd --list-all`
  - 检查 UFW：`ufw status`
  - 如果 80 端口被阻止，添加允许规则

- [ ] 3.4 外部端口可达性测试
  - 从本地 Windows 执行 `Test-NetConnection -ComputerName 8.153.206.100 -Port 80`
  - 或使用 `curl -I http://8.153.206.100`
  - 记录测试结果

## 阶段 4：阿里云安全组配置

- [ ] 4.1 登录阿里云控制台
  - 访问阿里云 ECS 管理控制台
  - 找到实例 (IP: 8.153.206.100)

- [ ] 4.2 检查安全组规则
  - 进入"安全组配置"
  - 查看入方向规则
  - 确认是否存在允许 80 端口的规则

- [ ] 4.3 添加安全组规则（如果不存在）
  - 添加入方向规则
  - 协议类型：TCP
  - 端口范围：80/80
  - 授权对象：0.0.0.0/0
  - 保存规则

- [ ] 4.4 验证安全组生效
  - 等待 1-2 分钟让规则生效
  - 重新测试外部端口可达性

## 阶段 5：Nginx 配置优化

- [ ] 5.1 创建或修改站点配置
  - 编辑站点配置文件
  - 设置 `root /var/www/html;`
  - 设置 `index index.html;`
  - 配置日志路径

- [ ] 5.2 添加 MIME 类型配置
  - 确保 CSS 文件正确识别为 text/css
  - 确保 JS 文件正确识别为 application/javascript

- [ ] 5.3 添加安全头部
  - 添加 X-Frame-Options
  - 添加 X-Content-Type-Options
  - 添加 X-XSS-Protection

- [ ] 5.4 验证配置语法
  - 执行 `nginx -t`
  - 确认配置无语法错误
  - 如果有错误，根据提示修复

- [ ] 5.5 重载 Nginx 配置
  - 执行 `nginx -s reload`
  - 或 `systemctl reload nginx`
  - 确认重载成功

## 阶段 6：文件传输

- [ ] 6.1 确认目标目录
  - 确认 `/var/www/html` 目录存在
  - 如果不存在，创建目录：`mkdir -p /var/www/html`
  - 检查目录权限

- [ ] 6.2 传输网站文件
  - 使用 SCP 或 WinSCP 传输 `index.html`
  - 传输 `style.css`
  - 传输 `script.js`
  - 确认所有文件传输成功

- [ ] 6.3 验证文件完整性
  - 执行 `ls -lh /var/www/html/`
  - 检查文件大小是否与本地一致
  - 使用 `head` 或 `cat` 查看文件内容片段

- [ ] 6.4 设置文件权限
  - 执行 `chmod 644 /var/www/html/*.html`
  - 执行 `chmod 644 /var/www/html/*.css`
  - 执行 `chmod 644 /var/www/html/*.js`
  - 执行 `chmod 755 /var/www/html`

- [ ] 6.5 设置文件所有者
  - 确认 Nginx 运行用户（www-data 或 nginx）
  - 执行 `chown -R www-data:www-data /var/www/html` 或 `chown -R nginx:nginx /var/www/html`

## 阶段 7：部署验证

- [ ] 7.1 服务器端验证
  - 执行 `curl http://localhost` 查看响应
  - 检查 Nginx access.log：`tail -f /var/log/nginx/access.log`
  - 检查 Nginx error.log：`tail -f /var/log/nginx/error.log`
  - 确认无错误日志

- [ ] 7.2 外部访问验证
  - 从本地浏览器访问 `http://8.153.206.100`
  - 确认网站首页正常显示
  - 检查浏览器开发者工具控制台

- [ ] 7.3 资源加载验证
  - 确认 CSS 文件加载成功（检查 Network 标签）
  - 确认 JS 文件加载成功
  - 确认所有资源返回 200 状态码

- [ ] 7.4 功能测试
  - 验证玻璃拟态效果显示正常
  - 测试所有链接可点击
  - 测试页面交互功能

- [ ] 7.5 响应式测试
  - 使用浏览器开发者工具测试移动端视图
  - 测试不同屏幕尺寸下的显示效果
  - 确认移动端适配正常

## 阶段 8：性能和安全优化（可选）

- [ ] 8.1* 启用 Gzip 压缩
  - 在 Nginx 配置中启用 gzip
  - 配置压缩类型和最小长度
  - 重载配置并测试

- [ ] 8.2* 配置静态资源缓存
  - 为 CSS/JS 设置缓存过期时间
  - 添加 Cache-Control 头部
  - 验证缓存生效

- [ ] 8.3* 配置日志轮转
  - 检查 logrotate 配置
  - 确保日志不会无限增长

## 阶段 9：文档和交付

- [ ] 9.1 记录最终配置
  - 记录 Nginx 配置文件路径
  - 记录网站文件路径
  - 记录访问 URL

- [ ] 9.2 创建维护文档
  - 记录常用命令
  - 记录故障排查步骤
  - 记录更新流程

- [ ] 9.3 验收确认
  - 与用户确认网站访问正常
  - 确认所有功能符合预期
  - 记录任何遗留问题

## 故障排查任务（按需执行）

- [ ] T1. SSH 连接问题排查
  - 检查 SSH 服务状态
  - 检查 22 端口防火墙规则
  - 检查阿里云安全组 22 端口规则
  - 查看 SSH 日志

- [ ] T2. Nginx 启动失败排查
  - 查看 Nginx 错误日志
  - 检查配置文件语法
  - 检查端口占用情况
  - 检查文件权限

- [ ] T3. 403 Forbidden 排查
  - 检查文件权限
  - 检查 SELinux 状态
  - 检查 Nginx 用户权限
  - 检查目录索引配置

- [ ] T4. 404 Not Found 排查
  - 确认文件路径正确
  - 检查 Nginx root 配置
  - 确认 index.html 存在
  - 检查文件名大小写

- [ ] T5. 外部无法访问排查
  - 确认服务器本地可访问
  - 检查服务器防火墙
  - 检查阿里云安全组
  - 确认 Nginx 监听地址

- [ ] T6. CSS/JS 加载失败排查
  - 检查文件路径
  - 检查 MIME 类型配置
  - 查看浏览器控制台错误
  - 检查 Nginx 日志

## 注意事项

1. **任务执行顺序**：建议按阶段顺序执行，每个阶段完成后再进入下一阶段
2. **错误处理**：如果某个任务失败，先执行对应的故障排查任务
3. **备份优先**：在修改任何配置前，务必先备份
4. **验证为主**：每个阶段完成后都要进行验证
5. **可选任务**：标记为 `*` 的任务为可选，可根据需要执行

## 成功标准

部署成功的标志：
✅ 能够通过 `http://8.153.206.100` 访问网站
✅ 网站显示正常，包括玻璃拟态效果
✅ 所有资源文件（CSS、JS）正确加载
✅ 所有链接可点击
✅ 移动端访问正常
✅ 浏览器控制台无错误
