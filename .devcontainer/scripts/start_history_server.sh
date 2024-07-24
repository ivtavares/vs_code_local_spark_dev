/home/glue_user/spark/sbin/start-history-server.sh
sleep 3s
export LOG_FILE=`ls /home/glue_user/spark/logs`
export TERM=xterm
watch -n 5 cat /home/glue_user/spark/logs/$LOG_FILE 