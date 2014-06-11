'''
Created on Apr 9, 2014

@author: root
'''
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import nodeinfo_pb2


class collect:
    def sayHello(self):
        return "hello qsq"
    
    def getNodeInfo(self,ni):
        print(ni)
        nodeinfo = nodeinfo_pb2.NodeInfo()
        nodeinfo.ParseFromString(ni)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("cpu:" + nodeinfo.cpu +"\nmem:" +nodeinfo.mem+"\nos:"+nodeinfo.os+"\ndisk:"+nodeinfo.disk)
        return xmlrpclib.Binary("finish")

obj = collect()
server = SimpleXMLRPCServer(("127.0.0.1", 9999),allow_none=True)
server.register_instance(obj)
print("Listening on port 9999")
server.serve_forever()