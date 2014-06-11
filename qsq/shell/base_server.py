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
    SHARE_DIR = ["/usr/opt/","/root/.ssh/","/root/tmp/"]
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
        
        logger.info("系统基础配置已完毕\n开始配置NFS\n")
        NFSOper.nfs_server()
        
        logger.info("NFS配置已完毕\n开始配置ssh\n")
        os.chdir(self.workspace + "/lingyun/qsq/shell/")
        popen.popenShell("rm -rf /root/.ssh/*")
        popen.popenShell("./get_ssh_keygen.exp")
        os.chmod("/root/.ssh", 700)
        popen.popenShell("cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys")
        os.chmod("/root/.ssh/authorized_keys", 644)
        popen.popenShell("ssh-add /root/.ssh/id_rsa")
        
#         p = Cluster.objects.get(name=gl.CLUSTER)
#         hp = host.objects.filter(clusterid=p)
#         if len(hp) == 0:
#             print "不能获取主机名和密码，请安装第一步"
#             return 0
#         if os.path.exists("scpAFile.sh"):
#             os.remove("scpAFile.sh")
#         if os.path.exists("scp2slaves.sh"):
#             os.remove("scp2slaves.sh")
#         scpAfile = open("scpAFile.sh", 'w')
#         scp2slaves = open("scp2slaves.sh", 'w')
#         for h in hp:
#             scpAfile.write("scp $1 " + h.hostname + ":$2\n")
#             scp2slaves.write("scp -r $1 " + h.hostname + ":$2\n")
#             print("./scpWithPswd.exp " + h.hostname + " " + h.password)
#             foo = pexpect.spawn('scp /root/.ssh/authorized_keys %s:/root/.ssh/' % h.hostname)
#             foo.expect(['password: '])  
#             foo.sendline(h.password)
#             foo.expect(pexpect.EOF)
#         
#         hp.close()
#         p.close()
#         scpAfile.close()
#         scp2slaves.close()  
        
#         if(os.path.exists(slavehosts)):
#             fp = open(slavehosts,'r')
#             line = fp.readline()
#             if os.path.exists("scpAFile.sh"):
#                 os.remove("scpAFile.sh")
#             if os.path.exists("scp2slaves.sh"):
#                 os.remove("scp2slaves.sh")
#             scpAfile = open("scpAFile.sh",'w')
#             scp2slaves = open("scp2slaves.sh",'w')
#             while(line != ''):
#                 hostname = line.split(",")[0]
#                 password = line.split(",")[1]
#                 scpAfile.write("scp $1 "+hostname + ":$2\n")
#                 scp2slaves.write("scp -r $1 "+hostname + ":$2\n")
#                 print("./scpWithPswd.exp " + hostname + " "+ password)
#                 foo = pexpect.spawn('scp /root/.ssh/authorized_keys %s:/root/.ssh/' % hostname)
#                 foo.expect(['password: '])  
#                 foo.sendline(password)
#                 foo.expect(pexpect.EOF)  
#                 line=fp.readline()                   
#             fp.close()
#             scpAfile.close()
#             scp2slaves.close()    
#         else:
#             print("不能获取主机名和密码，请安装第一步")
#             return HttpResponseRedirect('step1')
        
        popen.popenShell("yum install -y php php-cli php-devel php-common httpd httpd-devel php-mbstring php-mysql php-pdo php-process mysql mysql-devel mysql-server mysql-libs wget lrzsz dos2unix pexpect libxml2 libxml2-devel MySQL-python curl curl-devel libssh2 libssh2-devel automake autoconf make gcc gcc-c++ libstdc++ libstdc++-devel")
        
    def step2(self):
        return 


        
if "__main__" == __name__:
    pass       
