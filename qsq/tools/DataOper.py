import os
from qsq.models import *
from qsq.transfer import gl

class Node:
    slave_hosts = '/root/workspace/lingyun/qsq/shell/slave_hosts'
    def saveNodes(self,nodeslist):
        if(os.path.exists(self.slave_hosts)):
                os.remove(self.slave_hosts)
        fp = open(self.slave_hosts,'w')
        for node in nodeslist.split('\n'):
#                 print("%s" % node)
            if(node[0] != "\n"):
                hosts = node.split(',')
                fp.write(hosts[0]+','+hosts[1]+"\n")
                        
        fp.flush()
        fp.close()
        
    def getNodesfromFile(self):
        nodes = []
        if os.path.exists(self.slave_hosts):
            fp = open(self.slave_hosts,'r')
            line = fp.readline()
            while(line != ''):
                hostname = line.split(",")[0]
                nodes.append(hostname) 
                line=fp.readline()                   
            fp.close()
        return nodes
    
    def getNodes(self):
        p=Cluster.objects.get(name=gl.CLUSTER)
        #p=Cluster.objects.get(name="bhwzyjy")
        nodelist = host.objects.filter(clusterid=p)
        node = []
        for n in nodelist:
            node.append(n.hostname)
        return node
    
    def getNodesTuple(self):
        nodes = self.getNodes()
        nl = []
        for node in nodes:
            s = (node,node)
            nl.append(s)
        nt = tuple(nl)
        return nt
        
    def test(self):
        d=u"slave5"
        hp = host.objects.get(hostname=d)
        return hp.hostname
    
    def getIPfromHosts(self):
        etc_hosts="/etc/hosts"
        nodes = {}
        if(os.path.exists(etc_hosts)):
            fp = open(etc_hosts,'r')
            
            for line in fp.readlines():  
 #               print len(line)                                                        
                if len(line) == 1:   
                    continue
                IP = line.split()[0]
                hostname = line.split()[1]                                 
                nodes[hostname]=IP            
 
            fp.close()
        return nodes
    
    def getServiceList(self):
        p=Cluster.objects.get(name=gl.CLUSTER) 
        #p=Cluster.objects.get(name="bhwzyjy") 
        serviceList=[]
        for k in p.component.split(","):
            if gl.componentKMV.has_key(k):
                serviceList.append(gl.componentKMV.get(k))
            
        print p.component
        return serviceList
       
class ConfigurationData:
    
    def getInitConf(self,com,l,filename):
        dsp = DefaultSetting.objects.filter(component=com,level=l,file=filename)
        return dsp
    
    def getComConf(self,com,l):
        dsp = DefaultSetting.objects.filter(component=com,level=l).order_by('file')
        return dsp

       

if "__main__" == __name__:
    hdfssite=ConfigurationData().getInitConf("hadoop2.2.0", "0", "hdfs-site.xml")
    print hdfssite
    
    
