'''
  ETTTP_Client_skeleton.py
 
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

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        
        ###################################################################
        # Receive who will start first from the server
        msg = client_socket.recv(SIZE).decode()

        # 메세지를 체크해서 유효하지 않다면 QUit
        msg_info = check_msg(msg, MY_IP)
        if msg_info == False:
            client_socket.close()
            TTT.quit()

        # start_player 설정
        if msg_info[1] == 'YOU':
            start_player = msg_info[1]
            start = 1
        else:
            start_player = msg_info[1]
            start = 0

        ######################### Fill Out ################################
        # Send ACK 
        ack = f"ACK ETTTP/1.0\r\nHost:{MY_IP}\r\nFirst-Move:{start_player}\r\n\r\n"
        client_socket.send(str(ack).encode())
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        
