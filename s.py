import socket
import threading
import select

listenPort = 1234

# The socket the server uses for listening
listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associate the listening socket with
# port 1234
listenSock.bind(('', 1234))

# Start listening with a connection backlog queue
# of 100
listenSock.listen(100)

# The user name to socket dictionary
userNameToSockDic = {}

# A map of group names to group member sockets
groupToSockDic = {}

# Map from user names to group names that the user is a member of
userNameToGroupMembershipsDic = {}

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

usernamePassword = {"a" : "a", "b" : "b", "c" : "c"}
	
def auth(clienComSock):
	flag=False;
	while not flag:
		
		# Get the user name
		userName = recvMsg(clienComSock)
		# Get the password	
		password = recvMsg(clienComSock)
		# change from bytes to string
		userName=userName.decode()
		password=password.decode()
		
		if not userName in usernamePassword:
			sendMsg(clienComSock, "Wrong credentials!")
			print("Wrong credentials")
		elif usernamePassword[userName] == password:
			print("Got user name", userName)
			sendMsg(clienComSock, ("Login Successful!"))
			flag = True
			break
	return userName
	
def serviceGroup(sock_group, cliSock):
	
	while True:
		read_sockets, _, exception_sockets = select.select(sock_group, [], sock_group)
		for notified_socket in read_sockets:
			msg = recvMsg(notified_socket)
			msg=msg.decode()

			for sock in sock_group:
				#if sock != cliSock:
				sendMsg(sock,msg)
				
############################################################
# Will be called by the thread that handles a single client
# @param clisock - the client socket
# @param userName - the user name to serve
#############################################################

def serviceTheClient(cliSock, userName, userToSock):
	
	# Keep servicing the client until it disconnects
	while cliSock:
		if flags[userToSock[userName]] == False:
			break
		# Receive the data from the client
		cliData = recvMsg(cliSock)
		
		msg = cliData.decode()
		#split cmds so each arguemnt can be iterated through
		cmds = msg.split()
            
		if cmds[0]=="/chatwith":
			socket_group=[]
			
			print("The user sent a group request command: ", msg)
			#take "/chatwith" off so the names are left
			cmds.pop(0)
			for cmd in cmds:
				#add the socket of the user to the sock list
				#---> need to make sure to add the client sock
				socket_group.append(userToSock[cmd])

                                # Add all members to the group 
				userNameToGroupMembershipsDic[cmd] = "Cool"
			
                        # Add the current user to the group
			userNameToGroupMembershipsDic[userName] = "Cool"
			socket_group.append(cliSock)
			groupToSockDic["Cool"] = socket_group
			#print(userNameToGroupMembershipsDic)
			#print(groupToSockDic)
                # Check if the user is a member of any groups
		if userName in userNameToGroupMembershipsDic:

			#print("The user name ", userName, " is in the dictionary")
                    # Get the group of the user
			groupName = userNameToGroupMembershipsDic[userName]
                    
			#print("The user is a member of ", groupName)
                    # Get all the sockets in that group
			groupSocks = groupToSockDic[groupName]
			#print("The group consists of sockets ", groupSocks)
			
			# Forward the message to everyone in the group
			for sock in groupSocks:
		    	# Don't forward to self
				if cliSock != sock:
					sendMsg(sock, "<"+userName+"> "+ msg)

                # The poor loner is not a member of any groups
		else:               
			sendMsg(cliSock, "Hey, loner!")
                     
                     
                     
                     #flags[userToSock[cmd]] = False
				#sendMsg(userToSock[cmd], "Welcome to the group!")
			        	
				#print(userToSock[cmd])
			#socket_group.append(userToSock[userName])
			#print(socket_group)
			
			#groupThread = threading.Thread(target=serviceGroup, args=(socket_group, cliSock,))
			#groupThread.start()


		print("<", userName, "> ",cliData.decode())
		
		# Send the string to the client
		#sendMsg(cliSock, "> " + userName)
		#break
		#if msg == "exit":
			# Hang up the client
			#cliSock.close()
flags={}
# Server loop
while True:
	
	# Accept the connection
	clienComSock, cliInfo = listenSock.accept()


	print("New client connected: ", cliInfo)
	
	userName = auth(clienComSock)
	
	# The user name to socket	
	userNameToSockDic[userName] = clienComSock
	
	flags[userNameToSockDic[userName]]=True
	
	# Create a new thread
	cliThread = threading.Thread(target=serviceTheClient, args=(clienComSock,userName,userNameToSockDic,))
	
	# Start the thread
	cliThread.start()
	
	
	
	
	
