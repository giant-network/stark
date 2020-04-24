# Stark
简单、灵活、可配置的导航网站
### 特性：
> - [x] 清爽的界面，给用户提供便捷的导航。
> - [x] 可配置的后台管理系统，给管理人员提供快速更新和修改的管理后台。
> - [x] 根据网址名称和简介的全局搜索。
> - [x] 针对单个用户的网址收藏，免登陆。

---
### 快速开始：
> 强烈推荐!  

直接去docker hub 拉取镜像跑容器  
拉取镜像，启动容器：

```
docker run  -p 8818:8080 -d felixglow/stark:V1.0
```
最后访问代理服务器 http://xxx.xxx.xxx.xx:8818 （部署服务器的公网IP加8818端口）就可以看到啦   

访问后台管理系统，添加数据：http://xxx.xxx.xxx.xx:8818/admin/management/  访问密码默认为：giant123  

> 注意，docker方式部署直接用sqlite做数据库，数据量不大，为你省去配置数据库的麻烦。

---

![image](https://github.com/giant-network/stark/blob/master/frontend/public/nav.jpg)


#### 其他方式部署
##### Docker部署
##### 1. 自己构建镜像
如果需要改动代码
改完代码，项目主目录构建镜像（前端代码需要编译，npm run build）
```
docker build -t stark:V1.0 .
```
启动容器
```
docker run  -p 8818:8080 -d stark:V1.0
```
与docker hub方式一样，同样访问 http://xxx.xxx.xxx.xx:8818 

##### 2. 直接部署
backend/settings路径中对应的环境配置，配置mysql连接。  
初始化数据库表执行:
```
python manage.py migrate
```

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
### 技术栈
1. 后端使用python，web框架使用django。  
2. 前端react，使用ant-design的前端框架  

### 如何使用
###### 管理员角色
数据模型分为三个
> - 标签（网址类别）
> - 卡片（网址信息）
> - 卡片菜单 （网址的不同入口，如测试环境、生产环境等）

管理员通过http://部署的访问地址/admin/management/ （例如http://xxx.xxx.xxx.xx:8818/admin/management/ ）访问后台管理系统，添加数据。
> 注意：docker方式部署，后端访问密码默认为：giant123  

![image](https://github.com/giant-network/stark/blob/master/frontend/public/admin.jpg)

前台查看新增的网址信息

###### 普通用户
1. 点击卡片下的菜单，进入该网址的对应入口。  
2. 点击卡片右上角的五角星，就可以收藏到我的收藏☆中，以后可以直接从我的收藏快速找到你想经常访问的地址。(清除浏览器cookie后会失效)
3. 右上角可根据网址名称和描述，全局搜索。

    
