'''
Created on May 22, 2014

@author: root
'''
# -*- coding: utf-8 -*-
from subprocess import Popen,PIPE
from Log import Loger

class popenOper:
    
    def popenShell(self,command,sin=None):
        p = Popen(command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
        (stdoutdata, stderrdata) = p.communicate(input=sin)
        code = p.wait()
        Loger().popenLogger(command, stdoutdata, stderrdata)
        if code:
            exit(1)


if __name__ == '__main__':
    pass