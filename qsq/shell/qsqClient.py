# -*- coding: utf-8 -*-
import os
from subprocess import Popen,PIPE

class popenOper: 
    def popenShell(self,command,sin=None):
        p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
        (stdoutdata, stderrdata) = p.communicate(input=sin)
        code = p.wait()
        if len(stderrdata):
            print "error:  %s" % stderrdata 
        if code:
            exit(1)

class linuxUser:
    def createUser(self,username):
        command = "useradd %s -G root" % username
        popenOper().popenShell(command)

class NFSOper:
    INSTALL_COMMAND = "yum install -y nfs-utils rpcbind"
    SHARE_DIR = ["/usr/opt/","/root/.ssh/","/root/tmp/"]
    def nfs_client(self,serverIP):
        t = popenOper()
        t.popenShell(self.INSTALL_COMMAND) 
        t.popenShell("showmount -e %s" %serverIP)         
        for dir in self.SHARE_DIR:
            mkdir = "mkdir -p %s" % dir   
            t.popenShell(mkdir) 
            t.popenShell("mount -t nfs %s:%s %s" %(serverIP,dir,dir)) 

class Install:
    workspace = os.getcwd()
    def step1(self):
        popen = popenOper()
        popen.popenShell("chkconfig sshd on")
        popen.popenShell("service sshd start")
        popen.popenShell("service iptables stop")
        popen.popenShell("service ip6tables stop")
        popen.popenShell("chkconfig iptables off")
        popen.popenShell("chkconfig ip6tables off")
        popen.popenShell("setenforce 0")
        popen.popenShell("sed 's/^SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config")
        popen.popenShell("sed 's/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config")
        popen.popenShell("sed 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/ssh_config")
        popen.popenShell("sed 's/#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config")
        popen.popenShell("service ntpd start")
        popen.popenShell("chkconfig ntpd on")
        
        print ("系统基础配置已完毕\n开始配置NFS\n")
        NFSOper().nfs_client("192.168.2.31")                                                                                                                                                                                                                                                                
                        
        popen.popenShell("yum -y install automake openssl-devel libtool flex bison pkgconfig gcc-c++ boost-devel libevent-devel zlib-devel python-devel ruby-devel")
        os.chdir("/root/tmp/softeware")
        popen.popenShell("tar zxvf thrift-0.9.1.tar.gz")
        os.chdir("/root/tmp/thrift-0.9.1")
        popen.popenShell("./configure && make && make install")
        os.chdir("/root/tmp/thrift-0.9.1/lib/py")
        popen.popenShell("python setup.py install")                      
        
if __name__ == "__main__":
    Install().step1()