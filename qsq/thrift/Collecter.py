'''
Created on May 8, 2014

@author: root
'''
from collections import OrderedDict
import platform
import os, socket, struct, fcntl

class Collecter:
    
    def __init__(self):
        self.hostname = platform.node()
        self.machine = platform.machine()
        self.ostype = platform.dist()
        self.pversion = platform.python_version()
        self.architecture = platform.architecture()
    
    def CPUinfo(self):
        CPUinfo = OrderedDict()
        procinfo = OrderedDict()
    
        nprocs = 0
        with open('/proc/cpuinfo') as f:
            for line in f:
                if not line.strip():
                    CPUinfo['proc%s' % nprocs] = procinfo
                    nprocs = nprocs + 1
                    procinfo = OrderedDict()
                else:
                    if len(line.split(':')) == 2:
                        procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                    else:
                        procinfo[line.split(':')[0]] = ''
        return CPUinfo
    
    def load_stat(self):
        loadavg = {}
        f = open('/proc/loadavg')
        con = f.read().split()
        f.close()
        loadavg['lavg_1'] = con[0]
        loadavg['lavg_5'] = con[1]
        loadavg['lavg_15'] = con[2]
        loadavg['nr'] = con[3]
        loadavg['last_pid'] = con[4]
        return loadavg
    
    def meminfo(self):
        meminfo = OrderedDict()
    
        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
        return meminfo
    
    def disk_stat(self,path="/"):
        hd = {}
        disk = os.statvfs(path)
        hd['available'] = disk.f_bsize * disk.f_bavail /1024.0/1024.0/1024.0
        hd['capacity'] = disk.f_bsize * disk.f_blocks /1024.0/1024.0/1024.0
        hd['used'] = disk.f_bsize * disk.f_bfree /1024.0/1024.0/1024.0
        return hd
    
    def get_ip(self):
        try:
            ip=self.get_local_ip('eth1')
        except Exception , e:
            try:
                ip=self.get_local_ip('eth0')
            except Exception , e:
                print e
            else:
                return ip           
        else:
            return ip
        
        
    
    def get_local_ip(self,ifname='eth0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        inet = fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))
        ret = socket.inet_ntoa(inet[20:24])
        return ret

if __name__ == '__main__':
    #print Collecter().CPUinfo()['proc0']['model name']  
    #print'{0:.2f}'.format(float(Collecter().meminfo()['MemTotal'].split(' ')[0])/1024/1024) + 'GB'
    #print '{0:.2f}'.format(Collecter().disk_stat()['capacity'])
    #print Collecter().load_stat()['lavg_1']
    print Collecter().get_ip()
    
