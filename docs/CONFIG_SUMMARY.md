# 网站配置功能总结

## 功能概述

实现了网站的动态配置功能，管理员可以在 Django Admin 后台修改网站的标题、导航语、页脚信息等，无需修改代码即可更新网站内容。

## 配置项说明

### 1. 网站基础配置

| 配置项 | 字段名 | 说明 | 默认值 |
|--------|--------|------|--------|
| 网站标题 | site_title | 浏览器标签页显示的标题 | Stark |
| 顶部标题 | site_header | 顶部导航栏和侧边栏显示的标题 | Stark Dashboard |
| 导航语 | site_description | 首页顶部的描述文字 | Stark 集合了众多站点的入口，提供一站式的便捷访问，快试试把他设为你的主页吧。 |

### 2. 页脚配置

| 配置项 | 字段名 | 说明 | 默认值 |
|--------|--------|------|--------|
| 链接1文本 | footer_link1_text | 第一个页脚链接的文本 | Pro 首页 |
| 链接1地址 | footer_link1_url | 第一个页脚链接的URL | https://pro.ant.design |
| 链接2文本 | footer_link2_text | 第二个页脚链接的文本 | GitHub |
| 链接2地址 | footer_link2_url | 第二个页脚链接的URL | https://github.com/ant-design/ant-design-pro |
| 链接3文本 | footer_link3_text | 第三个页脚链接的文本 | Ant Design |
| 链接3地址 | footer_link3_url | 第三个页脚链接的URL | https://ant.design |
| 版权信息 | footer_copyright | 页脚版权信息 | Copyright © 2018 蚂蚁金服体验技术部出品 |

## 技术实现

### 后端实现

#### 1. 数据模型 (apps/config/models.py)

```python
class SiteConfig(models.Model):
    # 网站基础配置
    site_title = models.CharField(max_length=100, default='Stark', verbose_name='网站标题')
    site_header = models.CharField(max_length=100, default='Stark Dashboard', verbose_name='顶部标题')
    site_description = models.TextField(
        default='Stark 集合了众多站点的入口，提供一站式的便捷访问，快试试把他设为你的主页吧。',
        verbose_name='导航语'
    )
    
    # 页脚配置
    footer_link1_text = models.CharField(max_length=50, default='Pro 首页', verbose_name='链接1文本')
    footer_link1_url = models.URLField(default='https://pro.ant.design', verbose_name='链接1地址')
    footer_link2_text = models.CharField(max_length=50, default='GitHub', verbose_name='链接2文本')
    footer_link2_url = models.URLField(
        default='https://github.com/ant-design/ant-design-pro',
        verbose_name='链接2地址'
    )
    footer_link3_text = models.CharField(max_length=50, default='Ant Design', verbose_name='链接3文本')
    footer_link3_url = models.URLField(default='https://ant.design', verbose_name='链接3地址')
    footer_copyright = models.CharField(
        max_length=200,
        default='Copyright © 2018 蚂蚁金服体验技术部出品',
        verbose_name='版权信息'
    )
    
    # 软删除支持
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    
    class Meta:
        db_table = 'config_siteconfig'
        verbose_name = '网站配置'
        verbose_name_plural = '网站配置'
```

#### 2. API 接口

**网站基础配置接口**
```
GET /api/config/site/

返回格式：
{
    "title": "Stark",
    "header": "Stark Dashboard",
    "description": "Stark 集合了众多站点的入口..."
}
```

**页脚配置接口**
```
GET /api/config/footer/

返回格式：
{
    "link1": {
        "name": "Pro 首页",
        "url": "https://pro.ant.design"
    },
    "link2": {
        "name": "GitHub",
        "url": "https://github.com/ant-design/ant-design-pro"
    },
    "copyright": "Copyright © 2018 蚂蚁金服体验技术部出品"
}
```

#### 3. 初始化命令

```bash
python manage.py init_footer_config
```

该命令会创建默认配置（如果不存在），支持幂等性，多次执行不会重复创建。

### 前端实现

#### 1. 配置获取

各组件在 `componentDidMount` 时调用 API 获取配置：

```javascript
fetchSiteConfig = () => {
  fetch('/api/config/site/')
    .then(response => response.json())
    .then(data => {
      this.setState({
        siteTitle: data.title || 'Stark',
        siteHeader: data.header || 'Stark Dashboard',
        siteDescription: data.description || '默认描述'
      });
    })
    .catch(error => {
      console.error('获取配置失败:', error);
      // 使用默认值
    });
};
```

#### 2. 配置应用位置

| 配置项 | 应用位置 | 组件文件 |
|--------|----------|----------|
| site_title | 浏览器标签页标题 | BasicLayout.js |
| site_header | 顶部导航栏标题 | TopNavHeader/index.js |
| site_header | 侧边栏标题 | SiderMenu/SiderMenu.js |
| site_description | 首页导航语 | Dashboard/HomePage.js |
| footer_* | 页脚链接和版权 | layouts/Footer.js |

#### 3. 样式优化

修改了 `TopNavHeader/index.less`，支持长标题显示：

```less
.logo h1 {
  width: auto;
  overflow: visible;
  white-space: nowrap;
  vertical-align: middle;
}
```

## 使用步骤

### 1. 初始化配置（首次部署）

```bash
cd backend

# 执行数据库迁移
python manage.py makemigrations config
python manage.py migrate

# 初始化配置数据
python manage.py init_footer_config
```

### 2. 修改配置

1. 登录 Django Admin 后台：`http://服务器IP:8818/admin/`
2. 使用默认密码登录（giant123）
3. 进入 "Config" → "Site configs"
4. 点击配置记录进行编辑
5. 修改需要的配置项
6. 点击保存
7. 刷新前端页面即可看到效果

### 3. 验证配置

- [ ] 浏览器标签页标题是否更新
- [ ] 顶部导航栏标题是否更新
- [ ] 侧边栏标题是否更新
- [ ] 首页导航语是否更新
- [ ] 页脚链接和版权信息是否更新

## 容错处理

### 1. 默认值机制

所有配置项都有默认值，即使 API 调用失败或数据库无数据，也能正常显示。

```javascript
// 前端默认值
this.state = {
  siteTitle: 'Stark',
  siteHeader: 'Stark Dashboard',
  siteDescription: 'Stark 集合了众多站点的入口...'
};

// 后端默认值
site_title = models.CharField(max_length=100, default='Stark')
```

### 2. 错误处理

```javascript
.catch(error => {
  console.error('获取配置失败:', error);
  // 使用 state 中的默认值，不影响页面显示
});
```

### 3. 软删除支持

配置记录支持软删除（`is_deleted` 字段），不会真正从数据库删除，可以恢复。

## 扩展建议

如需添加新的配置项：

### 1. 后端修改

```python
# 在 SiteConfig 模型中添加字段
class SiteConfig(models.Model):
    # ... 现有字段
    new_field = models.CharField(max_length=100, default='默认值', verbose_name='新字段')
```

### 2. 数据库迁移

```bash
python manage.py makemigrations config
python manage.py migrate
```

### 3. 更新 API 视图

```python
# 在 views.py 中返回新字段
def site_config(request):
    config = SiteConfig.objects.filter(is_deleted=False).first()
    return JsonResponse({
        'title': config.site_title if config else 'Stark',
        'header': config.site_header if config else 'Stark Dashboard',
        'new_field': config.new_field if config else '默认值',  # 新增
    })
```

### 4. 前端使用

```javascript
fetchSiteConfig = () => {
  fetch('/api/config/site/')
    .then(response => response.json())
    .then(data => {
      this.setState({
        newField: data.new_field || '默认值'
      });
    });
};
```

### 5. 更新初始化命令

```python
# 在 init_footer_config.py 中添加新字段的初始化
SiteConfig.objects.get_or_create(
    id=1,
    defaults={
        # ... 现有字段
        'new_field': '默认值',
    }
)
```

## 相关文件

### 后端文件
- `backend/apps/config/models.py` - 数据模型定义
- `backend/apps/config/views.py` - API 视图实现
- `backend/apps/config/urls.py` - URL 路由配置
- `backend/apps/config/admin.py` - Admin 后台配置
- `backend/apps/config/management/commands/init_footer_config.py` - 初始化命令
- `backend/apps/config/migrations/0001_initial.py` - 数据库迁移文件

### 前端文件
- `frontend/src/layouts/BasicLayout.js` - 浏览器标题
- `frontend/src/components/TopNavHeader/index.js` - 顶部导航栏
- `frontend/src/components/TopNavHeader/index.less` - 顶部导航栏样式
- `frontend/src/components/SiderMenu/SiderMenu.js` - 侧边栏
- `frontend/src/pages/Dashboard/HomePage.js` - 首页导航语
- `frontend/src/layouts/Footer.js` - 页脚

## 注意事项

1. **配置修改后需要刷新** - 前端页面需要刷新才能看到配置更新
2. **建议只保留一条配置** - 避免多条配置记录导致混淆
3. **修改配置不需要重启** - 配置存储在数据库，修改后立即生效
4. **支持中文配置** - 所有配置项都支持中文内容
5. **URL 自动验证** - URL 字段会自动验证格式是否正确
6. **容器启动自动初始化** - Docker 容器启动时会自动执行初始化命令

## 常见问题

### Q: 修改配置后前端没有更新？
A: 需要刷新浏览器页面，配置是在页面加载时获取的。

### Q: 可以添加多条配置记录吗？
A: 可以，但系统只会使用第一条未删除的记录。建议只保留一条。

### Q: 如何恢复默认配置？
A: 在 Admin 后台编辑配置，将各字段改回默认值，或者删除配置记录后重新运行初始化命令。

### Q: 配置数据存储在哪里？
A: 存储在 SQLite 数据库的 `config_siteconfig` 表中。

### Q: Docker 部署时配置会丢失吗？
A: 如果使用 Volume 挂载数据库文件，配置不会丢失。建议挂载 `/stark/backend` 目录。

### Q: 可以通过 API 修改配置吗？
A: 当前只提供了查询接口，修改需要通过 Admin 后台。如需 API 修改，可以自行扩展。

## 版本历史

- **V2.0** - 首次实现网站配置功能
  - 支持网站标题、顶部标题、导航语配置
  - 支持页脚链接和版权信息配置
  - 提供初始化命令
  - 支持软删除
