#!/bin/sh
set -e 

##### myql 命令变量
MYSQL_COMM=/usr/local/mysql/bin/mysql
MYSQL_DUMP_COMM=/usr/local/mysql/bin/mysqldump
DATETIME=`date +%Y-%m-%d-%H`
BACK_DIR="/tmp/${DATETIME}"

###  源库信息

S_MYSQL_HOST=172.27.100.151
S_MYSQL_USER='root'
S_MYSQL_PASS='JVrx1LYv9BzVvvLYhac'
S_MYSQL_PORT=3306
S_MYSQL_DBS=(accounting cbox_accounting commodity customer fxs_order  marketing oss tencent_config user)

## 目标库信息

D_MYSQL_HOST=localhost
D_MYSQL_USER='root'
D_MYSQL_PASS='xierui123'
D_MYSQL_PORT=3306
D_MYSQL_DBS=(accounting cbox_accounting commodity customer fxs_order  marketing oss tencent_config user)

### 创建备份表 使用k8s 备份，每次都会重建

mkdir -p ${BACK_DIR}

# 备份源库的数据库，按照库来备份

back(){
  echo "\033[32m#############################备份源数据库${S_MYSQL_HOST}###############################\033[0m"
  if [ -d ${BACK_DIR} ]; then
    for db in ${S_MYSQL_DBS[@]} 
    do 
      echo "\033[32m $db \033[0m 正在备份，文件路径\033[32m ${BACK_DIR}/${db}.sql \033[0m"
      ${MYSQL_DUMP_COMM} -h ${S_MYSQL_HOST} -u${S_MYSQL_USER} -p${S_MYSQL_PASS} -P ${S_MYSQL_PORT} --set-gtid-purged=off  ${db} > ${BACK_DIR}/${db}.sql
      # 处理备份出来40101 的数据问题
      mv ${BACK_DIR}/${db}.sql ${BACK_DIR}/${db}.sql-bak
      grep -v '*.*!.*' ${BACK_DIR}/${db}.sql-bak > ${BACK_DIR}/${db}.sql
      rm -rf ${BACK_DIR}/${db}.sql-bak
    done 
    else 
      echo "备份文件夹不存在"
  fi
}


drop(){
  # 先删除目标数据库
  echo "\033[32m #################################执行删除目标数据库${D_MYSQL_HOST}#################################\033[0m"
  for db in ${D_MYSQL_DBS[@]} 
  do 
    ${MYSQL_COMM} -h ${D_MYSQL_HOST} -u ${D_MYSQL_USER} -p${D_MYSQL_PASS} -P ${D_MYSQL_PORT} -e "drop database ${db}"
    echo "数据库\033[31m $db \033[0m 已删除"
    ${MYSQL_COMM} -h ${D_MYSQL_HOST} -u ${D_MYSQL_USER} -p${D_MYSQL_PASS} -P ${D_MYSQL_PORT} -e "create database ${db}"
    echo "重新创建数据库\033[32m $db \033[0m"
  done 
}

import(){
  # 导入目标数据库
  echo "\033[32m####################################导入目标${D_MYSQL_HOST}数据库中######################\033[0m"
  sql=(`ls ${BACK_DIR}`)
  for i in `seq 0 8`
  do 
    echo "\033[33m ${D_MYSQL_DBS[$i]} \033[0m 库正在导入\033[32m  ${sql[$i]} \033[0m"
    ${MYSQL_COMM} -h ${D_MYSQL_HOST} -P ${D_MYSQL_PORT} -u${D_MYSQL_USER} -p${D_MYSQL_PASS} ${D_MYSQL_DBS[$i]} < ${BACK_DIR}/${sql[i]} 
  done
}

main(){
  back
  drop
  import
}

main
