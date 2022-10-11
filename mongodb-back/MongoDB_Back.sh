#!/bin/bash

set -e 
# Author xierui
# Email 99106949@qq.com


# Backup directory

DUMP_CMD="/usr/local/mongodb/bin/mongodump"
DUMP_DIR="/data/mongodb_bak/mongodb_bak_now"
TAR_DIR="/data/mongodb_bak/mongodb_bak_list"
DATE=`date +"%Y%m%d-%H%M"`

TAR_BACK="mongodb_back_$DATE.tar.gz"
DAYS=60

 
#DB_USER=
#DB_PASS=
#DB_HOST=
#DB_PORT=

# Create backup directory automatically
if [ ! -d $DUMP_DIR ];then
  echo "$DUMP_DIR not exsits"
  echo "$DUMP_DIR is being create"
  mkdir -p $DUMP_DIR  
fi

if [ ! -d $TAR_DIR ]; then
  echo "$TAR_DIR not exsits"
  echo "$TAR_DIR is being create"
  mkdir -p $TAR_DIR
fi

echo -e "\nThe backup directory is $DUMP_DIR , backup compressed directory is  $TAR_DIR "

if [ ! -f $DUMP_CMD ];then
  echo "Please download the binary mongodb and rename it put in /usr/local/mongodb， \
        Mongodb download link 'https://www.mongodb.com/try/download'"
  exit 101
fi

echo -e "The backup command directory is in $DUMP_CMD \n \n"

read -p "Please enter your mongodb connection information in order: DB_USER DB_PASS DB_HOST DB_PORT DB_NAME: " DB_USER DB_PASS DB_HOST DB_PORT DB_NAME
echo "your mongo info DB_USER=$DB_USER DB_PASS=$DB_PASS DB_HOST=$DB_HOST DB_PORT=$DB_PORT DB_NAME=$DB_NAME"

read -p "Do you want to continue (y/n) " confirm
if [ $confirm = y ];then
  true
else
  exit 99
fi

cd $DUMP_DIR
rm -rf $DUMP_DIR/*
$DUMP_CMD -h $DB_HOST:$DB_PORT -u $DB_USER -p $DB_PASS -d $DB_NAME --authenticationDatabase "admin"

tar -zcvf $TAR_DIR/$TAR_BACK $DUMP_DIR/dump/*



# Auto delete 60 days ago data
find $TAR_DIR/ -mtime +$DAYS -delete
exit 0

#vi /etc/crontab
#每星期六晚上20:30开始执行MongoDB数据库备份脚本
#30 20 * * 6 root /data/mongodb_bak/MongoDB_bak.sh

#恢复全部数据库
#mongorestore -u $DB_USER -p $DB_PASS -h $DB_HOST:$DB_PORT --authenticationDatabase "admin" --noIndexRestore --dir /data/mongodb_bak/mongodb_bak_now/path/
#恢复单个数据库
#mongorestore -u $DB_USER -p $DB_PASS -h $DB_HOST:$DB_PORT --authenticationDatabase "admin" --noIndexRestore -d db --dir /data/mongodb_bak/mongodb_bak_now/path
