# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
import os, pexpect
from qsq.models import host, Cluster
from qsq.transfer import gl
from qsq.tools.popenOper import popenOper
from qsq.tools.Log import Loger

class linuxUser:
    def createUser(self,username):
        command = "useradd %s -G root" % username
        popenOper().popenShell(command)

class NFSOper:
    INSTALL_COMMAND = "yum install -y nfs-utils rpcbind"
    SHARE_DIR = ["/usr/opt/","/root/tmp/"]
    def nfs_server(self):
        t = popenOper()
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

class Install:
    workspace = os.getcwd()
    def step1(self):
        popen = popenOper()
        logger=Loger().getLogger()
        print ("系统基础配置已完毕\n开始配置NFS\n")
        logger.info("系统基础配置已完毕\n开始配置NFS\n")
        NFSOper().nfs_server()
        
        logger.info("NFS配置已完毕\n开始配置ssh\n")
        os.chdir("/root/workspace/lingyun/qsq/shell/")
        popen.popenShell("rm -rf /root/.ssh/*")
        popen.popenShell("./get_ssh_keygen.exp")
        os.chmod("/root/.ssh", 700)
        popen.popenShell("cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys")
        os.chmod("/root/.ssh/authorized_keys", 644)
        popen.popenShell("ssh-add /root/.ssh/id_rsa")
        
        

