from PySide import QtGui, QtCore
from PySide.QtCore import *
import threading
import time, re
import string
import connection
import re



class commInter(QObject, threading.Thread):
	

	## ## ## SIGNALS ## ## ##
    readyRead = QtCore.Signal(str,str,str)
    

    def __init__(self, connectionType):
        QObject.__init__(self)
        threading.Thread.__init__(self)

        self.devType = None # type de peripehrique traite
        self.devNum = None # numero du peripherique
        self.devStatus = None # etat du peripherique
        self.conn = connection.connection(connectionType)
        self._stopEvent = threading.Event()

		
    
    def readString(self, s):
        s = s.decode('utf-8')
        print(s)
        
        m = re.search(r'\%(?P<type>\w)(?P<id>\d+)=(?P<value>\-?\d+)\%', s)
        # Get values
        if m:
            gd = m.groupdict()
            self.devType = gd['type']
            self.devNum = gd['id']
            self.devStatus = gd['value']
        
        print('>>', self.devType, self.devNum, self.devStatus)
        
	
    def stop(self):
        """ Stop all serial events """
        self._stopEvent.set()		

    def sendMessage(self, dt, dn, ds):
        s = "%"+dt+dn+"="+ds+"%"
        self.conn.sendMessage(s)
  
  
  
    def run(self):
        
        print('Thread start')
    	
        self.conn.createServer()
        while not self._stopEvent.isSet():
            message = self.conn.getMessage()
            self.readString(message)
            self.readyRead.emit(self.devType, self.devNum, self.devStatus)
            print(self.devType, self.devNum, self.devStatus)
            time.sleep(0.1)
            #self._stopevent.wait(0.1)
        print('Thread exit')
              
    		
    
    		