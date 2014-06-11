'''
Created on Apr 9, 2014

@author: root
'''
import xmlrpclib
import nodeinfo_pb2
import cPickle as pickle

nodeinfo = nodeinfo_pb2.NodeInfo()
nodeinfo.cpu="i5"
nodeinfo.mem="4G"
nodeinfo.disk="1T"
nodeinfo.os="centos"
nodeinfo.load="0"
nodeinfo_str=nodeinfo.SerializePartialToString()
print nodeinfo_str

c = pickle.dumps(nodeinfo_str, protocol=1)
b = xmlrpclib.Binary(c)
server = xmlrpclib.ServerProxy("http://127.0.0.1:9999",allow_none=True)
work=server.getNodeInfo(b)
#work=server.sayHello()
print work