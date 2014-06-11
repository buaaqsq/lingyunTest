'''
Created on Apr 24, 2014

@author: qsq
'''
from qsq import models
import os
from qsq.transfer import gl
from qsq.tools.popenOper import popenOper

class wgetTool():
    
    def getSoftware(self,path,software):
        str = "tar -zxvf " + path + "/" + software + ".tar.gz"
        os.system(str)
        return os.getcwd()+"/" + software
        
        

class installTool():
    
    def makeConfFile(self,dic,filename):
        
        if os.path.exists(filename):
            os.remove(filename)
        
        f = open(filename,'w')
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n")
        f.write("<configuration>\n")
        for k in dic.keys():
            s = "<property>\n<name>"+ k +"</name>\n<value>" + dic[k] + "</value>\n</property>\n"
            f.write(s)
        f.write("<configuration>\n")
        f.flush()
        f.close()
    
    def makeShFile(self,dic,filename):
        if os.path.exists(filename):
            os.remove(filename)
        f = open(filename,'w')
        for k in dic.keys():
            f.write("export " + k + "=" + dic[k] + "\n")
            
        f.write()
        f.flush()
        f.close()
        
    #installTool().getSlaveFile("worker","slaves")
    def getSlaveFile(self,rolename,file):
        if os.path.isfile(file):
            os.remove(file)
        f = open(file,"w")
        srp = models.serviceRole.objects.get(name=rolename)
        hsp = models.hostRole.objects.filter(servicerole=srp)
        for p in hsp:
            f.write(p.hostid.hostname+"\n")
        f.flush()
        f.close()
        return os.getcwd()+"/"+file
   
    def getConf(self,n,c,f):       
        clusterp = models.Cluster.objects.get(name=n)
        componp=models.Component.objects.get(cluster=clusterp,name=c)
        cfg = models.Configuration.objects.filter(component=componp,file=f)
        dic ={}
        for a in cfg:
            dic[a.name] = a.value
        return dic
    
    def getConfFile(self,n,c,f):
        self.makeConfFile(self.getConf(n,c,f),os.getcwd()+"/"+f)
        return os.getcwd()+"/"+f
    
    def getShFile(self,n,c,f):
        self.makeShFile(self.getConf(n,c,f),os.getcwd()+"/"+f)
        return os.getcwd()+"/"+f
        
    def setEnv(self,old,new,file):
        str = 'sed -i "s/^'+old+'/'+new+'/"'+' '+file
        os.system(str)     
        
class ServiceInstall():      
    def hadoopInstaller(self,clusterName):
        hadoophome = wgetTool().getSoftware("/tmp/software", "hadoop-2.2.0")
        coresiteF = installTool().getConfFile(clusterName, "Hadoop", "core-site.xml")
        hdfssiteF = installTool().getConfFile(clusterName, "Hadoop", "hdfs-site.xml")
        yarnsiteF = installTool().getConfFile(clusterName, "Hadoop", "yarn-site.xml")
        mapredsiteF = installTool().getConfFile(clusterName, "Hadoop", "mapred-site.xml")
        slaveFile=installTool().getSlaveFile("datanode","slaves")
        hadoopEnvSh=installTool().getShFile(clusterName,"Hadoop","hadoop-env.sh")
        f = open(hadoopEnvSh,"w")
        f.write('for f in $HADOOP_HOME/contrib/capacity-scheduler/*.jar; do \n\
  if [ "$HADOOP_CLASSPATH" ]; then \n\
    export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$f \n\
  else \n\
    export HADOOP_CLASSPATH=$f \n\
  fi \n\
done ')
        f.flush()
        f.close()
        popenOper().popenShell("mv %s %s/etc/hadoop/" %(coresiteF,hadoophome))
        popenOper().popenShell("mv %s %s/etc/hadoop/" %(hdfssiteF,hadoophome))
        popenOper().popenShell("mv %s %s/etc/hadoop/" %(yarnsiteF,hadoophome))
        popenOper().popenShell("mv %s %s/etc/hadoop/" %(mapredsiteF,hadoophome))
        popenOper().popenShell("mv %s %s/etc/hadoop/" %(slaveFile,hadoophome))
        popenOper().popenShell("mv %s %s/etc/hadoop/" %(hadoopEnvSh,hadoophome))
        popenOper().popenShell("mv %s /usr/opt/" %hadoophome)
        return 0
    
    def hbaseInstaller(self):
        hbasehome = wgetTool().getSoftware("/tmp/software", "hbase")
        hbasesiteF = installTool().getConfFile(gl.CLUSTER, "hbase", "hbase-site.xml")
        
    def gangliaInstaller(self):
        hbasehome = wgetTool().getSoftware("/tmp/software", "hbase")
        hbasesiteF = installTool().getConfFile(gl.CLUSTER, "hbase", "hbase-site.xml")

        
        

if __name__ == '__main__':
    it=ServiceInstall().hadoopInstaller("demo")
    print it
    
