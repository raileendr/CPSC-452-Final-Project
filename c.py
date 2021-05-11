import socket
import threading

# The server port and IP
serverIP = "127.0.0.1"
serverPort = 1234

# Create a TCP socket that uses IPv4 address
cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
cliSock.connect((serverIP, serverPort))

###########################################################
# The function to handle the message of the specified format
# @param sock - the socket to receive the message from
# @returns the message without the header
############################################################
def recvMsg(sock):
	
	# The size
	size = sock.recv(3)
	
	# Convert the size to the integer
	intSize = int(size)

	# Receive the data
	data = sock.recv(intSize)

	return data

################################################
# Puts the message into the formatted form
# and sends it over the socket
# @param sock - the socket to send the message
# @param msg - the message
################################################
def sendMsg(sock, msg):

	# Get the message length
	msgLen = str(len(msg))
	
	# Keep prepending 0's until we get a header of 3	
	while len(msgLen) < 3:
		msgLen = "0" + msgLen
	
	# Encode the message into bytes
	msgLen = msgLen.encode()
	
	# Put together a message
	sMsg = msgLen + msg.encode()
	
	# Send the message
	sock.sendall(sMsg)

###################################################
# Handles the user input
# @param mySock - the socket on which to handle the input
###################################################
def inputHandlerThread(mySock, username):
	
	while True:
		msg = input("")
		sendMsg(cliSock, msg)

def auth(cliSock):

	while True:
		username = input("Enter your username: ")
		sendMsg(cliSock, username)
		password = input("Enter your password: ")
		sendMsg(cliSock, password)

		msg=recvMsg(cliSock)
		print(msg.decode())
		if msg.decode() == "Login Successful!":
			inputterThread = threading.Thread(target=inputHandlerThread, args=(cliSock,username,))
			inputterThread.start()
			arrivingMessageListener = threading.Thread(target=handleArrivingMessages, args=(cliSock,))
            # Start the threa
			arrivingMessageListener.start()
			break
	

################################################
# Listens for new messages
#@param mySock - the socket on which to handle the output
################################################
def handleArrivingMessages(mySock):

	while True:
		msg = recvMsg(mySock)
		print(msg.decode())

	
	
		
#added this because they werent being called
auth(cliSock)
#inputHandlerThread(cliSock)
#handleArrivingMessages(cliSock)
	

#	msg = input("Enter a message: ")
	
#	sendMsg(cliSock, msg)
#	msg=recvMsg(cliSock)
#	print(msg.decode())
		
	# Send a message to the server
#	cliSock.sendall(msg.encode())

	# Receive at most 1000 bytes from the server
#	recvData = cliSock.recv(1000)

#	print(recvData)
