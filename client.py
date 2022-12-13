# Kaia Cormier and Sabrina Hatch
# Pair programmed Proj 1 :D
# 9/29/2022
#
# helpful resources:
# http headers for dummies:
#
from socket import *
import sys # In order to terminate the program
import time
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def one_thread():
    clientSocket = socket(AF_INET,SOCK_STREAM)
    #make socket and address dynamic later
    #connect the socket to the server
    host = sys.argv[1]
    port = int(sys.argv[2])
    clientSocket.connect((host, int(port)))
    clientSocket.sendall(f'GET /{sys.argv[3]} HTTP/1.1\r\n\r\n'.encode())
#    message = clientSocket.recv(1024)
#    while message:
#        print(message.decode(), end="")
#        message = clientSocket.recv(1024)

    clientSocket.close()
def main():
    executor = ProcessPoolExecutor()
    for i in range(1000):
        executor.submit(one_thread)

main()
