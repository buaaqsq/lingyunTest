#!/bin/bash
chkconfig sshd on
service iptables stop
service ip6tables stop
chkconfig iptables off
chkconfig ip6tables off
setenforce 0
sed 's/^SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
sed 's/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
sed 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/ssh_config
sed 's/#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config
service ntpd start
chkconfig ntpd on

echo "系统基础配置已完毕"

yum install -y php php-cli php-devel php-common httpd httpd-devel php-mbstring php-mysql php-pdo php-process mysql mysql-devel mysql-server mysql-libs wget lrzsz dos2unix pexpect libxml2 libxml2-devel MySQL-python curl curl-devel libssh2 libssh2-devel automake autoconf make gcc gcc-c++ libstdc++ libstdc++-devel

yum -y install automake openssl-devel libtool flex bison pkgconfig gcc-c++ boost-devel libevent-devel zlib-devel python-devel ruby-devel
echo '此版本为测试版本，功能还有不足，请多包含'
echo '此版本中安装前提是master中/etc/hosts已配置完毕,所有节点中的jdk已配置完毕'
