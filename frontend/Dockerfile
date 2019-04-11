FROM node:8.11

COPY package.json .

RUN npm install --registry=https://registry.npm.taobao.org/

COPY /  .

RUN npm run build

FROM nginx:1.12-alpine

COPY --from=0 dist /var/run/www

ADD  default.conf /etc/nginx/conf.d/default.conf
ADD  mime.types /etc/nginx/conf.d/mime.types

ENTRYPOINT nginx -g "daemon off;"
