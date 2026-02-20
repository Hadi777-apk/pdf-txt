# 青龙面板部署指南

## 快速开始

### 1. 前置要求
- Linux 系统（乌托邦）
- Docker 已安装
- Docker Compose 已安装

### 2. 一键部署

```bash
# 赋予脚本执行权限
chmod +x qinglong-deploy.sh

# 运行部署脚本
./qinglong-deploy.sh
```

### 3. 访问面板
- 地址：`http://8.153.206.100:5700`
- 首次访问会进行初始化配置

---

## 常用命令

### 查看运行状态
```bash
docker-compose ps
```

### 查看实时日志
```bash
docker-compose logs -f qinglong
```

### 停止服务
```bash
docker-compose down
```

### 重启服务
```bash
docker-compose restart qinglong
```

### 进入容器
```bash
docker exec -it qinglong bash
```

### 查看容器内文件
```bash
docker exec qinglong ls -la /ql/data
```

---

## 初始化配置

首次访问面板后，需要：

1. **设置管理员账号**
   - 用户名：自定义
   - 密码：自定义（务必记住）

2. **添加定时任务**
   - 在面板中添加脚本任务
   - 设置执行时间

3. **环境变量配置**
   - 如需要，在"环境变量"中添加必要的参数

---

## 数据备份

所有数据存储在 Docker 卷中，备份方法：

```bash
# 备份数据
docker run --rm -v qinglong_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/qinglong-backup.tar.gz -C /data .

# 恢复数据
docker run --rm -v qinglong_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/qinglong-backup.tar.gz -C /data
```

---

## 升级面板

```bash
# 拉取最新镜像
docker pull whyour/qinglong:latest

# 重启服务（自动使用新镜像）
docker-compose up -d
```

---

## 常见问题

### Q: 无法访问面板？
A: 检查防火墙是否开放 5700 端口
```bash
# 开放端口（Ubuntu/Debian）
sudo ufw allow 5700
```

### Q: 容器一直重启？
A: 查看日志找出原因
```bash
docker-compose logs qinglong
```

### Q: 如何修改端口？
A: 编辑 `docker-compose.yml`，修改 `ports` 部分
```yaml
ports:
  - "8080:5700"  # 改为 8080
```

### Q: 如何使用 SSL 证书？
A: 使用 Nginx 反向代理配置（见 nginx-qinglong.conf）

---

## 安全建议

1. **修改默认端口**（可选）
2. **使用强密码**
3. **定期备份数据**
4. **使用 SSL 证书**（生产环境）
5. **限制访问 IP**（如可能）

---

## 需要帮助？

- 官方文档：https://github.com/whyour/qinglong
- 社区讨论：GitHub Issues
