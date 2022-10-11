FROM swr.cn-north-4.myhuaweicloud.com/cysd/openjdk:8

ENV TZ=Asia/Shanghai

ADD sources.list /etc/apt/

RUN apt update -y && \
    apt install net-tools -y
