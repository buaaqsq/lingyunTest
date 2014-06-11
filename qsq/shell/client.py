#!/usr/bin/python
# -*- coding: utf8 -*-
import psutil
import platform

class Node(object):

    def dist(self, token):
        dist_json = ''
        sysinstaller = ''
        installer = ''
        ostype = platform.dist()
        if(ostype[0] in ['Ubuntu','debian','ubuntu','Debian']):
            sysinstaller = 'apt-get'
            installer = 'dpkg'
        elif(ostype[0] in ['SuSE', 'suse']):
            sysinstaller = 'zypper'
            installer = 'rpm'
        elif(ostype[0] in ['CentOS', 'centos', 'redhat','RedHat']):
            sysinstaller = 'yum'
            installer = 'rpm'

        machine = platform.machine()
        hostname = platform.node()
            
        dist_json = {'os.system':ostype[0], 'os.version':ostype[1], 'os.release':ostype[2], 'os.sysinstall':sysinstaller, 'os.installer':installer, 'os.arch':machine, 'os.hostname':hostname}


    def GetCpuInfo(self, token):
            cpu = []
            cpuinfo = {}
            f = open("/proc/cpuinfo")
            lines = f.readlines()
            f.close()
            for line in lines:
                if line == 'n':
                    cpu.append(cpuinfo)
                    cpuinfo = {}
                if len(line) < 2: continue
                name = line.split(':')[0].strip().replace(' ','_')
                var = line.split(':')[1].strip()
                cpuinfo[name] = var
            return json.dumps(cpuinfo, sort_keys=False, indent=4, separators=(',', ': '))

    def GetMemInfo(self, token):
            mem = {}
            f = open("/proc/meminfo")
            lines = f.readlines()
            f.close()
            for line in lines:
                if len(line) < 2:
                       continue
                name = line.split(':')[0]
                var = line.split(':')[1].split()[0]
                mem[name] = long(var) * 1024.0
            mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
            return json.dumps(mem, sort_keys=False, indent=4, separators=(',', ': '))
    '''
    url /node/GetLoadAvg/token
    '''
    def GetLoadAvg(self, token):
            loadavg = {} 
            f = open("/proc/loadavg") 
            con = f.read().split() 
            f.close() 
            loadavg['lavg_1']=con[0] 
            loadavg['lavg_5']=con[1] 
            loadavg['lavg_15']=con[2] 
            loadavg['nr']=con[3] 
            loadavg['last_pid']=con[4] 

    def GetNetTraffic(self, token):
            net_before = psutil.net_io_counters()
            time.sleep(0.1)
            net_after = psutil.net_io_counters()
            #print net_before
            #print net_after
            net = {}
            net['bytes_sent'] = (net_after.bytes_sent - net_before.bytes_sent)*10
            net['bytes_recv'] = (net_after.bytes_recv - net_before.bytes_recv)*10
            net['packets_sent'] = (net_after.packets_sent - net_before.packets_sent)*10
            net['packets_recv'] = (net_after.packets_recv - net_before.packets_recv) * 10

    def GetHddInfo(self, token):
            hdds = []
            mount = {}
            file_system = []
            type = []
            size = []
            used = []
            avail = []
            used_percent = []
            mounted_on = []
            opts = []
            hdds = psutil.disk_partitions()
            for line in hdds:
                file_system.append(line[0].replace('\\n',''))
                type.append(line[2].replace('\\n',''))
                mounted_on.append(line[1].replace('\\n',''))
                opts.append(line[3].replace('\\n',''))
                
                size.append(psutil.disk_usage(line[1]).total)
                used.append(psutil.disk_usage(line[1]).used)
                avail.append(psutil.disk_usage(line[1]).free)
                used_percent.append(psutil.disk_usage(line[1]).percent)
                
            mount['file_system'] = file_system
            mount['type'] = type
            mount['size'] = size
            mount['used'] = used
            mount['avail'] = avail
            mount['used_percent'] = used_percent
            mount['mounted_on'] = mounted_on
            mount['opts'] = opts
            dist_json = json.dumps(mount)

    def GetCpuDetail(self, token):
            cpu = {}
            user = psutil.cpu_times_percent().user
            system = psutil.cpu_times_percent().system
            iowait = psutil.cpu_times_percent().iowait
            idle = 100 - user - system - iowait

            cpu['user'] = user
            cpu['system'] = system
            cpu['iowait'] = iowait
            cpu['idle'] = idle
            cpu = json.dumps(cpu)