'''
Created on Apr 9, 2014

@author: root
'''
import sys
import nodeinfo_pb2

nodeinfo = nodeinfo_pb2.NodeInfo()
nodeinfo.cpu="i5"
nodeinfo.mem="4G"
nodeinfo.disk="1T"
nodeinfo.os="centos"
nodeinfo.load="0"
nodeinfo_str=nodeinfo.SerializePartialToString()
print nodeinfo_str