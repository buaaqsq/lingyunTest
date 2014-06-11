'''
Created on Apr 10, 2014

@author: root
'''
# import sys, glob
# sys.path.append('gen-py')
# sys.path.insert(0, glob.glob('../../lib/py/build/lib.*')[0])

from nodeinfo import *
from nodeinfo.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class CollectHandler:
    def __init__(self):
        self.log = {}
        
    def ping(self):
        print 'ping()'
        
    def seyHello(self,word):
        print "hello,boy!" + word + "\n"
        return "hello"
        
    def getNodeInfo(self,ni):
        print ni.cpu + "    " + ni.mem  + "    " + ni.disk  + "    " + ni.os + "  " + ni.load + "  " + ni.ip 
        return "haha shoudao"
    
    def getHostInformation(self,hi):
        print hi.cpu_num
        return "getit"
    
    def getHostMoniter(self,hm):
        print hm.proc_run
        return "getit"

class InstallHandler:
    def __init__(self):
        self.log = {}


    
handler = CollectHandler()
processor = collect.Processor(handler)
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

#server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
#You could do one of these for a multithreaded server
server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'