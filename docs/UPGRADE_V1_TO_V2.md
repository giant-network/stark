# 从 V1.0 升级到 V2.0 迁移指南

## 迁移场景

如果你之前运行的是 V1.0 版本，数据存储在容器内部（没有挂载 volume），现在需要升级到 V2.0 并保留数据。

## 数据位置

V1.0 容器内的数据位置：
- 数据库：`/stark/backend/db.sqlite3`
- 图片文件：`/stark/backend/media/`

## 迁移步骤

### 方案1：从旧容器复制数据到新容器（推荐）

#### 步骤1：从旧容器导出数据

```bash
# 假设旧容器名称为 stark-v1（如果不知道，用 docker ps -a 查看）
OLD_CONTAINER="stark-v1"

# 创建临时目录存放数据
mkdir -p ~/stark_backup
cd ~/stark_backup

# 从旧容器复制数据库
docker cp ${OLD_CONTAINER}:/stark/backend/db.sqlite3 ./db.sqlite3

# 从旧容器复制媒体文件
docker cp ${OLD_CONTAINER}:/stark/backend/media ./media

# 确认文件已复制
ls -lh
# 应该看到 db.sqlite3 和 media/ 目录
```

#### 步骤2：启动新容器并挂载数据

```bash
# 停止旧容器（不要删除，以防万一）
docker stop ${OLD_CONTAINER}

# 启动 V2.0 容器，挂载数据目录
docker run -p 8818:8080 -d \
  --name stark-v2 \
  -v ~/stark_backup/db.sqlite3:/stark/backend/db.sqlite3 \
  -v ~/stark_backup/media:/stark/backend/media \
  felixglow/stark:V2.0

# 查看日志，确认启动成功
docker logs -f stark-v2
```

#### 步骤3：验证数据

```bash
# 访问网站
curl http://localhost:8818

# 检查数据是否正常
# 1. 访问前端，查看之前添加的卡片是否还在
# 2. 访问后台 http://localhost:8818/admin/
# 3. 检查图片是否正常显示
```

#### 步骤4：确认无误后删除旧容器

```bash
# 确认新容器运行正常后，删除旧容器
docker rm ${OLD_CONTAINER}
```

---

### 方案2：使用 docker commit 保存数据（备选）

如果方案1遇到问题，可以使用这个方法：

#### 步骤1：从旧容器创建新镜像（包含数据）

```bash
OLD_CONTAINER="stark-v1"

# 提交旧容器为新镜像（包含数据）
docker commit ${OLD_CONTAINER} stark:v1-with-data

# 停止旧容器
docker stop ${OLD_CONTAINER}
```

#### 步骤2：从包含数据的镜像启动临时容器

```bash
# 启动临时容器
docker run -d --name stark-temp stark:v1-with-data tail -f /dev/null

# 导出数据
mkdir -p ~/stark_backup
docker cp stark-temp:/stark/backend/db.sqlite3 ~/stark_backup/
docker cp stark-temp:/stark/backend/media ~/stark_backup/

# 停止并删除临时容器
docker stop stark-temp
docker rm stark-temp
```

#### 步骤3：启动 V2.0 容器并挂载数据

```bash
# 启动 V2.0 容器
docker run -p 8818:8080 -d \
  --name stark-v2 \
  -v ~/stark_backup/db.sqlite3:/stark/backend/db.sqlite3 \
  -v ~/stark_backup/media:/stark/backend/media \
  felixglow/stark:V2.0
```

---

### 方案3：在线迁移（零停机）

如果需要零停机迁移：

#### 步骤1：在不同端口启动 V2.0

```bash
# 先导出旧容器数据
OLD_CONTAINER="stark-v1"
mkdir -p ~/stark_backup
docker cp ${OLD_CONTAINER}:/stark/backend/db.sqlite3 ~/stark_backup/
docker cp ${OLD_CONTAINER}:/stark/backend/media ~/stark_backup/

# 在不同端口启动 V2.0（例如 8819）
docker run -p 8819:8080 -d \
  --name stark-v2 \
  -v ~/stark_backup/db.sqlite3:/stark/backend/db.sqlite3 \
  -v ~/stark_backup/media:/stark/backend/media \
  felixglow/stark:V2.0

# 测试 V2.0 是否正常
curl http://localhost:8819
```

#### 步骤2：切换流量

```bash
# 确认 V2.0 正常后，停止 V1.0
docker stop ${OLD_CONTAINER}

# 重新启动 V2.0 在 8818 端口
docker stop stark-v2
docker rm stark-v2

docker run -p 8818:8080 -d \
  --name stark-v2 \
  -v ~/stark_backup/db.sqlite3:/stark/backend/db.sqlite3 \
  -v ~/stark_backup/media:/stark/backend/media \
  felixglow/stark:V2.0
```

---

## 数据迁移验证清单

迁移完成后，请验证以下内容：

- [ ] 所有标签（Tag）是否正常显示
- [ ] 所有卡片（Card）是否正常显示
- [ ] 卡片的图片是否正常加载
- [ ] 卡片菜单是否正常显示
- [ ] 搜索功能是否正常
- [ ] 收藏功能是否正常（注意：收藏数据在浏览器 localStorage，不在数据库）
- [ ] 后台管理是否可以登录
- [ ] 后台可以正常添加/编辑/删除数据
- [ ] 新增的配置功能是否正常（Config → Site configs）

## V2.0 新功能配置

迁移完成后，可以配置新功能：

### 1. 配置网站信息

访问后台管理：http://服务器IP:8818/admin/

进入 Config → Site configs，配置：
- 网站标题（浏览器标签页）
- 顶部标题（导航栏）
- 导航语（首页描述）
- 页脚链接和版权信息

### 2. 体验新功能

- 收藏功能优化：数据保存在 localStorage，浏览器关闭后不丢失
- 智能标签位置：有收藏时"我的收藏"显示在第一个，无收藏时显示在最后
- 操作反馈：收藏/取消收藏时有提示信息

## 数据持久化建议

为了避免将来再次遇到数据迁移问题，建议使用 volume 挂载：

```bash
# 创建持久化目录
mkdir -p ~/stark_data/db
mkdir -p ~/stark_data/media

# 复制现有数据
cp ~/stark_backup/db.sqlite3 ~/stark_data/db/
cp -r ~/stark_backup/media/* ~/stark_data/media/

# 启动容器时挂载
docker run -p 8818:8080 -d \
  --name stark \
  -v ~/stark_data/db/db.sqlite3:/stark/backend/db.sqlite3 \
  -v ~/stark_data/media:/stark/backend/media \
  --restart unless-stopped \
  felixglow/stark:V2.0
```

这样以后升级版本时，只需要：
```bash
docker stop stark
docker rm stark
docker run -p 8818:8080 -d \
  --name stark \
  -v ~/stark_data/db/db.sqlite3:/stark/backend/db.sqlite3 \
  -v ~/stark_data/media:/stark/backend/media \
  --restart unless-stopped \
  felixglow/stark:V2.1  # 新版本
```

## 回滚方案

如果 V2.0 出现问题，可以快速回滚到 V1.0：

```bash
# 停止 V2.0
docker stop stark-v2
docker rm stark-v2

# 重新启动 V1.0（如果还没删除）
docker start ${OLD_CONTAINER}

# 或者重新运行 V1.0
docker run -p 8818:8080 -d \
  --name stark-v1 \
  -v ~/stark_backup/db.sqlite3:/stark/backend/db.sqlite3 \
  -v ~/stark_backup/media:/stark/backend/media \
  felixglow/stark:V1.0
```

## 常见问题

### Q: 如何找到旧容器的名称？
```bash
docker ps -a | grep stark
```

### Q: 如果旧容器已经停止了怎么办？
A: 没关系，`docker cp` 命令对停止的容器也有效。

### Q: 数据库迁移会自动执行吗？
A: 是的，V2.0 容器启动时会自动执行 `python manage.py migrate`，会自动创建新的配置表。

### Q: V1.0 的数据会丢失吗？
A: 不会，V2.0 完全兼容 V1.0 的数据结构，只是新增了配置表。

### Q: 如果忘记备份就删除了旧容器怎么办？
A: 如果容器已删除且没有备份，数据将无法恢复。建议在删除前一定要先备份数据。

### Q: 挂载 volume 后，容器内的文件会被覆盖吗？
A: 是的，挂载的本地文件会覆盖容器内的文件。所以要确保挂载的是正确的数据文件。

### Q: 可以直接在旧容器上升级吗？
A: 不建议。Docker 的最佳实践是创建新容器，而不是修改现有容器。

## 技术支持

如果迁移过程中遇到问题，可以：
1. 查看容器日志：`docker logs stark-v2`
2. 进入容器检查：`docker exec -it stark-v2 bash`
3. 检查数据库：`docker exec -it stark-v2 sqlite3 /stark/backend/db.sqlite3`
