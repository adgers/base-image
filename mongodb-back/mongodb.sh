#!/bin/bash



set -e 

DUMP_CMD="/usr/local/mongodb/bin/mongodump"
RESTORE_CMD="/usr/local/mongodb/bin/mongorestore"
DUMP_DIR="/data/mongodb_bak/mongodb_bak_now"
TAR_DIR="/data/mongodb_bak/mongodb_bak_list"
DATE=`date +%Y_%m_%d`
EXPIR_DATE="20"
TAR_BAK="mongodb_bak_$DATE.tar.gz"



# 生产只读账号
DB_USER="nxe-oadbread"
DB_PASS="XKcTFITyGP@PLnoZ"
DB_HOST="172.25.1.8:27017"
DB_NAME="nxe-oadb"

# 预生产mongouser 账号 需要删除所有的表再进行导入
DB_USER_UAT="mongouser"
DB_PASS_UAT="mHpWh6kipX0U6fUK"
DB_HOST_UAT="10.128.1.30:27017"
DB_NAME_UAT="nxe-oadb"



if [ ! -d ${DUMP_DIR} ] && [ ! -d ${TAR_DIR} ];then
  echo "$DUMP_DIR and $TAR_DIR is not exist"
else
  echo "${DUMP_DIR} and ${TAR_DIR} is being created"
  mkdir -p ${DUMP_DIR}
  mkdir -p ${TAR_DIR}
fi

#
cd ${DUMP_DIR}
ls -a 
rm -rf ${DUMP_DIR}/*

mkdir -p ${DUMP_DIR}/${DATE}

# 执行dump 命令进行数据库备份
${DUMP_CMD} -h ${DB_HOST} -u ${DB_USER} -p ${DB_PASS}  -d ${DB_NAME} --authenticationDatabase "admin" -o ${DUMP_DIR}/${DATE} 

# 执行restore 命令进行数据库恢复

${RESTORE_CMD} -h ${DB_HOST_UAT} -u ${DB_USER_UAT} -p ${DB_PASS_UAT} --authenticationDatabase "admin"  --drop -d ${DB_NAME_UAT} $DUMP_DIR/${DATE}/${DB_NAME}
# 进行打包压缩
tar -zcf ${TAR_DIR}/${TAR_BAK} ${DUMP_DIR}/$DATE

