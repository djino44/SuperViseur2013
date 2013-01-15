import socket

class connection:
	def __init__(self, connType):
		self.connectionType = connType
		self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def createServer(self):
		if(self.connectionType==1):
			self.createServerSock()

	def sendMessage(self, s):
		if(self.connectionType==1):
			self.sendMessageSock(s)

	def getMessage(self):
		if(self.connectionType==1):
			return self.getMessageSock()


	def createServerSock(self):
		self.serverSock.bind(("", 50007))
		self.serverSock.listen(5)


	def sendMessageSock(self, s):
		self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clientSock.connect(("169.254.141.61", 50007))
		self.clientSock.send(s)
		self.clientSock.close()

	def getMessageSock(self):
		connection, address = self.serverSock.accept()
		return connection.recv(1024)

