import sys
from PySide.QtCore import Qt, QSize,QObject
from PySide import QtCore, QtGui
from Thread_re import commInter


import time
import random



def updateD(devType,devNum,devStatus):
    
    print(devType+devNum+devStatus)
        

i=0
com = commInter(1)
com.readyRead.connect(updateD)
com.start()
random.seed()


        

#while 1:
#    com.sendMessage("T", '0' +str(int(random.random()*5+1)), "1")
#    time.sleep(0.1)
#    com.sendMessage("T", '0' +str(int(random.random()*5+1)), "0")
#    time.sleep(0.1)
#    com.sendMessage("A", '01', str(random.uniform(1, 5)))
#    time.sleep(0.1)
    