#!/bin/bash


ip="1.1.1.1"
email="rui.xie@nx-engine.com"


while true
do 
  ping -c10 $ip > /dev/null 2>&1
  if [ $? != "0" ];then
    python /root/mail.py $email "$ip is down" "$ip is down"
  fi
  sleep 30
done
