#!/usr/bin/env python3

########################################################################

import socket
import argparse
import time
import sys
import threading
import errno
import struct

###############################################################
# Functions used to create multicast sockets to send or receive
###############################################################

#function used to create multicast sockets - for multiple chat rooms
#to receive messages from multiple clients by creating a socket with a "group IP"
#returns the socket so that multiple of these multicast sockets with "group IPs" can
#be created
def create_server_multicast_socket(chatRoomAddr,chatRoomPort):
    any_IP = "0.0.0.0"
    try:
        multicast_server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        multicast_server_socket.setblocking(False)
        multicast_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        multicast_server_socket.bind((any_IP,chatRoomPort))
        ############################################################
        # multicast_request must contain a bytes object consisting
        # of 8 bytes. The first 4 bytes are the multicast group
        # address. The second 4 bytes are the interface address to
        # be used. An all zeros I/F address means all network
        # interfaces.
        ############################################################
        multicast_if_bytes = socket.inet_aton(any_IP)
        multicast_group_bytes = socket.inet_aton(chatRoomAddr)
        multicast_request = multicast_group_bytes + multicast_if_bytes
        multicast_server_socket.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,multicast_request)
        multicast_server_socket.settimeout(1)

    except Exception as msg:
        print(msg)
        sys.exit(1)
    return multicast_server_socket


########################################################################
# 
#
#
#
#
#
#                       ECHO CLIENT SERVER CLASS
#
#
#
#
#
#
########################################################################

class Server:

    HOSTNAME = "0.0.0.0" # socket.gethostname()
    CDR_PORT = 50000

    RECV_SIZE = 1024
    BACKLOG = 10
    
    MSG_ENCODING = "utf-8"
    chatroom_socket_thread_track_history_dict = {} #dictionary of: "chatroom name": (ChatRoomSocket, (ChatRoomAddr,ChatRoomPort),ChatRoomThread,[]) - empty list used to store chat log

    def __init__(self):
        self.thread_list = []
        self.create_listen_socket()
        self.process_connections_forever()

    def create_listen_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Get socket layer socket options.
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind socket to socket address, i.e., IP address and port.
            self.socket.bind( (Server.HOSTNAME, Server.CDR_PORT) )

            # Set socket to listen state.
            self.socket.listen(Server.BACKLOG)
            print("Chat Room Directory Server listening on port {} ...".format(Server.CDR_PORT))

        except Exception as msg:
            print(msg)
            sys.exit(1)





    def process_connections_forever(self):
        try:
            while True:
                new_client = self.socket.accept()

                # A new client has connected. Create a new thread and
                # have it process the client using the connection
                # handler function.
                new_thread = threading.Thread(target=self.connection_handler,
                                              args=(new_client,))

                # Record the new thread.
                self.thread_list.append(new_thread)

                # Start the new thread running.
                #print("Starting serving thread: ", new_thread.name)
                new_thread.daemon = True
                new_thread.start()

        except Exception as msg:
            print(msg)
        except KeyboardInterrupt:
            print()
        finally:
            print("Closing server socket ...")
            self.socket.close()
            sys.exit(1)

    def connection_handler(self, client):
        self.cur_connection, self.cur_address_port = client
        cur_connection, cur_address_port = client
        print("-" * 72)
        print("Connection received from {}.".format(cur_address_port))


        while True:
            # Receive bytes over the TCP connection. This will block
            # until "at least 1 byte or more" is available.
            recvd_bytes = cur_connection.recv(Server.RECV_SIZE) 
            
            # If recv returns with zero bytes, the other end of the
            # TCP connection has closed (The other end is probably in
            # FIN WAIT 2 and we are in CLOSE WAIT.). If so, close the
            # server end of the connection and get the next client
            # connection.
            #print(recvd_bytes)
            if len(recvd_bytes) == 0:
                print("Closing {} client connection ... ".format(cur_address_port))
                cur_connection.close()
                break
                
            # Decode the received bytes back into strings. Then output
            # them.
            self.recvd_str = recvd_bytes.decode(Server.MSG_ENCODING)
            print("Received: "+ self.recvd_str +" cmd") #used for debugging (may want to comment out later)
            self.recvd_str_arr = self.recvd_str.split(" ")

            if self.recvd_str_arr[0] == Client.LIST_CMD:
                self.send_output_list(client)
            elif self.recvd_str_arr[0] == Client.CREATE_CMD:
                self.determine_correct_create_array()
                self.create_chatroom()
            elif self.recvd_str_arr[0] == Client.DELETE_CMD:
                self.determine_correct_delete_array()
                self.do_delete()
            elif self.recvd_str_arr[0] == Client.REPLAY_CMD:
                self.determine_correct_replay_array()
                self.do_Replay(client)
            elif self.recvd_str_arr[0] == Client.BYE_CMD:
                print(threadName, "Closing client connection ... ")
                cur_connection.close()
            else:
                pass


    ##################################
    #### HANDLE LIST CMD SERVER SIDE #
    ##################################

    def send_output_list(self,client):

        self.outputlist_str = ""
        cur_connection, cur_address_port = client
        
        #str to seperate chars: ^]
        #str to sep different entries:\n

        for (chatroomname,addr_port) in Server.chatroom_socket_thread_track_history_dict.items():
            addr,port = addr_port[1] #addr_port[1] returns the tuple of the socket object which contains the IP addr and port #
            port = str(port)
            self.outputlist_str += chatroomname + "^]" + addr + "^]" + port + "\n" #seperate all values by "^]", then seperate different chatrooms by "\n"
        
        if self.outputlist_str == "": #no entries in dictionary
            self.outputlist_str = "CRD is empty"
            
        cur_connection.sendall(self.outputlist_str.encode(Server.MSG_ENCODING))

        

    ##################################
    ##################################
    ##################################

        
        

    ################################
    #### HANDLE DELETE SERVER SIDE #
    ################################

    def determine_correct_delete_array(self):
        self.correct_delete_chat_arr = ["delete",""] #output will be 2 col array
        if len(self.recvd_str_arr) == 2:
            self.correct_delete_chat_arr = self.recvd_str_arr

        if len(self.recvd_str_arr) > 2:
            i = 1
            j = 1
            while i < len(self.recvd_str_arr):
                
                self.correct_delete_chat_arr [j] += self.recvd_str_arr[i]
                
                if i < len(self.recvd_str_arr) -1:
                    self.correct_delete_chat_arr [j] += " "
                else:
                    pass
                i+=1
                
    def do_delete(self):
        ChatRoomName = self.correct_delete_chat_arr[1] #use proper array (that accounted for whitespaces in chatroom name)
        if ChatRoomName in Server.chatroom_socket_thread_track_history_dict: #case in which the chatroom name is actually in the dictionary
            del Server.chatroom_socket_thread_track_history_dict[ChatRoomName]
            print("Success. Deleted chatroom: " +ChatRoomName + ".") 
        else:
            print("Chatroom: " +ChatRoomName + " does not exist.") 
        

    ################################
    ################################
    ################################
                




    ################################
    #### HANDLE CREATE SERVER SIDE #
    ################################

    def determine_correct_create_array(self):
        self.correct_create_chat_arr = ["create","","",""] #output will be 4 col array
        if len(self.recvd_str_arr) == 4:
            self.correct_create_chat_arr = self.recvd_str_arr
            
        if len(self.recvd_str_arr) > 4:
            i = 1
            j = 1
            while i < len(self.recvd_str_arr):

                if i <len(self.recvd_str_arr) - 3:
                    self.correct_create_chat_arr [j] += self.recvd_str_arr[i] + " "
                    
                elif i <len(self.recvd_str_arr) - 2:
                    self.correct_create_chat_arr [j] += self.recvd_str_arr[i]
                else:
                    j+=1
                    self.correct_create_chat_arr [j]= self.recvd_str_arr[i]
                    
                i+=1


    #method to actually create the chatroom on the server end
    def create_chatroom(self):
        ChatRoomName, ChatRoomAddr, ChatRoomPort = self.correct_create_chat_arr[1:] #this works since this array is: ["create",<chatroom name>,IP addr,port]
        ChatRoomPort = int(ChatRoomPort)
        #if-else catch for rooms that are created of the same IP + port number
        if len(Server.chatroom_socket_thread_track_history_dict) == 0: #case where there's nothing in the dictionary (i.e.: CRD is empty)
        
            ChatRoomSocket = create_server_multicast_socket(ChatRoomAddr, ChatRoomPort) #create a receive socket to add the chatroomaddr group IP to the multicast membership - enables server to listen to chat msgs
            print("Created the chatroom: " + ChatRoomName + " with IP addr: " + ChatRoomAddr + " and port: " + str(ChatRoomPort))
            ChatRoomThread = threading.Thread(target = self.record_chatroom_activity,args = (ChatRoomName,))#thread to this to ensure that any activity in the chatrooms is recorded in the dictionary's arr
            Server.chatroom_socket_thread_track_history_dict[ChatRoomName] = (ChatRoomSocket, (ChatRoomAddr,ChatRoomPort),ChatRoomThread,[]) #make a dictionary field of: {receive socket, tuple of IP,port #, the thread handling chatrecording, and an empty arr which will store a chatlog           
            ChatRoomThread.daemon = True
            ChatRoomThread.start()

        else:
            same_addr_and_port = False
            same_room_name = False
	    #loop through dictionary to see if there is an attempt to create a chatroom with IP + port in use or a chatroom with the same name trying to be created
            for (j,k) in Server.chatroom_socket_thread_track_history_dict.items():
		#catch for same IP and port being used in new chatroom
                if k[1][0] == ChatRoomAddr and k[1][1] == ChatRoomPort:
                    same_addr_and_port = True
                    break
		#catch for same name as existing name used in new chatroom
                if j == ChatRoomName:
                    same_room_name = True
                    
            if same_addr_and_port == True:
                print("Trying to create a chatroom with the same IP + port that already exists. Error")

            elif same_room_name == True:
                print("Trying to create a chatroom name that is already in use. Error")
            
            else:
                ChatRoomSocket = create_server_multicast_socket(ChatRoomAddr, ChatRoomPort) #create a receive socket to add the chatroomaddr group IP to the multicast membership - enables server to listen to chat msgs 
                print("Created the chatroom: "+ ChatRoomName + " with IP addr: " + ChatRoomAddr + " and port: " + str(ChatRoomPort))
                ChatRoomThread = threading.Thread(target = self.record_chatroom_activity,args = (ChatRoomName,)) #thread to this to ensure that any activity in the chatrooms is recorded in the dictionary's arr
                Server.chatroom_socket_thread_track_history_dict[ChatRoomName] = (ChatRoomSocket, (ChatRoomAddr,ChatRoomPort),ChatRoomThread,[]) #make a dictionary field of: {receive socket, tuple of IP,port #, the thread handling chatrecording, and an empty arr which will store a chatlog

                ChatRoomThread.daemon = True
                ChatRoomThread.start()        










    #method used to keep track of msgs sent in a specific chatroom 
    def record_chatroom_activity(self,chatroom):
        ChatRoomSocket = Server.chatroom_socket_thread_track_history_dict[chatroom][0] #get the created receive multicast socket  - enables server to listen to chat msgs 
        print("chatroom recorder running for chatroom: " + chatroom)
        
        while True:
            try:
                chatmsgs,addr = ChatRoomSocket.recvfrom(Server.RECV_SIZE) #receives chat msgs from the multicast socket
                chatmsgs = chatmsgs.decode(Server.MSG_ENCODING)
                Server.chatroom_socket_thread_track_history_dict[chatroom][len(Server.chatroom_socket_thread_track_history_dict[chatroom])-1].append(chatmsgs) #add to chatroom's chatlog list/array
            except KeyboardInterrupt:
                print()
                exit()
            except Exception as msg:
                pass



    ################################
    ################################
    ################################

                

    ################################
    #### HANDLE REPLAY SERVER SIDE #
    ################################

    def determine_correct_replay_array(self):
        self.correct_replay_chat_arr = ["replay",""] #output will be 2 col array
        if len(self.recvd_str_arr) == 2:
            self.correct_replay_chat_arr  = self.recvd_str_arr 
                        
        if len(self.recvd_str_arr) > 2:
            i = 1
            j = 1
            while i < len(self.recvd_str_arr):
                self.correct_replay_chat_arr[j] += self.recvd_str_arr[i]
                if i < len(self.recvd_str_arr) -1:
                    self.correct_replay_chat_arr[j]+=" "
                else:
                    pass
                i+=1

    def do_Replay(self,client):
        ChatRoomName = self.correct_replay_chat_arr[1] #get the correct chatroom name from determine_correct_replay_array method
        cur_connection, cur_address_port = client
        print("Trying to replay msgs from chatroom: " + ChatRoomName)
        if ChatRoomName in Server.chatroom_socket_thread_track_history_dict: #if the chatroom actually has been created
            ChatLog = Server.chatroom_socket_thread_track_history_dict[ChatRoomName][len(Server.chatroom_socket_thread_track_history_dict[ChatRoomName])-1]
            
            if len(ChatLog) == 0: # empty array (no msgs in chat)
                ChatLog = ["No chat activity in chatroom " + ChatRoomName]
            str_to_send = "\n".join(ChatLog)
            cur_connection.sendall(str_to_send.encode(Server.MSG_ENCODING))#send array within the dictionary (of chat log) seperated by "\n"
        else: #if the chatroom has not been created yet
            chatroom_DNE_str = "The chatroom: " + ChatRoomName + " has not been created yet."
            cur_connection.sendall(chatroom_DNE_str.encode(Server.MSG_ENCODING))


    ################################
    ################################
    ################################




        



                


########################################################################
# 
#
#
#
#                       ECHO CLIENT CLASS
#
#
#
#
#
########################################################################

class Client:

    # Set the server hostname to connect to. If the server and client
    # are running on the same machine, we can use the current
    # hostname.
    SERVER_HOSTNAME = socket.gethostname()

    RECV_BUFFER_SIZE = 1024
    
    #Main commands (when not connected)
    CONNECT_CMD = "connect"
    NAME_CMD = "name"
    CHAT_CMD = "chat"

    #client-to-CRDS commands (when connected)
    LIST_CMD = "list"
    CREATE_CMD = "create"
    DELETE_CMD = "delete"
    REPLAY_CMD = "replay"
    BYE_CMD = "bye"

    TTL = 15 #ttl sets the number of subnetworks that the multicast packets can traverse
    TTL_BYTE = struct.pack('B', TTL)
    

    def __init__(self):
        while True:
            self.create_client_multicast_socket() #create multicast socket to transmit UDP packets to the "multicast group"
            self.chatroom_addr_port_dict = {} #create empty dictionary to store tuple of ("ip addr",port #) associated w/each chatroom name
            self.name = "user: " #provided name before any sort of change
            self.TCP_est = 0 # variable to indicate if TCP connection is established (0 = not, 1 = established)
            while True:
                
                #TCP connection is not established yet => "main prompt"
                if self.TCP_est == 0:
                    
                    self.get_main_command_input() #get "main command" from client (before TCP connection)

                    #CONNECT CMD:
                    #client wants to connect to CRDS - Chat Room Directory Server
                    if self.main_cmd_input_text == Client.CONNECT_CMD:
                        self.create_TCP_socket_connect_to_server()
                        self.TCP_est = 1 #TCP connection established
                        continue

                    #NAME <USERNAME> CMD:
                    #client wants to set his/her username
                    if self.main_cmd_input_text.split(" ")[0] == Client.NAME_CMD:
                        self.name_arr = self.main_cmd_input_text.split(" ")
                        self.name = ""
                        if len(self.name_arr)< 2: #input must be at least 2 in length i.e.: ["name",<username>]
                            print("Invalid name command. Try again.")
                            continue
                        else:
                            self.set_client_name()

                    #chat <chatroom> CMD:
                    if self.main_cmd_input_text.split(" ")[0] == Client.CHAT_CMD:
                        
                        self.chatroom_arr = self.main_cmd_input_text.split(" ")
                        self.chatroom = ""
                        if len(self.chatroom_arr)< 2: #input must be at least 2 in length i.e.: ["chat",<chatroom>]
                            print("Invalid chat command. Try again.")
                            continue
                        else:
                            self.set_chatroom_name() #method used to get proper chatroom (accounts for spaces in the chatroom)
                            self.go_to_chat_mode() #method used to start chat in the chatroom


                #TCP connection is established => "CRDS prompt"                
                if self.TCP_est == 1:
                    
                    self.get_client_to_CRDS_input() #client to Chat Room Directory Server prompt
                    

                    #list CMD:
                    if self.client_to_CRDS_cmd_input_text == Client.LIST_CMD:
                        self.get_and_output_list() #receive and print chatroom list from the Server

                    
                    #create <chatroom name> <IP addr> <port> CMD:
                    if self.client_to_CRDS_cmd_input_text.split(" ")[0] == Client.CREATE_CMD:
                        self.create_chat = ""
                        self.create_chat_arr = self.client_to_CRDS_cmd_input_text.split(" ")
                        if len(self.create_chat_arr)< 4: #ensure that input is at least 4 length long arr: ["create", <chatroom name>,<IP addr>,<port #>]
                            print("Invalid create chatroom command. Try again.")
                            continue
                        else:
                            self.get_create_chatroom_name() #method used to get proper chatroom (accounts for spaces in the chatroom)
                            admin_scope_IP_multicast_range_start = '239.0.0.0' 
                            admin_scope_IP_multicast_range_end = '239.255.255.255'
                            IP_to_check = self.correct_create_chat_arr[2] #gets string of input IP addr (from CRDS input)
                            in_range = self.check_ipv4_in_range(IP_to_check,admin_scope_IP_multicast_range_start,admin_scope_IP_multicast_range_end) #check if IP of chatroom is between 239.0.0.0 - 239.255.255.255
                            if in_range:
                                self.do_chatroom_create() #create chatroom only if IP is within 239.0.0.0 to 239.255.255.255
                            else:
                                print("Invalid IP input. Valid IPs are from: 239.0.0.0 to 239.255.255.255")
                                continue

                            

                        

                    #delete <chatroom> CMD:
                    if self.client_to_CRDS_cmd_input_text.split(" ")[0] == Client.DELETE_CMD:
                        self.delete_chat_arr = self.client_to_CRDS_cmd_input_text.split(" ")
                        self.delete_chat = ""
                        if len(self.delete_chat_arr)< 2: #input must be at least 2 in length i.e.: ["delete",<chatroom>]
                            print("Invalid delete chatroom command. Try again.")
                            continue
                        
                        else:
                            self.get_delete_chatroom_name()#method used to get proper chatroom (accounts for spaces in the chatroom)
                            self.do_chatroom_delete() #method used to delete chatroom
                            


                    #replay <chatroom> CMD:
                    if self.client_to_CRDS_cmd_input_text.split(" ")[0] == Client.REPLAY_CMD:
                        self.replay_chat_arr = self.client_to_CRDS_cmd_input_text.split(" ")
                        self.replay_chat = ""
                        if len(self.replay_chat_arr)< 2: #input must be at least 2 in length i.e.: ["replay",<chatroom>]
                            print("Invalid replay chatroom command. Try again.")
                            continue
                        else:
                            self.get_replay_chatroom_name() #method used to get proper chatroom (accounts for spaces in the chatroom)
                            self.do_replay() #method used to replay chatroom log

                                                
                        
                    #bye CMD:    
                    if self.client_to_CRDS_cmd_input_text == Client.BYE_CMD:
                        self.TCP_socket.close()
                        self.TCP_est = 0


    ##################################################
    ## METHODS FOR HANDLING CLIENT END "CONNECT" CMD #
    ##################################################

                        
    #Method for creating TCP socket and establishing connection to server (CRDS)
    def create_TCP_socket_connect_to_server(self):
        try:
            # Create an IPv4 TCP socket.
            self.TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.TCP_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.TCP_socket.connect((Client.SERVER_HOSTNAME, Server.CDR_PORT))  
        except Exception as msg:
            print(msg)
            sys.exit(1)

    ##################################################
    ##################################################
    ##################################################

    #added for lab 4 - create multicast socket to transmit UDP packets to the "multicast group"
    def create_client_multicast_socket(self):
        try:
            self.multicast_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.multicast_client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, Client.TTL_BYTE)
        except Exception as msg:
            print(msg)
            sys.exit(1)


    ##################################################
    ## METHODS FOR HANDLING CLIENT END "NAME" CMD    #
    ##################################################
    
    #added for lab 4 - set the client's name followed by : (i.e.: "Alex: ") 
    def set_client_name(self):
        
        if len(self.name_arr) == 2:
            self.name = self.name_arr[1] + ": "
        
        if len(self.name_arr) > 2: #accounts for spaces inbetween the input name
            i = 1
            while i < len(self.name_arr):
                self.name += self.name_arr[i]
                if i < len(self.name_arr) -1:
                    self.name+=" "
                else:
                    self.name+=": "
                i+=1
        print("Name changed. \nWhen in chat mode, " + self.name + " will come before anything you type")

        

    ##################################################
    ##################################################
    ##################################################
                


    ####################################################
    ## METHODS FOR HANDLING CLIENT END CHATROOM CREATE #
    ####################################################

    #added for lab 4 - determine full chatroom name (in case chatroom has any space inbetween) - gets string and array outputs
    def get_create_chatroom_name(self):
        self.correct_create_chat_arr = ["create","","",""] #output will be 4 col array
        if len(self.create_chat_arr) == 4:
            self.create_chat = self.create_chat_arr[1] + " " + self.create_chat_arr[2] + " " +self.create_chat_arr[3] 
            self.correct_create_chat_arr = self.create_chat_arr
            
        if len(self.create_chat_arr) > 4: #accounts for spaces inbetween the chatroom name
            i = 1
            j = 1
            while i < len(self.create_chat_arr):

                if i <len(self.create_chat_arr) - 3:
                    self.correct_create_chat_arr [j] += self.create_chat_arr[i] + " "
                    
                elif i <len(self.create_chat_arr) - 2:
                    self.correct_create_chat_arr [j] += self.create_chat_arr[i]
                else:
                    j+=1
                    self.correct_create_chat_arr [j]= self.create_chat_arr[i]
                    
                self.create_chat += self.create_chat_arr[i]
                if i < len(self.create_chat_arr) -1:
                    self.create_chat+=" "
                else:
                    pass
                i+=1
 
    #method to create the chatroom     
    def do_chatroom_create(self):
        #send create <chatroom name> to server to get it to handle chatroom create
        self.create_str_to_send = "create " + self.create_chat
        self.connection_send(self.create_str_to_send) #ON THE SERVER SIDE, CHECK IF LENGTH RECEIVED IS > 4, IF SO, LAST 2 INDEX IS <IP> <PORT>, 1st index is "create"

        ChatRoomName,ChatRoomAddr,ChatRoomPort = self.correct_create_chat_arr[1:]
        ChatRoomPort = int(ChatRoomPort)
        
        #if-else catch for rooms that are created of the same IP + port number OR same chatroom name - DO SAME THING ON SERVER END!!
        
        if len(self.chatroom_addr_port_dict) == 0:
            self.chatroom_addr_port_dict[ChatRoomName] = (ChatRoomAddr,ChatRoomPort) #keep dictionary of tuples updated
        else:
            same_addr_and_port = False
            same_room_name = False
            
            #loop through dictionary items
            for (j,k) in self.chatroom_addr_port_dict.items():
                if k[0][0] == ChatRoomAddr and k[0][1] == ChatRoomPort: #same IP and port already in use
                    same_addr_and_port = True
                    break
                if j == ChatRoomName: #same chatroom name already in use
                    same_room_name = True  
                    break
                
            if same_addr_and_port == True:
                print("Trying to create a chatroom with the same IP + port that already exists. Error")

            elif same_room_name == True:
                print("Trying to create a chatroom name that is already in use. Error")
            
            else:
                 self.chatroom_addr_port_dict[ChatRoomName] = (ChatRoomAddr,ChatRoomPort) #keep dictionary of tuples updated



    #method for creating tuples of IP addrs
    def create_IPv4_tuple(self,IPv4_str):
        return tuple(int(n) for n in IPv4_str.split('.'))

    #method for checking if the IPv4 addr is in range of: (start, end) IP addrs - used to check if client input addr is within 239.0.0.0 - 239.255.255.255
    def check_ipv4_in_range(self,addr, start, end):
        return self.create_IPv4_tuple(start) <= self.create_IPv4_tuple(addr) <= self.create_IPv4_tuple(end)
            

    ##################################################
    ##################################################
    ##################################################



                 
    ###################################################
    ## METHODS FOR HANDLING CLIENT END CHATROOM DELETE#
    ###################################################    

    #added for lab 4 - determine full delete chatroom name (in case chatroom has any space inbetween)
    def get_delete_chatroom_name(self):
        self.correct_delete_chat_arr = ["delete",""] #output will be 2 col array
        if len(self.delete_chat_arr) == 2:
            self.delete_chat = self.delete_chat_arr[1]
            self.correct_delete_chat_arr = self.delete_chat_arr

        if len(self.delete_chat_arr) > 2: #accounts for spaces inbetween the chatroom name
            i = 1
            j = 1
            while i < len(self.delete_chat_arr):
                
                self.correct_delete_chat_arr [j] += self.delete_chat_arr[i]     
                self.delete_chat += self.delete_chat_arr[i]
                if i < len(self.delete_chat_arr) -1:
                    self.delete_chat+=" "
                    self.correct_delete_chat_arr [j] += " "
                else:
                    pass
                i+=1
        
    #handle delete <chatroom>    
    def do_chatroom_delete(self):
        self.delete_str_to_send = "delete " + self.delete_chat
        self.connection_send(self.delete_str_to_send) #send delete <chatroom name> to server
        ChatRoomName = self.delete_chat #chatroom name to delete
        #check if entry is in dictionary. If so, remove it from dictionary
        if ChatRoomName in self.chatroom_addr_port_dict:
            del self.chatroom_addr_port_dict[ChatRoomName]
        


    ##################################################
    ##################################################
    ##################################################


            

    ####################################################
    ## METHODS FOR HANDLING CLIENT END CHATROOM REPLAY #
    ####################################################         

    #added for lab 4 - determine full replay chatroom name (in case chatroom has any space inbetween)
    def get_replay_chatroom_name(self):
        if len(self.replay_chat_arr) == 2:
            self.replay_chat = self.replay_chat_arr[1] 
                        
        if len(self.replay_chat_arr) > 2: #accounts for spaces inbetween the chatroom name
            i = 1
            while i < len(self.replay_chat_arr):
                self.replay_chat += self.replay_chat_arr[i]
                if i < len(self.replay_chat_arr) -1:
                    self.replay_chat+=" "
                else:
                    pass
                i+=1
 
    #send replay cmd to server, and get the "replayed" string from the server (chatlog) + print it out
    def do_replay(self):
        self.replay_str_to_send = "replay " + self.replay_chat
        self.connection_send(self.replay_str_to_send)
        self.connection_receive()


    ##################################################
    ##################################################
    ##################################################



    ###############################################
    ## METHODS FOR HANDLING CLIENT END "List" CMD #
    ###############################################
    
    def get_and_output_list(self):
        
            self.connection_send(self.client_to_CRDS_cmd_input_text) #send "list" request to server
            self.connection_receive_no_print()# get back empty string or strings which represent the chatroom name
            recvd_str = self.recvd_from_server
            for messy_room_info in recvd_str.split("\n"):
                room_id = messy_room_info.split("^]")
                #account for cases where CDR is empty
                if len(room_id) == 1:
                    print(" ".join(room_id))
                    print("\n")
                    
                #cases where CDR is not empty
                if len(room_id) == 3:
                    print(" ".join(room_id))
                    ChatRoomName, ChatRoomAddr, ChatRoomPort = room_id
                    ChatRoomPort = int(ChatRoomPort)
                    self.chatroom_addr_port_dict[ChatRoomName] = (ChatRoomAddr,ChatRoomPort)
                    
                    
    ###############################################
    ###############################################
    ###############################################

                    
                    
                
    #################################################################
    ## METHODS FOR HANDLING main input prompt and CRDS input prompt #
    #################################################################
    
    #added for lab 4
    def get_main_command_input(self):
        # In this version we keep prompting the user until a non-blank
        # line is entered.
        print("Main commands options:\n1)connect \n2)name <chat name> \n3)chat <chat room name>\n")
        while True:
            self.main_cmd_input_text = input("main> ")
            if self.main_cmd_input_text != "":
                break
            
    #added for lab 4
    def get_client_to_CRDS_input(self):
        # In this version we keep prompting the user until a non-blank
        # line is entered.
        print("Chat Room Directory Server (CRDS) commands options:\n1)create <chat room name> <IP addr (range: 239.0.0.0 to 239.255.255.255)> <port> \n2)list \n3)delete <chat room name> \n4)replay <chat room name> \n5)bye\n")
        while True:
            self.client_to_CRDS_cmd_input_text = input("CRDS> ")
            if self.client_to_CRDS_cmd_input_text != "":
                break

    
    #################################################################
    #################################################################
    #################################################################


            

    ############################################
    ## METHODS FOR HANDLING CLIENT END CHAT CMD#
    ############################################

    #added for lab 4 - determine full chatroom name (in case chatroom has any space inbetween)
    def set_chatroom_name(self):
        self.correct_chatroom_arr = ["chat", ""] #array is only 2 col: ["chat", <chatroom name>]
        if len(self.chatroom_arr) == 2:
            self.chatroom = self.chatroom_arr[1]
            self.correct_chatroom_arr = self.chatroom_arr
        
        if len(self.chatroom_arr) > 2: #accounts for spaces inbetween the chatroom name
            i = 1
            j = 1
            while i < len(self.chatroom_arr):
                self.correct_chatroom_arr[j]+=self.chatroom_arr[i]
                self.chatroom += self.chatroom_arr[i]
                if i < len(self.chatroom_arr) -1:
                    self.chatroom+=" "
                    self.correct_chatroom_arr[j]+=" "
                else:
                    pass
                i+=1

    
    #added for lab 4 - "chatroom prompt"
    def get_chatroom_input(self,ChatRoomName = ""):

        self.in_chat = 1 #variable to indicate that we are in chat mode (1 = chat mode, 0 = not chat mode)
        print("Welcome to the chatroom, " + ChatRoomName +".\All users in the chatroom will receive your messages. Enjoy!")
        while True:
            chatroom_txt = input("chat > ")
            if chatroom_txt == "":
                continue
            #escape character is: ^[ (hex 1B == ^[ == ctrl [)
            elif chatroom_txt == '\x1b': 
                self.in_chat = 0
                break
            else:
                #send w/e we got from the user to the chat room (multicast group socket)
                self.multicast_client_socket.sendto((self.name+ chatroom_txt).encode(Server.MSG_ENCODING),self.chatroom_addr_port_dict[ChatRoomName])

    def go_to_chat_mode(self):
        ChatRoomName = self.chatroom

        #only proceed to "chat mode" if the chatroom name is already in the dictionary
        if ChatRoomName in self.chatroom_addr_port_dict:
            
                ChatRoomAddr, ChatRoomPort = self.chatroom_addr_port_dict[ChatRoomName]
                Remote_ChatRoomSocket = create_server_multicast_socket(ChatRoomAddr,ChatRoomPort) #create a remote multicast socket which will receive from multiple clients (IFF they join the chat (or the multicast group))
                print('Use ^[ ( ctrl [ ) to exit the chatroom')
                self.in_chat = 1 #indicate we are in chat mode

                #start a new thread for chatroom communication from this client.
                #The main thread (calling thread) deals with chat input from other clients 
                
                
                new_chat_thread = threading.Thread(target = self.get_chatroom_input, args = (ChatRoomName,))
                new_chat_thread.daemon = True
                new_chat_thread.start()

                while True:
                    #If the client leaves the chatroom close the
                    #chat room socket that this particular client is
                    #sending UDP packets to
                    if self.in_chat == 0:
                        Remote_ChatRoomSocket.close()
                        break
                    try:
                        txt,IP_addr = Remote_ChatRoomSocket.recvfrom(Server.RECV_SIZE)
                        txt = txt.decode(Server.MSG_ENCODING)
                        print(txt) #display chatroom input for all clients
                    except socket.timeout:
                        pass
                    except KeyboardInterrupt:
                        print()
                        break
                    except Exception as msg:
                        print(msg)
                        roomSocket.close()
            
        
            
    #########################################
    #########################################
    #########################################

                        

                
    def connection_send(self,msg_to_send):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
            self.TCP_socket.sendall(msg_to_send.encode(Server.MSG_ENCODING))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive(self):
        try:
            # Receive and print out text. The received bytes objects
            # must be decoded into string objects.
            recvd_bytes = self.TCP_socket.recv(Client.RECV_BUFFER_SIZE)

            # recv will block if nothing is available. If we receive
            # zero bytes, the connection has been closed from the
            # other end. In that case, close the connection on this
            # end and exit.
            if len(recvd_bytes) == 0:
                print("Closing server connection ... ")
                self.TCP_socket.close()
                sys.exit(1)

            print("Received: ", recvd_bytes.decode(Server.MSG_ENCODING))
            self.recvd_from_server = recvd_bytes.decode(Server.MSG_ENCODING)

        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive_no_print(self):
        try:
            # Receive and print out text. The received bytes objects
            # must be decoded into string objects.
            recvd_bytes = self.TCP_socket.recv(Client.RECV_BUFFER_SIZE)

            # recv will block if nothing is available. If we receive
            # zero bytes, the connection has been closed from the
            # other end. In that case, close the connection on this
            # end and exit.
            if len(recvd_bytes) == 0:
                print("Closing server connection ... ")
                self.TCP_socket.close()
                sys.exit(1)

            self.recvd_from_server = recvd_bytes.decode(Server.MSG_ENCODING)

        except Exception as msg:
            print(msg)
            sys.exit(1)

########################################################################
# Process command line arguments if this module is run directly.
########################################################################

# When the python interpreter runs this module directly (rather than
# importing it into another file) it sets the __name__ variable to a
# value of "__main__". If this file is imported from another module,
# then __name__ will be set to that module's name.

if __name__ == '__main__':
    roles = {'client': Client,'server': Server}
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--role',
                        choices=roles, 
                        help='server or client role',
                        required=True, type=str)

    args = parser.parse_args()
    roles[args.role]()

########################################################################






