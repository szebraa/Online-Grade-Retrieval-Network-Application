
"""
BY: Alex Szebrag 

to create a Client: "python EchoClientServer.py -r client" 
to create a Server: "python EchoClientServer.py -r server" 

or you can import the module into another file, e.g., 
import EchoClientServer

"""

########################################################################

import socket
import argparse
import sys
import threading
import os
import time
import datetime


########################################################################
# Echo Server class
########################################################################

class Server:

    # Set the server hostname used to define the server socket address
    # binding. Note that 0.0.0.0 or "" serves as INADDR_ANY. i.e.,
    # bind to all local network interface addresses.
    HOSTNAME = "0.0.0.0"

    # Set the server port to bind the listen socket to. TCP and UDP ports
    FSP_PORT = 30001 #File sharing port (TCP file sharing connection port)
    SDP_PORT = 56926 #added for lab 3 - Service Discovery Port
	
    #common client-server FTP command constants  added - lab 3	
    SCAN_CMD = "scan" #added for lab 3
    RLIST_CMD = "rlist" #added for lab 3
    PUT_CMD = "put"
    GET_CMD = "get"
    BYE_CMD = "bye" #added for lab 3
    PUT_RESP = "ok" 
    CONNECT_CMD = "connect " + socket.gethostbyname(socket.gethostname()) +" "+ str(FSP_PORT) #added for lab 3 "connect 192.168.0.33 30001"

    #common file paths added for lab 3 TO CHANGE EVERYTIME U MOVE FOLDERS!!
    CLIENT_LOCAL_DIRECTORY = "C:\\Users\\Alex\\Desktop\\Electrical engineering\\4th year (round 2)\\term 2\\Comp Eng 4DN4\\labs\\3\\4DN4_lab_3\\Code\\client_local_files"
    READ_CLIENT_LOCAL_DIRECTORY = r"C:\Users\Alex\Desktop\Electrical engineering\4th year (round 2)\term 2\Comp Eng 4DN4\labs\3\4DN4_lab_3\Code\client_local_files"
    SERVER_SHARING_DIRECTORY = "C:\\Users\\Alex\\Desktop\\Electrical engineering\\4th year (round 2)\\term 2\\Comp Eng 4DN4\\labs\\3\\4DN4_lab_3\\Code\\server_shared_files"
    READ_SERVER_SHARING_DIRECTORY = r"C:\Users\Alex\Desktop\Electrical engineering\4th year (round 2)\term 2\Comp Eng 4DN4\labs\3\4DN4_lab_3\Code\server_shared_files"

    #added constants for response to getting scan string from client - lab 3
    MSG = "Alex's File Sharing Service"
    MSG_ENCODING = "utf-8"    
    MSG_ENCODED = MSG.encode(MSG_ENCODING)
    SERVICE_DISCOVERY_MSG = "SERVICE DISCOVERY"
	
    #size of texts and files (bytes) that can be received at a time (added for lab 3) 
    RECV_SIZE = 1024 #added for lab 3
    RECV_BUFFER_SIZE = 1024
    FILE_RECV_BUFFER = 4096 #file "download/upload" rate (bytes)
    MAX_CONNECTION_BACKLOG = 10
    

    # Create server socket address. It is a tuple containing
    # address/hostname and port.
    SOCKET_ADDRESS_TCP = (HOSTNAME, FSP_PORT)

    SOCKET_ADDRESS_UDP = (HOSTNAME, SDP_PORT) #added for lab 3

    def __init__(self):
        self.thread_list = [] #added for lab 3 - list of "connection" threads for multiple TCP connections
        self.put_thread_list = [] #added for lab 3 - list of "put" file threads for threaded puts (allows multiple clients to put file in shared directory)
        self.lock = threading.Lock() #create a "lock" to lock the thread (used later to ensure correct simultaneously file "put")
        self.get_shared_directory()#added for lab 3 - get list of remote files (available for sharing)
        self.print_shared_directory()#added for lab 3 - print remote files (available for sharing)
        self.create_listen_and_broadcast_sockets() #setup TCP and UDP sockets for server
		
        while True: #process TCP connections + UDP received bytes forever
            try: #used to catch the case in which os.remove() removes an invalid file (in the except branch)
                try: #used to capture the case in which the server is closed
                    self.receive_forever() #added for lab 3
                except: #ensure that there is no partial file remnant remaining in the shared directory
                    self.file_received.close()
                    try:
                        while True: #remove all files that the client wants to put to the server in the created threads
                            os.remove(self.file_received.name)
                    except:
                        pass
                    print("Closing client connection ... ")
                    self.TCP_socket.close() #close TCP connections
                    break
                    sys.exit(1)
            except: #graceful exit incase we are not "putting" the file into the server directory (i.e.: self.file_received does not exist)
                sys.exit(1)

    #modified for lab 3    
    def create_listen_and_broadcast_sockets(self):
        try:
            #CREATE UDP/SDP socket - added for lab 3
            self.UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create UDP socket, IPv4
            self.UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.UDP_socket.setblocking(False) #added for lab 3 - make accept,receive, and send non-blocking
            self.UDP_socket.bind(Server.SOCKET_ADDRESS_UDP)
            print("Listening for service discovery messages on SDP port {} ...".format(Server.SDP_PORT))

            # Create an IPv4 TCP socket.
            self.TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.TCP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#allows us to reuse the socket without waiting for any timeouts
            self.TCP_socket.setblocking(False) #added for lab 3 - make accept,receive, and send non-blocking
            self.TCP_socket.bind(Server.SOCKET_ADDRESS_TCP)
            self.TCP_socket.listen(Server.MAX_CONNECTION_BACKLOG)
			
            print("Listening for file sharing connections on port {} ...".format(Server.FSP_PORT)) #edited for lab 3
        except Exception as msg:
            print(msg)
            sys.exit(1)

    #added for lab 3- receive  UDP broadcasts forever
    def receive_forever(self):
        while True:
            #try block for UDP broadcasts
            try:
                recvd_UDP_bytes, address = self.UDP_socket.recvfrom(Server.RECV_SIZE)
                recvd_UDP_str = recvd_UDP_bytes.decode(Server.MSG_ENCODING) #Decode the received bytes back into strings.
                
                # Check if the received packet contains a service scan command
                if Server.SERVICE_DISCOVERY_MSG == recvd_UDP_str:
                    self.UDP_socket.sendto(Server.MSG_ENCODED, address) # Send the service advertisement message back to the client
					
            except socket.error:
                pass            
            except KeyboardInterrupt:
                print()
                sys.exit(1)
            
            #try block for TCP connections (threading to allow multiple TCP connections from clients)
            try:
                
                new_client = self.TCP_socket.accept() # A new client has connected.
		# Create a new thread and process the client- thread connection_handler
                new_thread = threading.Thread(target=self.connection_handler,
                                              args=(new_client,))
               
                self.thread_list.append(new_thread)  # Record the new connection thread

                # Start the new thread running.
                #print("Starting serving thread: ", new_thread.name)
                new_thread.daemon = True
                new_thread.start() 
            except socket.error:
                pass
            except Exception as msg:
                print(msg)
            except KeyboardInterrupt:
                print()

    #added for lab 3 - function to find files currently available for sharing (from server)
    def get_shared_directory(self):
        os.chdir(Server.READ_SERVER_SHARING_DIRECTORY) #change directory name when moving from desktop to laptop
        self.rlist_array = os.listdir() #store remote list in an array
        self.rlist_array_size = len(self.rlist_array) #find array size of remote files

    #added for lab 3 - print shared directory (server)
    def print_shared_directory(self):
        print("shared directory files that are available for sharing: ")
        i = 0
        #loop through the array and print all files available for sharing 
        while i<self.rlist_array_size:
            print(self.rlist_array[i])
            i+=1
	
    #method that the thread excutes (used to handle multiple client "puts" at once) 
    def threaded_put_file(self,Client):
	#cur thread locks thread until done with file xfer "put" (so that 2 file "puts" dont interfere with each other)
        with self.lock:
            connection, address_port = Client
            Ip_addr, port_num = address_port
            print("-" * 72)
            print("Put file request received from ",end='')
            print(Ip_addr,end='')
            print(" on port ",end='')
            print(port_num)
	    #double check client issues put command, then store length of file + file name + send ok resp to client
            if self.recvd_str.split("/")[0] == Server.PUT_CMD:
                self.put_file_len = int(self.recvd_str.split("/")[2]) #get file size in bytes
                self.put_file_name = self.recvd_str.split("/")[1] #store file name to be received
                connection.sendall(Server.PUT_RESP.encode(Server.MSG_ENCODING)) #respond back with "ok"
            connection.setblocking(True) #enabled to ensure put works correctly (will not work with no blocking + socket.error exception handler)   
            amount_received = 0 #keep track of how much of the file has been received from client
            self.file_received = open(self.put_file_name,'wb') #create a file of the same name in the server shared dir
			
            #loop until we receive all bytes of the "put"/sent file from the client
	    #in the loop write the bytes that have been received to the opened file in the server dir 
            while(amount_received < self.put_file_len):
                self.get_shared_directory() #ensure we are at the server shared dir each time
                try:
                    enc_file = connection.recv(Server.FILE_RECV_BUFFER) #received bytes from the file the client wants to "put"
                    if enc_file: #ensure that there are still bytes received
                        # write to the file each line received
                        self.file_received.write(enc_file) #copy bytes received from file (sent by client) into newly created file (same name as file sent)
                        amount_received += len(enc_file) # inc amount received by the amount of bytes received from the client
                        print ("Amount received: " + str(amount_received) + " total size: " + str(self.put_file_len))
                    else: #if no bytes are received, close newly created file 
                        self.file_received.close()
                        break
                #except socket.error:
                    #pass
		#both exceptions ensure that no remnant of the file will remain in the servers shared dir
                except KeyboardInterrupt:
                    self.file_received.close()
                    os.remove(self.file_received.name)
                    print("Closing client connection ... ")
                    connection.close()
                    break
                except:
                    self.file_received.close()
                    os.remove(self.file_received.name)
                    print("Closing client connection ... ")
                    connection.close()
                    break
                        

            #ensure that the total bytes received is the same as the file the client wants to "put"
	    #if so: send a msg back to the client confirming that file has been received, update server shared dir
	    #and close the file that was written to (so that the file can be opened properly in the server folder)
            if(amount_received == self.put_file_len):
                print ("Done Receiving")
                connection.sendall(("Received file "+self.put_file_name).encode(Server.MSG_ENCODING))
                self.get_shared_directory() #update shared directory 
                self.file_received.close()
            
            return #for some reason thread would not return without this
                

    #method to handle multiple TCP client connections    
    def connection_handler(self, client):
        connection, address_port = client
        Ip_addr, port_num = address_port
        print("-" * 72)
        print("Connection received from ",end='')
        print(Ip_addr,end='')
        print(" on port ",end='')
        print(port_num)
        connection.setblocking(False) #ensure that current client's socket is set to non-blocking
        while True: #loop to process any UDP discover requests + any TCP (multiple) TCP connections
            try: #to catch anything that goes wrong in the loop at all
			
		#UDP discovery/advertisement response - ensure that client UDP discovery can still occur even if the client trying to 
		#discover the File Sharing Service while its already est a TCP connection
                try:
                    recvd_UDP_bytes, address = self.UDP_socket.recvfrom(Server.RECV_SIZE)
                    recvd_UDP_str = recvd_UDP_bytes.decode(Server.MSG_ENCODING)
                    
                    # Check if the received packet contains a service scan command
                    if Server.SERVICE_DISCOVERY_MSG == recvd_UDP_str:
                        self.UDP_socket.sendto(Server.MSG_ENCODED, address) # Send the service advertisement message back to the client.
       
                except socket.error:
                    pass            
                except KeyboardInterrupt:
                    print()
                    sys.exit(1)
                
		#try block to handle TCP connections
                try:
                    recvd_bytes = connection.recv(Server.RECV_BUFFER_SIZE)

                    if len(recvd_bytes) == 0:
                        print("Closing client connection ... ")
                        connection.close()
                        break
		    #not really needed - added as safety incase we don't get msg in utf-8 encoding (try will work ~100% of time)
                    try:
                        self.recvd_str = recvd_bytes.decode(Server.MSG_ENCODING)
                    except UnicodeDecodeError:
                        self.recv_str = ""
						
		    #handle "connect" command - send connection established back to client
                    if self.recvd_str == Server.CONNECT_CMD:
                        connection_est_str = "connection established"
                        connection_est_enc = connection_est_str.encode(Server.MSG_ENCODING)
                        connection.sendall(connection_est_enc)
                    
		    #handle "bye" command - send current connection closed back to client - then close TCP connection
                    if self.recvd_str == Server.BYE_CMD:
                        print("Closing client connection ... ")
                        connection_close_str = "current connection closed"
                        connection_close_enc = connection_close_str.encode(Server.MSG_ENCODING)
                        connection.sendall(connection_close_enc)
                        connection.close()
                        break
                    
                    #handle "get <filename>" command.. string is sent such that string is: get/<filename>.. otherwise not valid get
                    if len(self.recvd_str.split("/"))== 2:
                        #ensure that "get" command is used by client
                        if self.recvd_str.split("/")[0] == Server.GET_CMD:
                            self.string_arr_get_file = self.recvd_str.split("/") #create 2 col array ["get",<filename>]
                            
                            b = 0
                            self.get_shared_directory() #change dir to server shared dir + update dir
                            #loop through to see if the file the client wants to "get" is a valid file (in servers dir)
                            while b<self.rlist_array_size:
                                if self.string_arr_get_file[1] == self.rlist_array[b]:
                                    break #filename match, index b (in the servers list of dir files) is the same as the requested file
                                b+=1
                            #case in which the file client wants to "get" is in the servers dir
                            if b < self.rlist_array_size:
                                connection.sendall("ok".encode(Server.MSG_ENCODING)) #inform client that file is in server's dir
                                self.string_get_file_size = str(os.path.getsize(os.getcwd() + "\\" + self.string_arr_get_file[1])) #get size of "get" file
                                amount_sent =0 #counter to ensure complete size of file is sent to client
                                enc_get_file = open(self.string_arr_get_file[1],'rb') #open the requested "get" file read its bytes
                                #send the file's bytes line by line to the client - update amount sent continuously
                                for line in enc_get_file:
                                    amount_sent += len(line)
                                    print ("Amount sent: " + str(amount_sent) + " total size: " + self.string_get_file_size)
                                    connection.sendall(line)
                            
                            # close the file, the next recevied data will include whether the transfer was succesful or not
                                enc_get_file.close()
                                data = connection.recv(Client.RECV_SIZE) #client sends back that data transfer is successful
                                data_dec = data.decode(Server.MSG_ENCODING)
                                if(data_dec != ""):
                                    print(data_dec)
                                    
                            #file is not in servers shared dir - inform client
                            else:
                                print("File is not in Server's shared directory")
                                connection.sendall("File is not in Server's shared directory".encode(Server.MSG_ENCODING))
                                
                        #Invalid "get" request - inform client
                        else:
                            print("Invalid get input")
                            connection.sendall("Invalid get input".encode(Server.MSG_ENCODING))
                            
                        
                    
                    #handle "put <filename>" command .. string is sent such that string is: get/<filename>/filesize.. otherwise not valid put 
                    if len(self.recvd_str.split("/"))== 3:
                        
                        #verify "put" command is entered
                        if self.recvd_str.split("/")[0] == Server.PUT_CMD: 

                            #create new thread for a client wanting to "put" a file in the server's directory
                            new_thread2 = threading.Thread(target=self.threaded_put_file,
                                                          args=(client,))
                            
                            # Record the new thread.
                            self.put_thread_list.append(new_thread2)

                            # Start the new thread running.
                            #print("Starting serving thread: ", new_thread.name)
                            new_thread2.daemon = True
                            new_thread2.start()
                            #loop to ensure that the thread doesn't accidently exit while it is still active/alive
                            while new_thread2.is_alive():
                                continue
                            new_thread2.join() #join thread to the main thread
                            
                            
                    #handle "rlist" command
                    if self.recvd_str == Server.RLIST_CMD:
                        self.get_shared_directory()#changed to shared dir + update shared dir list
                        j = 0
                        self.rlist_str ="" #empty string to store shared dir list
                        #loop through the shared dir list, and store all dir list elements into a string
                        while j<self.rlist_array_size:
                            self.rlist_str +=self.rlist_array[j]
                            self.rlist_str +="\n"
                            j+=1
                        self.rlist_enc = self.rlist_str.encode(Server.MSG_ENCODING)
                        connection.sendall(self.rlist_enc) #send encoded string of shared dir filenames
                        continue

                except socket.error:
                    pass            
                except KeyboardInterrupt:
                    print()
                    sys.exit(1)
                    
            except socket.error: #catch any socket blocking errors that go on at all during the loop
                pass
            except KeyboardInterrupt: #catch control C interupt during the loop
                print()
                print("Closing client connection ... ")
                connection.close()
                break

########################################################################
# Echo Client class
########################################################################

class Client:

    # Set the server hostname to connect to. If the server and client
    # are running on the same machine, we can use the current
    # hostname.
    SERVER_HOSTNAME = socket.gethostname()
    
    #common client commands
    SCAN_CMD = "scan" #added for lab 3
    LLIST_CMD ="llist" #added for lab 3
    CONNECT_CMD = "connect " + socket.gethostbyname(socket.gethostname()) +" "+ str(Server.FSP_PORT) #added for lab 3 "connect 192.168.0.33 30001"
    PUT_CMD = "put"
    GET_CMD = "get"
    PUT_RESP = "ok"
    MSG_ENCODING = "utf-8"
    RLIST_CMD = "rlist" #added for lab 3
    BYE_CMD = "bye" #added for lab 3

    #common directory folders TO CHANGE EVERYTIME U CHANGE FOLDER DIRECTORY LOCATION
    READ_CLIENT_LOCAL_DIRECTORY = r"C:\Users\Alex\Desktop\Electrical engineering\4th year (round 2)\term 2\Comp Eng 4DN4\labs\3\4DN4_lab_3\Code\client_local_files"
    SERVER_SHARING_DIRECTORY = "C:\\Users\\Alex\\Desktop\\Electrical engineering\\4th year (round 2)\\term 2\\Comp Eng 4DN4\\labs\\3\\4DN4_lab_3\\Code\\server_shared_files"
    READ_SERVER_SHARING_DIRECTORY = r"C:\Users\Alex\Desktop\Electrical engineering\4th year (round 2)\term 2\Comp Eng 4DN4\labs\3\4DN4_lab_3\Code\server_shared_files"
    CLIENT_LOCAL_DIRECTORY = "C:\\Users\\Alex\\Desktop\\Electrical engineering\\4th year (round 2)\\term 2\\Comp Eng 4DN4\\labs\\3\\4DN4_lab_3\\Code\\client_local_files"

    #constants added for lab 3 - UDP port/boradcasting
    SCAN_TIMEOUT = 3
    SCAN_INTERVAL = 1
    TOTAL_SCAN_TIME = 5
    RECV_SIZE = 1024
    BROADCAST_ADDRESS = "255.255.255.255" 
    BROADCAST_PORT = 56926
    ADDRESS_PORT = (BROADCAST_ADDRESS, BROADCAST_PORT)
    RECV_BUFFER_SIZE = 1024
    SERVICE_DISCOVERY_MSG = "SERVICE DISCOVERY"
    SERVICE_DISCOVERY_ENCODED = SERVICE_DISCOVERY_MSG.encode(MSG_ENCODING)
    
    def __init__(self):
        while True: #client window does not close unless exception is raised
            
            TCP_est = 0 #added to indicate if TCP connection est (0 = not , 1 =est)
            self.get_socket() #create client UDP and TCP sockets
            while True: #continuously get client input, then process command
                self.get_console_input() #get input on what should be done (scan,connect,llist,rlist,etc) - added for lab 3

                #handle "scan" command
                if self.input_text == Client.SCAN_CMD: #if "scan" input by user broadcast scan for file sharing service
                    self.scan_for_service() #added for lab 3
                    
                #handle "llist" command    
                if self.input_text == Client.LLIST_CMD: #if local list command entered, call function to output local list dir
                    self.get_local_directory() #added for lab 3 - change to local dir, update list of filenames + size
                    self.print_local_directory() #added for lab 3 - print local dir

                #handle "connect <IP addr> <port>" command 
                if self.input_text == Client.CONNECT_CMD: #added for lab 3
                    self.string_arr_IP_addr_port_num = self.input_text.split(" ")#make a 3 col array ["connect", "192.168.0.33", "30001"]
                    self.connect_to_server() #attempt to est a TCP connection with server
                    TCP_est = 1 #indicate TCP connection est
                    self.connection_send() # tell server that client is connecting
                    self.connection_receive() # server responds to tell client that connection is est


                ########################## COMMANDS THAT REQUIRE TCP CONNECTIONS (BELOW) ###########################################

                #handle "rlist" command - if connection is established, send request to server, server responds with shared directory string
                if self.input_text == Client.RLIST_CMD and TCP_est == 1:
                    self.connection_send()
                    self.connection_receive()
                #if connection is not established, can't view shared directory list    
                if self.input_text == Client.RLIST_CMD and TCP_est == 0:
                    print("TCP connection has not been established")

                #handle "put <filename>" command - only if connection is established   
                if self.input_text.split(" ")[0] == Client.PUT_CMD and TCP_est == 1:

                    #catch cases in which you would either have just a "put" command alone or put "" 
                    if len(self.input_text.split(" "))< 2: 
                        continue
                    if self.input_text.split(" ")[1] == "": 
                        continue
                    #catch cases in which file names have spaces between characters (ensure 2 col array) 
                    if len(self.input_text.split(" "))> 2:
                        inp_size = len(self.input_text.split(" "))
                        n = 0
                        temp_arr = self.input_text.split(" ")
                        self.string_arr_put_file = []
                        while n<inp_size:
                            if n <= 1: #create 2 col array ["put", <first string in filename with spaces>]
                                self.string_arr_put_file.append(temp_arr[n])
                            else:
                                self.string_arr_put_file[1] = self.string_arr_put_file[1] + " " + temp_arr[n] 
                            n+=1

                    else:
                        if len(self.input_text.split(" ")) == 2:
                            self.string_arr_put_file = self.input_text.split(" ") #create a 2 col array ["put", <filename>]
                     
                    text_of_put_file = self.string_arr_put_file[0] + "/" + self.string_arr_put_file[1] #seperate: "put"/<filename> 
                    i = 0
                    self.get_local_directory()
                    #try to find filename in local dir
                    while i<self.llist_array_size:
                        if self.string_arr_put_file[1] == self.llist_array[i]:
                            break
                        i+=1
                    #filename client wants to "put" is in local dir
                    if i < self.llist_array_size:
                        text_of_put_file = self.string_arr_put_file[0] + "/" + self.string_arr_put_file[1]
                        self.TCP_socket.sendall((text_of_put_file + "/"+ str(os.path.getsize(os.getcwd() + "\\" + self.string_arr_put_file[1]))).encode(Server.MSG_ENCODING)) #send enc string seperated by "/", put/<filename>/filesize
                        self.connection_receive() #try to receive an "ok" from server (ok to send)
                        
                        #server indicates its ok to send
                        if self.recv_msg_fr_server == Client.PUT_RESP: #means its okay to send a file
                            self.get_local_directory()#change dir to local dir + store/update all files names in an array             
                            
                            # open the file for reading, and send each line to the server                            
                            enc_sent_file = open(self.string_arr_put_file[1],'rb')
                            for line in enc_sent_file:
                                self.TCP_socket.sendall(line)
                            
                            # close the file, the next recevied data will include whether the transfer was succesful or not
                            enc_sent_file.close()
                            data = self.TCP_socket.recv(Client.RECV_SIZE)
                            data_dec = data.decode(Server.MSG_ENCODING)
                            if(data_dec != ""):
                                print(data_dec)

                        #server indicates its not ok to send
                        else:
                            print("Server not willing to accept your file transfer request")

                    else:
                        print("File is not in local directory")
                              
                #handle case if client tries to "put" a file when TCP connection is not established     
                if self.input_text.split(" ")[0] == Client.PUT_CMD and TCP_est == 0:
                    if len(self.input_text.split(" "))< 2:
                        continue
                    if self.input_text.split(" ")[1] == "": 
                        continue
                    print("TCP connection has not been established")

                #handle "get <filename>" command - only if connection is established 
                if self.input_text.split(" ")[0] == Client.GET_CMD and TCP_est == 1:
                    
                    #catch cases in which you would either have just a "get" command alone or get "" 
                    if len(self.input_text.split(" "))< 2:
                        continue
                    if self.input_text.split(" ")[1] == "": 
                        continue
                    
                    #catch cases in which file names have spaces between characters (ensure 2 col array)
                    if len(self.input_text.split(" "))> 2:
                        get_inp_size = len(self.input_text.split(" "))
                        q = 0
                        temp_arr2 = self.input_text.split(" ")
                        self.string_arr_get_file = []
                        while q<get_inp_size:
                            if q <= 1: #create 2 col array ("get", <first string in filename with spaces>)
                                self.string_arr_get_file.append(temp_arr2[q])
                            else:
                                self.string_arr_get_file[1] = self.string_arr_get_file[1] + " " + temp_arr2[q] 
                            q+=1

                    else:
                        if len(self.input_text.split(" ")) == 2:
                            self.string_arr_get_file = self.input_text.split(" ") #create a 2 col array ["get", <filename>]
                    
                    text_of_get_file = self.string_arr_get_file[0] + "/" + self.string_arr_get_file[1]
                    self.TCP_socket.sendall((text_of_get_file.encode(Server.MSG_ENCODING))) #send string seperated by "/" "get/<filename>"
                    recvd_bytes_indic = self.TCP_socket.recv(Client.RECV_BUFFER_SIZE) #receive response back from server
                    recvd_str_indic = recvd_bytes_indic.decode(Server.MSG_ENCODING)
                    
                    if recvd_str_indic == "ok": #file is in servers shared directory - do file transfer (receive)
                        amount_get_received = 0
                        os.chdir(Client.CLIENT_LOCAL_DIRECTORY) #change dir to local dir
                        self.file_received = open(self.string_arr_get_file[1],'wb') #open a file in write mode, same name as the file u want to receive from server
                        self.server_dir = Client.SERVER_SHARING_DIRECTORY
                        self.get_file_path = self.server_dir + "\\" + self.string_arr_get_file[1] #get exact filepath of file (from shared dir)
                        self.get_file_size = os.path.getsize(self.get_file_path) #get the size (bytes) of the file being transfered

                        #loop until client received all bytes of the file from the server
                        while(amount_get_received < self.get_file_size): 
                            self.get_local_directory()#mainly to ensure we are on local dir during this loop
                            enc_get_file = self.TCP_socket.recv(Server.FILE_RECV_BUFFER)#receive a certain # of bytes each time we receive a line of the file from the server
                            if enc_get_file:   
                                # write to the file each line received
                                self.file_received.write(enc_get_file)
                                amount_get_received += len(enc_get_file)
                                print ("Amount received: " + str(amount_get_received) + " total size: " + str(self.get_file_size))
                            else:
                                self.file_received.close()
                                break
                        #handle case in which file is fully received - notify client and update local dir
                        if(amount_get_received == self.get_file_size):
                            print ("Done Receiving")
                            self.TCP_socket.sendall(("Received file "+self.string_arr_get_file[1]).encode(Server.MSG_ENCODING))
                            self.get_local_directory() #update local directory 
                            self.file_received.close()

                    #catch case in which either the input is invalid or the file is not in shared dir                
                    else:
                        if recvd_str_indic == "File is not in Server's shared directory":
                            print("File is not in Server's shared directory")
                            continue

                        if recvd_str_indic == "Invalid get input":
                            print("Invalid get input")
                            continue

                #handle case where "get" command is entered, but no TCP connection est
                if self.input_text.split(" ")[0] == Client.GET_CMD and TCP_est == 0:
                    if len(self.input_text.split(" "))< 2:
                        continue
                    if self.input_text.split(" ")[1] == "": #ur gonna want a different check to make sure file is valid for the 2nd field of array
                        continue
                    print("TCP connection has not been established")
                   
                #handle "bye" command - if connection is established, send request to server, server responds by saying the connection is closed, then closes the tcp connction
                if self.input_text == Client.BYE_CMD and TCP_est == 1:
                    TCP_est = 0 #indicate TCP connection closed
                    self.connection_send()
                    self.connection_receive()
                    break
                else:
                    #if a TCP connection is not established, there's no connection to close
                    if self.input_text == Client.BYE_CMD and TCP_est == 0: 
                        print("TCP connection has not been established") 
               
    #modified for lab 3 - added UDP sockets
    def get_socket(self):
        try:
            #create IPv4 UDP broadcast socket - added for lab 3
            self.UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.UDP_socket.settimeout(Client.SCAN_TIMEOUT);

            # Create an IPv4 TCP socket.
            self.TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as msg:
            print(msg)
            sys.exit(1)

    #added method for lab 3 - send UDP broadcast looking for UDP/SDP port (fixed time scan)
    def scan_for_service(self):
        # Scan for Client.TOTAL_SCAN_TIME. First record the start time
        start_time = datetime.datetime.now()

        # Collect our scan results in a list.
        scan_results = []

        while True:
            # If we have scanned long enough, quit and print out our results
            current_time = datetime.datetime.now()
            if (current_time-start_time).seconds >= Client.TOTAL_SCAN_TIME:
                for result in scan_results:
                    name_of_file_sharing_service,address_and_port = result
                    IP_addr,SDP_port_num = address_and_port
                    #printout file sharing service + addr + port
                    print("The Server's SDP at IP addr/port ", end='')
                    print(IP_addr, end='')
                    print("/", end='')
                    print(SDP_port_num, end='')
                    print(" responded stating that the file sharing service: ")
                    print(name_of_file_sharing_service, end='')
                    print(" is found at IP address/port ", end='')
                    print(IP_addr , end='')
                    print("," , end='')
                    print(Server.FSP_PORT)
                return
            
            # Send a scan broadcast message
            print("Service Discovery scan in progress...")
            self.UDP_socket.sendto(Client.SERVICE_DISCOVERY_ENCODED, Client.ADDRESS_PORT) #modified for lab 3

            try:
                # Listen for a response from a server. We will keep
                # doing this until we have scanned for our total scan
                # time. A socket timeout allows us to recover if there
                # are no servers.
                recvd_bytes, address = self.UDP_socket.recvfrom(Client.RECV_SIZE)
                recvd_msg = recvd_bytes.decode('utf-8')

                # Collect only unique servers.
                if (recvd_msg, address) not in scan_results:
                    scan_results.append((recvd_msg, address))

                # Wait for Client.SCAN_INTERVAL seconds before
                # starting the next scan.
                time.sleep(Client.SCAN_INTERVAL)
            except socket.timeout:
                print("No service found")
                continue

            
    #added for lab 3 - function to find LOCAL files + print them
    def get_local_directory(self):
        os.chdir(Client.READ_CLIENT_LOCAL_DIRECTORY) #change directory name when moving from desktop to laptop
        self.llist_array = os.listdir() #store remote list in an array
        self.llist_array_size = len(self.llist_array) #find array size of remote files

    #added for lab 3 - print shared directory (server)
    def print_local_directory(self):
        print("local file sharing directory: ")
        i = 0
        #loop through the array and print all files available for sharing 
        while i<self.llist_array_size:
            print(self.llist_array[i])
            i+=1
    
    #modified for lab 3
    def connect_to_server(self):
        try:
            # Connect to the server using its socket address tuple.
            self.TCP_socket.connect((self.string_arr_IP_addr_port_num[1], int(self.string_arr_IP_addr_port_num[2]))) #self.TCP_socket.connect((Client.SERVER_HOSTNAME, Server.FSP_PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    #modified for lab 3
    def get_console_input(self):
        # In this version we keep prompting the user until a non-blank
        # line is entered.
        while True:
            self.input_text = input("Enter 1 of the following commands: 1)scan , 2)connect <IP address> <port>, 3)llist, 4)rlist,\n5)put <filename>, 6)get <filename>, 7)bye: ")
            if self.input_text != "":
                break
     
    def connection_send(self):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
            self.TCP_socket.sendall(self.input_text.encode(Server.MSG_ENCODING))
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
            self.recv_msg_fr_server = recvd_bytes.decode(Server.MSG_ENCODING)#added for lab 3

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






