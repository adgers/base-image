FROM  node:14.18.3

ADD sources.list /etc/apt/

ENV TZ=Asia/Shanghai

RUN apt update -y \
  && apt install net-tools \
  && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo "Asia/Shanghai" > /etc/timezone

