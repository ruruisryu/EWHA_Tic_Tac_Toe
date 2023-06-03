'''
  ETTTP_Sever_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept()
        
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        # Send start move information to peer
        if start == 0:
            start_player = "ME"
        else:
            start_player = "YOU"
        # First Player에 대한 SEND 메세지 만들어 전송
        msg=f"SEND ETTTP/1.0\r\nHost:{MY_IP}\r\nFirst-Move:{start_player}\r\n\r\n"
        client_socket.send(str(msg).encode())
    
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        ack = client_socket.recv(SIZE).decode()
        # ACK가 유효하지 않다면 Quit
        ack_info = check_msg(ack, MY_IP)
        if ack_info == False:
            client_socket.close()
            TTT.quit()
        
        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()
