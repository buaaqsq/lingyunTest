'''
Created on Apr 10, 2014

@author: root
'''
from nodeinfo import collect
from nodeinfo.ttypes import *
from Collecter import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)   
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)   
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)   
    # Create a client to use the protocol encoder
    client = collect.Client(protocol)    
    # Connect!
    transport.open()
    
    client.ping()
    print 'ping()'
    
    sum = client.seyHello("hello,I am jiangxiao")
    print 'seyHello'
    
    ni = NodeInfo()
    
    clt = Collecter()
    ni.cpu = clt.CPUinfo()['proc0']['model name']
    ni.mem = '{0:.2f}'.format(float(clt.meminfo()['MemTotal'].split(' ')[0]) / 1024 / 1024) + 'GB'
    ni.disk = '{0:.2f}'.format(clt.disk_stat()['capacity'])
    ni.os = clt.ostype[0] + " " + clt.ostype[1]
    ni.load = clt.load_stat()['lavg_1']
    ni.ip = clt.get_ip()
    
    message = client.getNodeInfo(ni)
    print message

    # Close!
    transport.close()

except Thrift.TException, tx:
  print '%s' % (tx.message)
