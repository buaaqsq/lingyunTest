# -*- coding: utf-8 -*-
from subprocess import Popen,PIPE
import os

from qsq.models import *
from qsq.tools.DataOper import *
import os, pexpect
from install import ServiceInstall
from qsq.shell.qsqService import Install

import logging
import logging.config
logging.config.fileConfig("/root/.qsq/logging.conf")
#create logger
logger = logging.getLogger("qsq")

class linuxUser:
    def createUser(self,username):
        command = "useradd %s -G root" % username
        p = Popen(command,shell=True,stdout=PIPE,stderr=PIPE)
        (stdoutdata, stderrdata) = p.communicate()
        return stdoutdata
    
class MylogOper:    
    def popenLogger(self,command,stdoutdata,stderrdata):
        logger.info("%s",command)
        if len(stderrdata):
            logger.error("%s",stderrdata)
            
class Tool:
    def popenShell(self,command,sin=None):
        p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
        (stdoutdata, stderrdata) = p.communicate(input=sin)
        code = p.wait()
        MylogOper().popenLogger(command, stdoutdata, stderrdata)
        return code
        
# NFS 安装测试
class NFSOper:
    INSTALL_COMMAND = "yum install -y nfs-utils rpcbind"
    SHARE_DIR = ["/usr/opt/"]
    def nfs_server(self):
        t = Tool()
        t.popenShell(self.INSTALL_COMMAND)                
        for dir in self.SHARE_DIR:
            mkdir = "mkdir -p %s" % dir
            t.popenShell(mkdir)
            echocommand="echo '%s *(rw,no_root_squash,sync)' >> /etc/exports" % dir
            t.popenShell(echocommand)        
        t.popenShell("service rpcbind start")
        t.popenShell("service nfs start")
        t.popenShell("chkconfig --level 2345 rpcbind on")
        t.popenShell("chkconfig --level 2345 nfs on")       
    
    def nfs_client(self,serverIP):
        t = Tool()
        t.popenShell(self.INSTALL_COMMAND) 
        t.popenShell("showmount -e %s" %serverIP)         
        for dir in self.SHARE_DIR:
            mkdir = "mkdir -p %s" % dir   
            t.popenShell(mkdir) 
            t.popenShell("mount -t nfs %s:%s %s" %(serverIP,dir,dir)) 

if __name__ == "__main__":
    if ServiceInstall().hadoopInstaller("test3"):
        print ("there are some error")
    Install().step1()
    p = Cluster.objects.get(name="test3")
    hp = host.objects.filter(clusterid=p)
    if len(hp) == 0:
        print("不能获取主机名和密码，请安装第一步")
    for h in hp:
        print h.hostname
        foo = pexpect.spawn("ssh %s 'python /root/qsqClient.py'" % h.hostname)
        foo.expect(['password: '])  
        foo.sendline(h.password)
        foo.expect(pexpect.EOF)
           

        