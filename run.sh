#!/bin/bash

service nginx start
cd backend

# 执行数据库迁移（确保新增的 config 应用表已创建）
python manage.py migrate

# 初始化网站配置（如果配置不存在则创建默认配置）
python manage.py init_footer_config

# 根据 CPU 核心数动态设置 worker 数量（推荐 2*CPU+1）
WORKERS=${GUNICORN_WORKERS:-4}
# 生产环境使用 INFO 级别日志
LOG_LEVEL=${GUNICORN_LOG_LEVEL:-INFO}
# 超时时间
TIMEOUT=${GUNICORN_TIMEOUT:-60}

# 使用 sync worker（更稳定，避免 gevent 兼容性问题）
gunicorn --bind 0.0.0.0:8000 \
         --workers $WORKERS \
         --timeout $TIMEOUT \
         --log-level $LOG_LEVEL \
         --access-logfile - \
         --error-logfile - \
         wsgi:application