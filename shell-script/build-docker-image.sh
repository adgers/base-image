#!/bin/sh
# Absolute path this script is in.
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
JAR_NAME=$1
IMAGE_NAME=$2
IMAGE_TAG=$3
REGISTRY=$4
DOCKER_HUB_USER=$5
DOCKER_HUB_PASSWORD=$6

echo JAR_FILE=$JAR_NAME.jar
TZ=Asia/Shanghai

# 1.创建dockerfile

cat <<EOF > Dockerfile

FROM swr.cn-north-4.myhuaweicloud.com/cysd/openjdk:8

ADD ${JAR_NAME}/target/${JAR_NAME}.jar /app/

# 应用需要暴露的端口
EXPOSE 8080

WORKDIR /app

ENTRYPOINT  ["sh", "-ec", "exec java \${JAVA_OPTS} -Xshare:off -jar ${JAR_NAME}.jar --spring.profiles.active=\${CYSD_ACTIVE_PROFILE}"]

EOF

ls ${JAR_NAME}/target/

#2. 构建docker镜像

# login REGISTRY
docker login ${REGISTRY} -u ${DOCKER_HUB_USER} -p ${DOCKER_HUB_PASSWORD}
# build
docker build -t $IMAGE_NAME:$IMAGE_TAG  $SCRIPT_PATH

# push to registry and delete local image.
docker push "$IMAGE_NAME:$IMAGE_TAG" && docker rmi -f "$IMAGE_NAME:$IMAGE_TAG"
