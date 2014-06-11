#!/usr/bin/python
import os
from xml.sax.handler import ContentHandler  
from xml.sax import parse  
from qsq.models import *

from  xml.dom import  minidom

class DOMXml():
    def get_attrvalue(self,node, attrname):
        return node.getAttribute(attrname) if node else ''
    
    def get_nodevalue(self,node, index = 0):
        return node.childNodes[index].nodeValue if node else ''
    
    def get_xmlnode(self,node,name):
        return node.getElementsByTagName(name) if node else []
    
    def xml_to_string(self,filename='user.xml'):
        doc = minidom.parse(filename)
        return doc.toxml('UTF-8')
    
    def get_xml_data(self,filename='user.xml'):
        doc = minidom.parse(filename) 
        root = doc.documentElement
    
        user_nodes = self.get_xmlnode(root,'user')
        user_list=[]
        for node in user_nodes: 
            user_id = self.get_attrvalue(node,'id') 
            node_name = self.get_xmlnode(node,'username')
            node_email = self.get_xmlnode(node,'email')
            node_age = self.get_xmlnode(node,'age')
            node_sex = self.get_xmlnode(node,'sex')
    
            user_name =self.get_nodevalue(node_name[0]).encode('utf-8','ignore')
            user_email = self.get_nodevalue(node_email[0]).encode('utf-8','ignore') 
            user_age = int(self.get_nodevalue(node_age[0]))
            user_sex = self.get_nodevalue(node_sex[0]).encode('utf-8','ignore') 
            user = {}
            user['id'] , user['username'] , user['email'] , user['age'] , user['sex'] = (
                int(user_id), user_name , user_email , user_age , user_sex
            )
            user_list.append(user)
        return user_list 
    def sendDataToDB(self,file,dbfilename,com):
        doc = minidom.parse(file) 
        root = doc.documentElement
        conf_nodes = self.get_xmlnode(root,'property')
        for node in conf_nodes:
            node_name = self.get_xmlnode(node,'name')
            node_value = self.get_xmlnode(node,'value')
            node_description = self.get_xmlnode(node,'description')
            namev = node_name[0].firstChild.data
            if len(node_value):
                valuev = node_value[0].firstChild.data
            else:
                valuev=""
            if len(node_description):
                descriptionv = node_description[0].firstChild.data
            else:
                descriptionv=""
            
            p=DefaultSetting(name=namev,value=valuev,description=descriptionv,file=dbfilename,component=com,level="1")
            p.save() 
        print "finished"
        
    def test(self,file,dbfilename,com):
        doc = minidom.parse(file) 
        root = doc.documentElement
        conf_nodes = self.get_xmlnode(root,'property')
        for node in conf_nodes:
            node_name = self.get_xmlnode(node,'name')
            node_value = self.get_xmlnode(node,'value')
            node_description = self.get_xmlnode(node,'description')
            print "name:" + node_name[0].firstChild.data
            if len(node_value):
                print "value:" + node_value[0].firstChild.data
            if len(node_description):
                print "description:" + node_description[0].firstChild.data
                 
        print "finished"
    def SQlToDB(self,file,com):
        f = open(file)
        for line in f.readlines():
            s = line[1:len(line)-3]
            val = s.split(",")
            namev = val[1]
            valuev=val[2]
            descriptionv=val[3]
            p=DefaultSetting(name=val[1][2:len(val[1])-1],value=val[2][2:len(val[2])-1],description=val[3][2:len(val[3])-1],file=val[4][2:len(val[4])-1],component=com,level=val[5][2:len(val[5])-1])
            p.save() 

    def testSQl(self,file,com):
        f = open(file)
        for line in f.readlines():
            s = line[1:len(line)-3]
            val = s.split(",")
            print val[1][2:len(val[1])-1]+":"+val[1]+":"+val[2]+":"+val[3]
#         doc = minidom.parse(file) 
#         root = doc.documentElement
#         conf_nodes = self.get_xmlnode(root,'property')
#         for node in conf_nodes:
#             node_name = self.get_xmlnode(node,'name')
#             node_value = self.get_xmlnode(node,'value')
#             node_description = self.get_xmlnode(node,'description')
#             print "name:" + node_name[0].firstChild.data
#             if len(node_value):
#                 print "value:" + node_value[0].firstChild.data
#             if len(node_description):
#                 print "description:" + node_description[0].firstChild.data
                 
        print "finished"


class configuration:
    
    def setConf(self,dic,filename):
        
        if os.path.exists(filename):
            os.remove(filename)
        
        f = open(filename,'w')
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n")
        f.write("<configuration>\n")
        for k in dic.keys():
            s = "<property>\n<name>"+ k +"</name>\n<value>" + dic[k] + "</value>\n</property>\n"
            f.write(s)
        f.write("<configuration>\n")
    
    def setEnv(self,old,new,file):
        str = 'sed -i "s/^'+old+'/'+new+'/"'+' '+file
        os.system(str)
    
    def sendShToDB(self,file,dbfilename,com):
        if not os.path.isfile(file):
            print "ERROR:" + file + " not exit!"
            exit(0)
        
        f = open(file,"r")
        for line in f.readlines():
            if line.startswith("export") or line.startswith("#export"):
                (head,sep,tail)=line.partition(" ")
                (n,equ,v)=tail.partition("=")
                print "name:" + n + "------" + "value:" + v
                p=DefaultSetting(name=n,value=v,description="",file=dbfilename,component=com,level="1")
                p.save()
        
        f.close()
        print "finished!"
        
        
        
        
if __name__ == "__main__":
    DOMXml().sendDataToDB("/root/mapred-default.xml","mapred-site.xml","hadoop2.2.0")
