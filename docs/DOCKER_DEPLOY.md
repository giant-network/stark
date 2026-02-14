# Docker 部署检查清单

## 当前部署方式确认

✅ **依然满足打包成一个镜像的条件！**

项目采用前后端打包成一个 Docker 镜像的方式，用户可以直接从 Docker Hub 拉取镜像运行。

## 部署架构

```
Docker 容器
├── Nginx (端口 8080)
│   ├── 前端静态文件 (/stark/frontend/dist)
│   └── 反向代理后端 API
├── Gunicorn + Django (端口 8000)
│   ├── API 接口
│   ├── Admin 后台
│   └── 静态文件服务
└── SQLite 数据库 (backend/db.sqlite3)
```

## 新增功能对部署的影响

### 1. 数据库变更
- ✅ 新增了 `config` 应用
- ✅ 新增了 `config_siteconfig` 表
- ✅ 使用 SQLite，无需额外配置

### 2. 启动脚本更新
已在 `run.sh` 中添加：
```bash
# 执行数据库迁移（确保新增的 config 应用表已创建）
python manage.py migrate

# 初始化网站配置（如果配置不存在则创建默认配置）
python manage.py init_footer_config
```

### 3. 前端代码变更
- ✅ 前端代码已编译到 `frontend/dist` 目录
- ✅ 新增的配置功能通过 API 调用，无需额外配置
- ✅ 收藏功能使用 localStorage，无需服务端支持

## 部署前检查清单

### ⚠️ 关键步骤：前端必须先编译

**前端静态文件的放置时机**：
- 前端文件通过 Dockerfile 中的 `COPY . ./stark` 复制到镜像
- 这意味着 `frontend/dist` 目录必须在构建镜像之前就存在
- **必须先执行 `npm run build` 编译前端，再执行 `docker build`**

### 必须完成的步骤（按顺序）

1. **前端编译**（必须第一步）
   ```bash
   cd frontend
   npm install  # 如果是首次构建
   npm run build
   cd ..
   ```
   ✅ 确认 `frontend/dist` 目录存在且包含编译后的文件
   ```bash
   ls -la frontend/dist/
   # 应该看到 index.html, static/ 等文件
   ```

2. **构建 Docker 镜像**
   ```bash
   docker build -t felixglow/stark:V2.0 .
   ```
   此时会将整个项目（包括 frontend/dist）复制到镜像中

3. **测试镜像**
   ```bash
   docker run -p 8818:8080 -d --name stark-test felixglow/stark:V2.0
   docker logs -f stark-test
   ```

### 文件复制流程

```
构建机器
├── frontend/
│   ├── src/           ← 源代码
│   └── dist/          ← npm run build 生成（必须存在）
├── backend/
└── Dockerfile

↓ docker build (COPY . ./stark)

Docker 镜像
└── /stark/
    ├── frontend/
    │   └── dist/      ← 被复制进镜像
    ├── backend/
    └── ...
```

### 常见错误

❌ **错误做法**：直接构建镜像，没有先编译前端
```bash
docker build -t stark:V2.0 .  # 错误！frontend/dist 不存在
```
结果：镜像中没有前端文件，访问页面 404

✅ **正确做法**：先编译前端，再构建镜像
```bash
cd frontend && npm run build && cd ..
docker build -t stark:V2.0 .
```

## 构建和发布流程

### 重要提醒

⚠️ **前端文件是在构建镜像之前放入的，不是在镜像构建过程中编译的！**

### 1. 构建镜像

```bash
# 第一步：编译前端（必须！）
cd frontend
npm install  # 如果是首次构建
npm run build  # 编译生成 dist 目录
cd ..

# 第二步：确认 dist 目录存在
ls -la frontend/dist  # 应该看到 index.html 等文件

# 第三步：构建 Docker 镜像
docker build -t felixglow/stark:V2.0 .
```

**镜像构建说明**：
- `COPY . ./stark` 会复制当前目录所有文件
- `.dockerignore` 文件排除了不必要的文件（源代码、node_modules 等）
- 只有 `frontend/dist` 目录会被复制到镜像
- 这样可以大幅减小镜像体积

Dockerfile 中的 `COPY . ./stark` 会将整个项目目录（包括 `frontend/dist`）复制到镜像中。因此：
- 必须先在本地编译前端：`npm run build`
- 然后再构建 Docker 镜像：`docker build`

### 1. 构建镜像（完整步骤）

```bash
# 步骤1: 编译前端（必须）
cd frontend
npm install          # 如果是首次构建或依赖有更新
npm run build        # 编译生成 dist 目录
cd ..

# 步骤2: 验证前端文件已生成
ls -la frontend/dist/
# 应该看到：
# - index.html
# - static/
# - 其他静态资源

# 步骤3: 构建 Docker 镜像
docker build -t felixglow/stark:V2.0 .

# 构建过程说明：
# 1. COPY . ./stark        ← 此时会复制 frontend/dist 到镜像
# 2. 安装 Python 依赖
# 3. 配置 Nginx
```

### 2. 测试镜像

```bash
# 运行容器
docker run -p 8818:8080 -d --name stark-test felixglow/stark:V2.0

# 查看日志
docker logs -f stark-test

# 测试访问
curl http://localhost:8818
curl http://localhost:8818/api/config/site/
curl http://localhost:8818/api/config/footer/

# 停止并删除测试容器
docker stop stark-test
docker rm stark-test
```

### 3. 推送到 Docker Hub

```bash
# 登录 Docker Hub
docker login

# 推送镜像
docker push felixglow/stark:V2.0

# 可选：打标签为 latest
docker tag felixglow/stark:V2.0 felixglow/stark:latest
docker push felixglow/stark:latest
```

## 用户使用方式

### 快速启动（推荐）

```bash
# 拉取并运行最新版本
docker run -p 8818:8080 -d felixglow/stark:V2.0

# 或使用 latest 标签
docker run -p 8818:8080 -d felixglow/stark:latest
```

### 访问地址

- 前端页面: http://服务器IP:8818
- 后台管理: http://服务器IP:8818/admin/
- 默认密码: giant123

### 配置网站信息

1. 访问后台管理: http://服务器IP:8818/admin/
2. 登录（默认密码: giant123）
3. 进入 Config → Site configs
4. 编辑配置项：
   - 网站标题（浏览器标签页）
   - 顶部标题（导航栏）
   - 导航语（首页描述）
   - 页脚链接和版权信息
5. 保存后刷新前端页面即可看到效果

## 数据持久化（可选）

如果需要持久化数据库和媒体文件：

```bash
docker run -p 8818:8080 -d \
  -v /path/to/data:/stark/backend/db.sqlite3 \
  -v /path/to/media:/stark/backend/media \
  felixglow/stark:V2.0
```

## 环境变量配置（可选）

可以通过环境变量调整 Gunicorn 配置：

```bash
docker run -p 8818:8080 -d \
  -e GUNICORN_WORKERS=8 \
  -e GUNICORN_TIMEOUT=120 \
  -e GUNICORN_LOG_LEVEL=DEBUG \
  felixglow/stark:V2.0
```

## 新版本特性

### V2.0 新增功能

1. **网站配置管理**
   - 支持动态配置网站标题、导航语、页脚信息
   - 无需修改代码，后台直接配置

2. **收藏功能优化**
   - 从 Cookie 迁移到 localStorage
   - 浏览器关闭后数据不丢失
   - 智能标签位置：有收藏时显示在第一个，无收藏时显示在最后

3. **前端代码优化**
   - 修复了多个代码质量问题
   - 提升了性能和安全性
   - 添加了操作反馈提示

4. **后端优化**
   - 修复了 Admin 删除 Card 导致项目无法访问的 bug
   - 修复了代码注入漏洞
   - 优化了 Nginx 和 Gunicorn 配置

## 镜像体积优化

通过 `.dockerignore` 文件，我们排除了以下内容：
- 前端源代码（只保留编译后的 dist）
- node_modules（不需要）
- Git 历史记录
- IDE 配置文件
- Python 缓存文件
- 文档文件

**优化效果**：
- 未优化：可能 500MB+
- 优化后：预计 200-300MB

## 常见问题

### Q: 为什么必须先编译前端？
A: Dockerfile 使用 `COPY . ./stark` 复制文件，不会在镜像构建时编译前端。必须在构建镜像前手动编译好 `frontend/dist` 目录。

### Q: 如果忘记编译前端会怎样？
A: 镜像中不会有 `frontend/dist` 目录，Nginx 无法找到前端文件，访问时会出现 404 错误。

### Q: 升级到 V2.0 后，旧数据会丢失吗？
A: 不会。新版本完全兼容旧版本的数据库结构，只是新增了配置表。

### Q: 如何从 V1.0 升级到 V2.0？
A: 直接拉取新镜像运行即可，启动时会自动执行数据库迁移。

### Q: 配置数据存储在哪里？
A: 存储在 SQLite 数据库的 `config_siteconfig` 表中。

### Q: 如何备份数据？
A: 备份 `backend/db.sqlite3` 文件和 `backend/media` 目录即可。

## 总结

✅ **完全满足打包成一个镜像的条件**

- 前后端代码都在镜像中
- 使用 SQLite，无需外部数据库
- 启动脚本自动执行迁移和初始化
- 用户只需一条命令即可运行
- 所有新功能都已集成，无需额外配置
