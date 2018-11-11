
"""
Echo Client and Server Classes

T. D. Todd
McMaster University

to create a Client: "python EchoClientServer.py -r client" 
to create a Server: "python EchoClientServer.py -r server" 

or you can import the module into another file, e.g., 
import EchoClientServers

"""

########################################################################

import socket
import csv
import argparse
import sys
import getpass
import hashlib

########################################################################
# Echo Server class
########################################################################

class Server:

    # Set the server hostname used to define the server socket address
    # binding. Note that 0.0.0.0 or "" serves as INADDR_ANY. i.e.,
    # bind to all local network interface addresses.
    HOSTNAME = "0.0.0.0"

    # Set the server port to bind the listen socket to.
    PORT = 50000

    RECV_BUFFER_SIZE = 1024
    MAX_CONNECTION_BACKLOG = 10
    GET_AVERAGES_CMD = "GETA"
    MSG_ENCODING = "utf-8"

    # Create server socket address. It is a tuple containing
    # address/hostname and port.
    SOCKET_ADDRESS = (HOSTNAME, PORT)

    def __init__(self):
        self.get_csv_file() #added for lab 2
        self.create_listen_socket()
        self.process_connections_forever()

    def get_csv_file(self): #added func to print csv file contents + return csv file + row size.. added for lab 2
        with open('course_grades_2018.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")

            self.csv_array_row_size = 0	
            a = []
            print("Data read from CSV file: ")
            for row in reader:
                a.append (row)
                print(row)
                self.csv_array_row_size += 1
            self.CSV_ARRAY = list(a)
            self.csv_array_col_size = len(self.CSV_ARRAY[0])


    def create_listen_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set socket layer socket options. This allows us to reuse
            # the socket without waiting for any timeouts.
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind socket to socket address, i.e., IP address and port.
            self.socket.bind(Server.SOCKET_ADDRESS)

            # Set socket to listen state.
            self.socket.listen(Server.MAX_CONNECTION_BACKLOG)
            print("Listening on port {} ...".format(Server.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_connections_forever(self):
        try:
            while True:
                # Block while waiting for accepting incoming
                # connections. When one is accepted, pass the new
                # (cloned) socket reference to the connection handler
                # function.
                self.connection_handler(self.socket.accept())
        except Exception as msg:
            print(msg)
        except KeyboardInterrupt:
            print()
        finally:
            self.socket.close()
            sys.exit(1)

    def connection_handler(self, client): #modified for lab 2
        connection, address_port = client
        print("-" * 72)
        print("Connection received from {}.".format(address_port))

        while True:
            try:
                # Receive bytes over the TCP connection. This will block
                # until "at least 1 byte or more" is available.
                recvd_bytes = connection.recv(Server.RECV_BUFFER_SIZE)
            
                # If recv returns with zero bytes, the other end of the
                # TCP connection has closed (The other end is probably in
                # FIN WAIT 2 and we are in CLOSE WAIT.). If so, close the
                # server end of the connection and get the next client
                # connection.
                if len(recvd_bytes) == 0:
                    print("Closing client connection ... ")
                    connection.close()
                    break

                    
                # Decode the received bytes back into strings. Then output
                # them.
                
                #added if block for lab #2 (the case in which GAC is received)... need to compare to encoded GAC
                #since we cant decode all received bytes in UTF-8 (may be encoded in SHA256)

                #added for lab 2 (if else block) - check if encoding is UTF-8 or SHA256 (GAC or student record)
                
                if recvd_bytes == Server.GET_AVERAGES_CMD.encode(Server.MSG_ENCODING):
                    print("Received GAC from client.")
                    avg_reply = self.CSV_ARRAY[0][4] + " " + self.CSV_ARRAY[12][0] + " = " + self.CSV_ARRAY[12][4] + "\n" + self.CSV_ARRAY[0][5] + " " + self.CSV_ARRAY[12][0] + " = " + self.CSV_ARRAY[12][5] + "\n"   
                    avg_reply = avg_reply + self.CSV_ARRAY[0][6] + " " + self.CSV_ARRAY[12][0] + " = " + self.CSV_ARRAY[12][6] + "\n" + self.CSV_ARRAY[0][7] + " " + self.CSV_ARRAY[12][0] + " = " + self.CSV_ARRAY[12][7] + "\n"
                    avg_reply = avg_reply + self.CSV_ARRAY[0][8] + " " + self.CSV_ARRAY[12][0] + " = " + self.CSV_ARRAY[12][8]
                    avg_reply_enc = avg_reply.encode(Server.MSG_ENCODING)
                    connection.sendall(avg_reply_enc)
                else:
                    print("Received IP/password hash ",end='')
                    print(recvd_bytes,end='')
                    print(" from client.")


                    
                    i=1
                    #create a loop to continuously create a new hash object (of the desired student # and password)
                    #to compare with what student # and password the client sent over
                    while i<11:
                        self.hashed_object = hashlib.sha256() #create hash object
                        self.hashed_object.update(self.CSV_ARRAY[i][0].encode(Server.MSG_ENCODING))
                        self.hashed_object.update(self.CSV_ARRAY[i][1].encode(Server.MSG_ENCODING))
                        self.hashed_ID_and_PW_compare = self.hashed_object.digest()
                        if self.hashed_ID_and_PW_compare == recvd_bytes:
                            break
                        i+=1
                    #if else block added to determine if student ID/PW in CSV file
                    if i<11:
                        print("Correct password, record found.")
                        grades_reply = self.CSV_ARRAY[0][3] + "= " + self.CSV_ARRAY[i][3] + ", " #get first name
                        grades_reply = grades_reply+ self.CSV_ARRAY[0][2] + "= " + self.CSV_ARRAY[i][2] + ":\n" #get last name
                        grades_reply = grades_reply+ self.CSV_ARRAY[0][4] + "= " + self.CSV_ARRAY[i][4] + "\n" #get midterm mark
                        grades_reply = grades_reply+ self.CSV_ARRAY[0][5] + "= " + self.CSV_ARRAY[i][5] + "\n" #get lab 1 mark
                        grades_reply = grades_reply+ self.CSV_ARRAY[0][6] + "= " + self.CSV_ARRAY[i][6] + "\n" #get lab 2 mark
                        grades_reply = grades_reply+ self.CSV_ARRAY[0][7] + "= " + self.CSV_ARRAY[i][7] + "\n" #get lab 3 mark
                        grades_reply = grades_reply+ self.CSV_ARRAY[0][8] + "= " + self.CSV_ARRAY[i][8] + "\n" #get lab 4 mark
                        connection.sendall(grades_reply.encode(Server.MSG_ENCODING))

                        
                    else:
                        print("Password failure.")
                        failure_message = "Incorrect student ID or password." 
                        connection.sendall(failure_message.encode(Server.MSG_ENCODING))


            except KeyboardInterrupt:
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
    RECV_BUFFER_SIZE = 1024
    GET_AVERAGES_CMD = "GETA"
    
    def __init__(self):
        while True: #added while block so that this continues without restarting client or server- lab2
            try:
                self.get_socket()
                self.get_client_command() #added for lab 2 to get command from client
                #if else block added to distinguish between GAC and non-GAC actions
                if self.input_command == Client.GET_AVERAGES_CMD: #added for lab 2 - IF GAC command is used
                    print("Fetching grade averages:")
                    self.connect_to_server() #create a TCP connection with the server
                    self.connection_send_GAC()
                    self.connection_receive_grade_avgs()
                else: #added for lab 2 IF GAC command NOT used .. request for student ID + password
                    while True:
                        self.student_id = input("Please enter your student ID: ")
                        if self.student_id != "":
                            break
                    while True:
                        self.password = getpass.getpass(prompt = 'Please enter your password: ')
                        if self.password != "":
                            break
                    print("ID number " + self.student_id + " and password " + self.password + " received.")
                    self.student_id_enc = self.student_id.encode(Server.MSG_ENCODING) #encode student ID in UTF-8 (bytes)
                    self.password_enc = self.password.encode(Server.MSG_ENCODING) #encode password in UTF-8 (bytes)
                    self.hashed_object = hashlib.sha256() #create hash object
                    self.hashed_object.update(self.student_id_enc)
                    self.hashed_object.update(self.password_enc)
                    self.hashed_ID_and_PW = self.hashed_object.digest()
                    self.connect_to_server() #create a TCP connection with the server
                    self.connection_send_HASH()
                    self.connection_receive()
                    
                    
            except(KeyboardInterrupt, EOFError):
                print()
                print("Closing server connection ...")
                self.socket.close()
                sys.exit(1)
                
                


            
    def get_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as msg:
            print(msg)
            sys.exit(1)
            
    def get_client_command(self): #added for lab 2
        while True:
            self.input_command = input("Please enter a command: ")
            if self.input_command != "":
                break
        print("Command entered: " + self.input_command)
        

        
    def connect_to_server(self):
        try:
            # Connect to the server using its socket address tuple.
            self.socket.connect((Client.SERVER_HOSTNAME, Server.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)
            
    #added send hashed ID + PW for lab #2
    def connection_send_HASH(self):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
            print("ID/password hash ",end='') #ensure no newline after print
            print(self.hashed_ID_and_PW,end='')
            print(" sent to server.")
            self.socket.sendall(self.hashed_ID_and_PW) #Encode GETA string (UTF-8)
        except Exception as msg:
            print(msg)
            sys.exit(1)
            
    #added send GAC function for lab #2
    def connection_send_GAC(self):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
        
            self.socket.sendall(self.input_command.encode(Server.MSG_ENCODING)) #Encode GETA string (UTF-8)
        except Exception as msg:
            print(msg)
            sys.exit(1)
                
    def connection_receive_grade_avgs(self): #added for lab 2
        try:
            # Receive and print out text. The received bytes objects
            # must be decoded into string objects.
            recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)

            # recv will block if nothing is available. If we receive
            # zero bytes, the connection has been closed from the
            # other end. In that case, close the connection on this
            # end and exit.
            if len(recvd_bytes) == 0:
                print("Closing server connection ... ")
                self.socket.close()
                sys.exit(1)

            print(recvd_bytes.decode(Server.MSG_ENCODING))

        except Exception as msg:
            print(msg)
            sys.exit(1)


    def connection_receive(self):
        try:
            # Receive and print out text. The received bytes objects
            # must be decoded into string objects.
            recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)

            # recv will block if nothing is available. If we receive
            # zero bytes, the connection has been closed from the
            # other end. In that case, close the connection on this
            # end and exit.
            if len(recvd_bytes) == 0:
                print("Closing server connection ... ")
                self.socket.close()
                sys.exit(1)

            print("Received: ")
            print(recvd_bytes.decode(Server.MSG_ENCODING))

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






