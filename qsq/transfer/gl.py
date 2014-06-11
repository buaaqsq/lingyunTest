USERNAME=''
CLUSTER =''
PCLUSTER = ''
STEP=0

ha = "0"
clustername = ""
username=""
pcluster=1
serverlist = ["namenode","resourmanager","hbasemaster","sparkmaster","gmated","hive","pig","Phoniex","zookeeper1","zookeeper2","zookeeper3"]
componentKV ={"1":"Hadoop", "2":"Hbase","3":"Hive","4":"Pig", "5":"Sqoop", "6":"Ganglia", "7":"Nagios", "8":"Spark","9":"Phoniex"}
componentKMV = {"2":"hbasemaster","3":"hive","4":"pig", "5":"sqoop", "6":"gmated", "7":"nagios", "8":"sparkmaster","9":"phoniex"}
componentKSV = {"1":["datanode","nodemanager"], "2":"regionserver","8":"worker"}