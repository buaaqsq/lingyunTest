'''
Created on Apr 25, 2014

@author: qsq
'''
from qsq import models
import os

class SSH():
    
    def scpAFile(self,file,hosts):
        if os.path.isfile(file):
            command = "scp "+file
            for h in hosts:
                print(command + " "+h+":"+os.path.dirname(file) + "/")
                #os.system(command + " "+h+":"+path)
        else:
            print "error"
        
        
    def scpDir(self,p,hosts):
        if os.path.isdir(p):
            command = "scp -r "+p
            for h in hosts:
                print(command + " "+h+":"+os.path.split(p)[0] + "/")
                #os.system(command + " "+h+":"+path)
        else:
            print "error"   


if __name__ == '__main__':
    ssh = SSH()
    ssh.scpDir("/usr/bin", ["slave1","slave2"])