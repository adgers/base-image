[root@centos7 container-mvn]# cat Dockerfile 
FROM alpine:3.14


# wget https://mirror.azure.cn/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz && tar xf pache-maven-3.6.3-bin.tar.gz

USER root
RUN  sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories  \
 && apk update \
 && apk add --no-cache bash tzdata openjdk8 curl
  
ENV TZ=Asia/Shanghai

ADD maven /usr/local/maven

ENV PATH="/usr/local/maven/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
