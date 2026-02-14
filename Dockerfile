# 使用 Python 3.6 最后一个版本（3.6.15）
FROM python:3.6.15-slim

COPY . ./stark

WORKDIR /stark

RUN cd /stark/backend && \
    apt-get update -y && \
    apt-get install -y \
        libsasl2-dev \
        python-dev \
        libldap2-dev \
        libssl-dev \
        nginx \
        # Pillow 依赖
        libjpeg-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libopenjp2-7-dev \
        libtiff5-dev \
        libwebp-dev \
        gcc && \
    pip install --upgrade pip setuptools && \
    pip install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mv stark_nginx.conf /etc/nginx/conf.d/

EXPOSE 8080

CMD ["sh", "run.sh"]