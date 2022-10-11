FROM nginx:1.22-alpine

# change to Asia/Shanghai timezone 

RUN sed -i "s#dl-cdn.alpinelinux.org#mirrors.aliyun.com#g" /etc/apk/repositories \
    && apk add tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone
ADD nginx.conf /etc/nginx/ 
ADD default.conf /etc/nginx/conf.d/
