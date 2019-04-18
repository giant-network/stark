# Stark
简单、灵活、可配置的导航网站
### 特性：
> - [x] 清爽的界面，给用户提供便捷的导航。
> - [x] 可配置的后台管理系统，给管理人员提供快速更新和修改的管理后台。
> - [x] 根据网址名称和简介的全局搜索。
> - [x] 针对单个用户的网址收藏，免登陆。

---
![image](https://github.com/giant-network/stark/blob/master/frontend/public/nav.jpg)

### 使用：

1. 后端使用python，web框架使用django。  
backend/settings路径中对应的环境配置，配置mysql连接。  
初始化数据库表执行:
```
python manage.py migrate
```
2. 前端react，使用ant-design的前端框架  


#### 如何部署
##### 直接部署


1. 后端在backend/路径下执行 
```
python manage.py runserver
```
根据环境变量中ENV的值（test/dev/prod）然后取settings中对应的环境配置

2. 前端可以在frontend/config/env.js中配置proxy后端的地址，可以直接
```
npm run start:[test/dev/prod]
```
，或者npm run build编译后通过nginx做代理
###### nginx 代理示例
```
server {
    gzip on;
    gzip_min_length 1k;
    gzip_buffers 4 16k;
    gzip_http_version 1.0;
    gzip_comp_level 2;
    gzip_types text/plain application/x-javascript text/css application/xml application/javascript;
    gzip_vary on;


    listen       80;
    server_name  localhost;

    location / {
        root   /var/run/www;
        index  index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://192.168.1.1:8080;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_set_header   Host              $http_host;
        proxy_set_header   X-Real-IP         $remote_addr;
    }

    location /media/ {
        proxy_pass http://192.168.1.1:8080/media/;
    }

    location /static/ {
        proxy_pass http://192.168.1.1:8080/static/;
    }

    location /admin/ {
        proxy_pass http://192.168.1.1:8080/admin/;
    }
}
```
##### Docker部署
数据库需要自己事先创建好
###### 1. 后端

在backend路径构建镜像:
```
docker build -t stark:backend1.0 .
```
启动后端镜像，示例：

```
docker run -e 'ENV=dev' -p 8080:8080 -v /home/data/stark/media:/stark/media/ -d stark:backend1.0
```
###### 2. 前端

在frontend路径构建镜像：
```
docker build -t stark:frontend1.0 .
```
启动前端镜像，示例：

```
docker run --name stark-frontend -p 8001:8088 -d stark:frontend1.0
```
通过nginx代理访问前端和后端服务器,最后访问代理服务器 http://xxx.xxx.xxx.xx:8001就可以看到啦

### 如何使用
###### 管理员角色
数据模型分为三个
> - 标签（网址类别）
> - 卡片（网址信息）
> - 卡片菜单 （网址的不同入口，如测试环境、生产环境等）

管理员通过http://xxx.xxx.xxx.xx:8001/admin/management/ 访问后台管理系统，添加数据。  
前台查看新增的网址信息

###### 普通用户
1. 点击卡片下的菜单，进入该网址的对应入口。  
2. 点击卡片右上角的五角星，就可以收藏到我的收藏☆中，以后可以直接从我的收藏快速找到你想经常访问的地址。(清除浏览器cookie后会失效)
3. 右上角可根据网址名称和描述，全局搜索。

    
