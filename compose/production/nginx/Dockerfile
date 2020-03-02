FROM nginx:stable-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk update && apk add --no-cache certbot

RUN rm /etc/nginx/conf.d/default.conf

COPY ./compose/production/nginx/yzp_blog.conf /etc/nginx/conf.d/yzp_blog.conf
