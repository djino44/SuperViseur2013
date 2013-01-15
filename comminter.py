# 
# @file comminter.py
# @brief Classe servant d'interface de communication
# 
import string
import connection

class commInter:
	def __init__(self,connectionType):
		self.devType = None # type de peripehrique traite
		self.devNum = None # numero du peripherique
		self.devStatus = None # etat du peripherique
		self.conn = connection.connection(connectionType)
    
	def readString(self, s):
		s = string.strip(s,"%")
		self.devType=s[0]
		self.devNum=s[1]+s[2]
		self.devStatus=s[4:len(s)]
        
	def serveForever(self):
		self.conn.createServer()
		while 1:
			message = self.conn.getMessage()
			self.readString(message)
			print self.devType, self.devNum, self.devStatus

	def sendMessage(self, dt, dn, ds):
		s = "%"+dt+dn+"="+ds+"%"
		self.conn.sendMessage(s)

