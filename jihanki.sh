#!/bin/sh
update() {
  echo `openssl sha256 -r $1 | awk '{print $1}'`
}
if [ $# -ne 2 ];
then
  usage
  exit 1
fi

INTERVAL=1 #監視間隔, 秒で指定
no=0
last=`update $1`
while true;
do
  sleep $INTERVAL
  current=`update $1`
  if [ "$last" != "$current" ];
  then
    nowdate=`date '+%Y/%m/%d'`
    nowtime=`date '+%H:%M:%S'`
    echo "no:$no\tdate:$nowdate\ttime:$nowtime\tfile:$1"
    eval $2
    last=$current
    no=`expr $no + 1`
  fi  
done
