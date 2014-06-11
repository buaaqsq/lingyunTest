'''
Created on May 22, 2014

@author: root
'''
# -*- coding: utf-8 -*-
import logging
import logging.config
logging.config.fileConfig("/root/.qsq/logging.conf")
#create logger
logger = logging.getLogger("qsq")

class Loger:
    
    def __init__(self):
        logging.config.fileConfig("/root/.qsq/logging.conf")
    
    def getLogger(self,name="qsq"):
        logger = logging.getLogger(name)
        return logger
    
    def popenLogger(self,command,stdoutdata,stderrdata):
        logger = self.getLogger()
        logger.info("%s",command)
        if len(stderrdata):
            logger.error("%s",stderrdata)


if __name__ == '__main__':
    pass