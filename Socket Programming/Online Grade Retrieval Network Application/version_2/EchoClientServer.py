
"""
By Alex Szebrag

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

#--------------------------------------------------------------------------------------------------------#
                #ADDED FUNCTION FOR LAB 2 - SERVER PRINT CSV FILE, STORE IN ARRAY, FIND ROWSIZE + COLSIZE
#--------------------------------------------------------------------------------------------------------#
        
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


#--------------------------------------------------------------------------------------------------------#
                #MODIFIED FOR LAB 2 - FUNCTION NOW - a) finds index of major fields
                # b)determines if GAC or student ID/PW was received
                # c)sends either avgs or student records back to client
#--------------------------------------------------------------------------------------------------------#
            
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

    def connection_handler(self, client):
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
                #-----------------------------------------------------------------------------------------------#

                #loop through to find common indexies (assume we know what strings in row 0
                #(i.e.:"ID Number") to look for
                #assume that students/student marks immediately follow the row of headers (i.e.: Midterm)
                #assume that when a ""(empty string) is reached there are no more student entries
                #assume that when a ""(empty string) is reached, the row immediately after is the "average row"
                #assume that header strings are all on the same row

                #--------------------------------------------------------------------------------------------------------#
                ## Expected parameter provided the current CSV file:
                #--------------------------------------------------------------------------------------------------------#
                #given the file: self.header_row_index  = 0, self.stundet_row_lower_index = 1, self.stundet_row_upper_index = 10
                #given the file(header columns): self.ID_num_index = 0 , self.PW_index = 1, self.Last_Name_index = 2
                #given the file(header columns): self.First_Name_index = 3 , self.Midterm_index = 4, self.lab_1_index = 5
                #given the file(header columns): self.lab_2_index = 6 , self.lab_3_index = 7, self.lab_4_index = 8
                #given the file: self.avg_row = 12, self.avg_col = 0
               
                
                j = 0
                k = 0
                self.stundet_row_lower_index = 0
                while j< self.csv_array_row_size:
                    while k<self.csv_array_col_size:
                        if self.CSV_ARRAY[j][k] == "ID Number":
                            self.ID_num_index = k #all ID nums stored on kth column
                            self.stundet_row_lower_index +=1 #we assume that students immediately follow the row with the string headers (i.e.: password)
                            self.header_row_index = j #find row index of headers (midterm, lab, etc)
                        if self.CSV_ARRAY[j][k] == "Password":
                            self.PW_index = k #all Passwords stored on kth column
                        if self.CSV_ARRAY[j][k] == "Last Name":
                            self.Last_Name_index = k #all Last Names stored on kth column
                        if self.CSV_ARRAY[j][k] == "First Name":
                            self.First_Name_index = k #all First Names stored on kth column
                        if self.CSV_ARRAY[j][k] == "Midterm":
                            self.Midterm_index = k #all Midterms stored on kth column
                        if self.CSV_ARRAY[j][k] == "Lab 1":
                            self.lab_1_index = k #all lab 1s stored on kth column
                        if self.CSV_ARRAY[j][k] == "Lab 2":
                            self.lab_2_index = k #all lab 2s stored on kth column
                        if self.CSV_ARRAY[j][k] == "Lab 3":
                            self.lab_3_index = k #all lab 3s stored on kth column
                        if self.CSV_ARRAY[j][k] == "Lab 4":
                            self.lab_4_index = k #all lab 4s stored on kth column
                        if self.CSV_ARRAY[j][k] == "":
                            self.stundet_row_upper_index = j-1 #upper row index of students (student rows are between self.stundet_row_lower_index and self.stundet_row_upper_index)  
                            self.avg_row = j+1
                            break #skip row of empty strings
                        if self.CSV_ARRAY[j][k] == "Averages":
                            self.avg_col = k
                            j = self.csv_array_row_size #ensure we leave both loops right away
                            break
                            
                        k+=1

                    j+=1
                    k = 0

                #------------------------------------------------------------------------------------------------#

                    
                # Decode the received bytes back into strings. Then output
                # them.
                
                #added if block for lab #2 (the case in which GAC is received)... need to compare to encoded GAC
                #since we cant decode all received bytes in UTF-8 (may be encoded in SHA256)
                
                if recvd_bytes == Server.GET_AVERAGES_CMD.encode(Server.MSG_ENCODING):
                    print("Received GAC from client.")
                    avg_reply = self.CSV_ARRAY[self.header_row_index][self.Midterm_index] + " " + self.CSV_ARRAY[self.avg_row][self.avg_col] + " = " + self.CSV_ARRAY[self.avg_row][self.Midterm_index] + "\n" #midterm avgs
                    avg_reply = avg_reply + self.CSV_ARRAY[self.header_row_index][self.lab_1_index] + " " + self.CSV_ARRAY[self.avg_row][self.avg_col] + " = " + self.CSV_ARRAY[self.avg_row][self.lab_1_index] + "\n" #lab 1 avgs  
                    avg_reply = avg_reply + self.CSV_ARRAY[self.header_row_index][self.lab_2_index] + " " + self.CSV_ARRAY[self.avg_row][self.avg_col] + " = " + self.CSV_ARRAY[self.avg_row][self.lab_2_index] + "\n" #lab 2 avgs
                    avg_reply = avg_reply + self.CSV_ARRAY[self.header_row_index][self.lab_3_index] + " " + self.CSV_ARRAY[self.avg_row][self.avg_col] + " = " + self.CSV_ARRAY[self.avg_row][self.lab_3_index] + "\n" #lab 3 avgs
                    avg_reply = avg_reply + self.CSV_ARRAY[self.header_row_index][self.lab_4_index] + " " + self.CSV_ARRAY[self.avg_row][self.avg_col] + " = " + self.CSV_ARRAY[self.avg_row][self.lab_4_index] #lab 4 avgs
                    avg_reply_enc = avg_reply.encode(Server.MSG_ENCODING)
                    connection.sendall(avg_reply_enc)
                else:
                    print("Received IP/password hash ",end='')
                    print(recvd_bytes,end='')
                    print(" from client.")


                    
                    i=self.stundet_row_lower_index
                    #create a loop to continuously create a new hash object (of the desired student # and password)
                    #to compare with what student # and password the client sent over
                    while i<=self.stundet_row_upper_index:
                        self.hashed_object = hashlib.sha256() #create hash object
                        self.hashed_object.update(self.CSV_ARRAY[i][self.ID_num_index].encode(Server.MSG_ENCODING)) #hash student ID number (to compare with client)
                        self.hashed_object.update(self.CSV_ARRAY[i][self.PW_index].encode(Server.MSG_ENCODING)) #hash password (to compare with client)
                        self.hashed_ID_and_PW_compare = self.hashed_object.digest() #hash both ID and PW to compare with clients hashed sent bytes
                        if self.hashed_ID_and_PW_compare == recvd_bytes:
                            break #we found the index value, i corresponding to the matched student (i.e.: both hashed bytes match)
                        i+=1

                    if i<=self.stundet_row_upper_index:
                        print("Correct password, record found.")
                        grades_reply = self.CSV_ARRAY[self.header_row_index][self.First_Name_index] + "= " + self.CSV_ARRAY[i][self.First_Name_index] + ", " #get first name
                        grades_reply = grades_reply+ self.CSV_ARRAY[self.header_row_index][self.Last_Name_index] + "= " + self.CSV_ARRAY[i][self.Last_Name_index] + ":\n" #get last name
                        grades_reply = grades_reply+ self.CSV_ARRAY[self.header_row_index][self.Midterm_index] + "= " + self.CSV_ARRAY[i][self.Midterm_index] + "\n" #get midterm mark
                        grades_reply = grades_reply+ self.CSV_ARRAY[self.header_row_index][self.lab_1_index] + "= " + self.CSV_ARRAY[i][self.lab_1_index] + "\n" #get lab 1 mark
                        grades_reply = grades_reply+ self.CSV_ARRAY[self.header_row_index][self.lab_2_index] + "= " + self.CSV_ARRAY[i][self.lab_2_index] + "\n" #get lab 2 mark
                        grades_reply = grades_reply+ self.CSV_ARRAY[self.header_row_index][self.lab_3_index] + "= " + self.CSV_ARRAY[i][self.lab_3_index] + "\n" #get lab 3 mark
                        grades_reply = grades_reply+ self.CSV_ARRAY[self.header_row_index][self.lab_4_index] + "= " + self.CSV_ARRAY[i][self.lab_4_index] + "\n" #get lab 4 mark
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

#--------------------------------------------------------------------------------------------------------#
                #MODIFIED FOR LAB 2 - FUNCTION NOW - a) request a command from client
                # b)IF GAC used, receive and display avgs
                # c)IF non-GAC, request for ID and password, print, then SHA256 encode
                # + print encoded hash, then connect to server and send HASHED value over
                # + receive then display either error msg or student record
#--------------------------------------------------------------------------------------------------------#
    
    def __init__(self): 
        while True:
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
            
    def get_client_command(self): #added for lab 2 (get GAC or non-GAC)
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

    #modified version of send (for has values only) - non-GAC case - lab 2
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
            
    #added send GAC function for lab #2 - modified version of provided send function
    def connection_send_GAC(self):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
        
            self.socket.sendall(self.input_command.encode(Server.MSG_ENCODING)) #Encode GETA string (UTF-8)
        except Exception as msg:
            print(msg)
            sys.exit(1)
                  
    def connection_receive_grade_avgs(self): #added for lab 2 - slightly modified receieve function for GAC 
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


    def connection_receive(self): #not modified (used to receive student records - lab 2)
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






