from socket import *
import sys # In order to terminate the program
import requests
from concurrent.futures import ThreadPoolExecutor

import time


#print(socket.gethostbyname(socket.gethostname()))

def process_request(connectionSocket, addr):
    try:

        # -------------
        # Fill in start
        # -------------
        message = connectionSocket.recv(1024)  # TODO: Receive the request message from the client
        print(str(message))
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
        # print("filename = ", filename)
        outputdata = f.read()  # TODO: Store the entire contents of the requested file in a temporary buffer
        # print("output Data", outputdata)
        # -----------
        # Fill in end
        # -----------
        #time.sleep(10)
        # -------------
        # Fill in start
        # -------------
        # TODO: Send one HTTP header line into socket
        http_header = "HTTP/1.1 200 OK\r\n\r\n"
        connectionSocket.send(http_header.encode())

        # -----------
        # Fill in end
        # -----------

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            # print("in the for loop")
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        #print("Connect finish")
        connectionSocket.close()

    except IOError:
        # -------------
        # Fill in start
        # -------------
        # TODO: Send response message for file not found
        #       Close client socket

        connectionSocket.send('HTTP/1.0 404 Error\n\n'.encode())
        connectionSocket.send("""<html> <head> <h1>Error 404: File not found</h1> </head> </html>""".encode())
        connectionSocket.close()

def main():

    serverSocket = socket(AF_INET, SOCK_STREAM)

    # -------------
    # Fill in start
    # -------------

      # TODO: Assign a port number
      #       Bind the socket to server address and server port http://127.0.0.1:8080/HelloWorld.html
      #       Tell the socket to listen to at most 1 connection at a time
    #print(serverSocket.gethostname())
    #print(serverSocket.getsockname())

    #TA via Diana:  that 8080 was the http port so I am using this
    #TA via Diana: you need to get your IPv4 address for the address by using gethostbyname(gethostname())
    serverSocket.bind(('0.0.0.0', 8081))
    serverSocket.listen()
    request_num = 0
    reset_time = time.time()
    max = 3
    # threads = []

    # -----------
    # Fill in end
    # -----------
    executor = ThreadPoolExecutor(max_workers=2)
    while True:

        # Establish the connection
        print('Ready to serve...')

        # -------------
        # Fill in start
        # -------------
        connectionSocket, addr = serverSocket.accept() # TODO: Set up a new connection from the client
        #print("accept connection from", addr)
        request_num = request_num+1

        if((time.time() - reset_time) > 1):
            reset_time = time.time()
            request_num = 1

        if request_num <= max:
            print(f"Accepting {addr}")
            executor.submit(process_request, connectionSocket, addr)
        else:
            print(f"Throwing out req {addr}")
            connectionSocket.close()


        # check last reset time
        # if reset time was > 1 second ago
        #   reset last_reset_time
        #   reset req_num 1
        # if req_num < max:
            # execute
        # else
            # throw away

        #print("done submit")

        # -----------
        # Fill in end
        # -----------


    serverSocket.close()
    sys.exit()  #Terminate the program after sending the corresponding data

if __name__ == '__main__':
    main()




