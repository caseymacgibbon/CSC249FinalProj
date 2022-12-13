# Kaia Cormier, Sabrina Hatch, Casey MacGibbon
# Pair programmed Proj 1 Phase 1-3 :D
# 9/29/2022
# 
# helpful resources: 
# http headers for dummies:   
# https://code.tutsplus.com/tutorials/http-headers-for-dummies--net-8039 
# socket documentation: 
# https://docs.python.org/3/library/socket.html

from socket import *
import sys # In order to terminate the program
import time
import threading
from concurrent.futures import ThreadPoolExecutor



# socket.recv(bufsize[, flags]) Receive data from the socket. The return value is a bytes object representing the data received. The maximum amount of data to be received at once is specified by bufsize. Bufszie 1024 - relatively small power of 2. (docs.python.org) 
      # decode converts from byte object to string
def one_thread(connectionSocket):
    try:
        message = connectionSocket.recv(1024)
        print(message)
        # -----------
        # Fill in end
        # -----------
        
        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]

        # Because the extracted path of the HTTP request includes 
            # a character '\', we read the path from the second character
        f = open(filename[1:])
    
        # -------------
        # Fill in start
        # -------------
        outputdata = f.read()
        # TODO: Store the entire contents of the requested file in a temporary buffer
        
        # -----------
        # Fill in end
        # -----------

        # ------------
        # Fill in start
        # -------------
        # TODO: Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
        # -----------
        # Fill in end
        # -----------

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        print("Connection to client close")
        connectionSocket.close()
    except IOError:
        # -------------
        # Fill in start
        # -------------
        # TODO: Send response message for file not found
        #       Close client socket
        #\r\n is new line for text formats on the internet
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        # create output data for the error message 
        outputdata = "404 not found <3"
        # Send the content of the error message to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

def main(): 
    serverSocket = socket(AF_INET, SOCK_STREAM)
      # TODO: Assign a port number 8081
    socketPort = 2002
      #       Bind the socket to server IP address and server port (IP address is server's current IP address)
    server = "0.0.0.0"
      # Print so we can see the IP address to enter the link into browser
    print(server)
    serverSocket.bind((server, socketPort))
      #       Tell the socket to listen to at most 1 connection at a time with listen func and param 1
    serverSocket.listen(10)
    print("the web server is up on port:", socketPort)
    executor = ThreadPoolExecutor()

    while True:
        
        # Establish the connection
        print('Ready to serve...') 
        
      # TODO: Set up a new connection from the client
      # The socket must be bound to an address and listening for connections. The return value is a pair (conn, address) where conn is a new socket object usable to send and receive data on the connection, and address is the address bound to the socket on the other end of the connection. (docs.python.org)
        connectionSocket, addr = serverSocket.accept()
        numReq = numReq + 1
        reset_time = time.time()
        max =3
        
        if((time.time() - reset_time) > 1):
            reset_time = time.time()
            numReq = 1
        if numReq < max:
            executor.submit(process_request, connectionSocket, addr)
        else:
            pass 
            
        
        print("Accepting from", addr)
        executor.submit(one_thread, connectionSocket)
        # TODO: Receive the request message from the client

    serverSocket.close()
    sys.exit()  #Terminate the program after sending the corresponding data

if __name__=="__main__":
    main()
