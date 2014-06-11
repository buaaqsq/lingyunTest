#!/usr/bin/python

class HDFSUrl:
	ip_url = ''
	
class PATH:	
	SOFTWARE_SHARE_BIN_DIR="/usr/opt/"
	SOFTWARE_LOCAL_BIN_DIR="/usr/local/"
	SOFTWARE_TAR_DIR="/root/tmp/software/"
	CONF_DIR="/etc/conf/"
	CONF_RUN_DIR=CONF_DIR+".self/"
	RUN_INFO_DIR="/var/QX/"
	HADOOP_DEV_HOME=SOFTWARE_SHARE_BIN_DIR+"hadoop/"
	HBASE_DEV_HOME=SOFTWARE_SHARE_BIN_DIR+"hbase/"
	ZOOKEEPER_DEV_HOME=SOFTWARE_SHARE_BIN_DIR+"zookeeper/"
	HADOOP_LOG_DIR=RUN_INFO_DIR+"hadoop/log"
	HADOOP_PID_DIR=RUN_INFO_DIR+"hadoop/pid"
	HADOOP_CONF_DIR=CONF_DIR+"hadoop/conf"
	HADOOP_TMP_DIR="/hadoop/tmp"
	HADOOP_DATA_DIR="/hadoop/dfs/data"
	HADOOP_NAME_DIR="/hadoop/dfs/name"
	PIG_HOME=SOFTWARE_LOCAL_BIN_DIR+"pig/"
	hive_HOME=SOFTWARE_LOCAL_BIN_DIR+"hive/"
	
	NFS_SHARE_DIR=(SOFTWARE_SHARE_BIN_DIR,"/home/hadoop/.ssh/","/home/hadoop/tmp",SOFTWARE_TAR_DIR)

