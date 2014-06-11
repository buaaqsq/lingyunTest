'''
Created on May 8, 2014

@author: root
'''

import os
os.system("yum -y install automake openssl-devel libtool flex bison pkgconfig gcc-c++ boost-devel libevent-devel zlib-devel python-devel ruby-devel")
os.chdir("/root/")
os.system("tar zxvf thrift-0.9.1.tar.gz")
os.chdir("/root/thrift-0.9.1")
os.system("./configure && make && make install")
os.chdir("/root/thrift-0.9.1/lib/py")
os.system("python setup.py install")