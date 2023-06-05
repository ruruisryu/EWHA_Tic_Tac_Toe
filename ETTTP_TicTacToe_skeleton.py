'''
  ETTTP_TicTacToe_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from PIL import ImageTk
from socket import *
import _thread
import re

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME", 'img':'Ryu'}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU", 'img':'Kim'}
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME", 'img':'Kim'}
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU", 'img':'Ryu'}
        ##################################################


        self.Ryu_img = ImageTk.PhotoImage(file=r'Ryu.jpg')
        self.Kim_img = ImageTk.PhotoImage(file=r'Kim.jpg')
        self.board_bg = 'white'
        self.board_img = ImageTk.PhotoImage(file='white.png')
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].image = self.board_img
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################

        # 소켓으로 상대방이 둔 위치 메세지를 받아온다.
        msg = self.socket.recv(SIZE).decode()
        #SEND format으로 잘 구성되었는지 check
        msg_info = check_send_format(msg, self.recv_ip)

        # msg_info가 false라면 msg가 올바른 구성이 아니므로 quit
        if msg_info == False:
            self.socket.close()
            self.quit()
            return
        # msg가 유효하다면 msg_info는 ['SEND',row, col]
        else:
            # ACK 보내기
            ack = self.create_ack(msg);
            self.socket.send(str(ack).encode("utf-8"))

            # 표시할 좌표 계산
            loc = int(msg_info[1])*3 + int(msg_info[2])
        ######################################################
            
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                
    # 입력창으로 디버그 메시지 보내기
    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:               # 사용자의 턴이 아닌데 디버그 메시지를 보냈다면
            self.t_debug.delete(1.0,"end") # 입력창 지우기
            return                         # 함수 종료
        
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")    # 입력창에서 메시지 가져오기
        d_msg = d_msg.replace("\\r\\n","\r\n") # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        이미 차지된 자리인지 확인하기
        '''
        split_msg = d_msg.split("\r\n") # 메세지를 적절하게 분할
        if split_msg[2].find("New-Move:") != -1: # New-Move:를 제거하고 좌표 값의 숫자만 남김
            split_msg[2] = split_msg[2].replace("New-Move:", "")
            msg_info = re.findall(r'\d+', split_msg[2])

        loc = int(msg_info[0]) * 3 + int(msg_info[1]) # 보드에서 자리 확인 
        
        if self.board[loc] != 0:
            return
        
        self.socket.send(str(d_msg).encode()) # 디버그 메시지 인코딩하여 소켓에 전송
        
        ack = self.socket.recv(SIZE).decode() # 소켓에서 ACK 메시지 받기
        valid = check_ack_format(ack, self.recv_ip)    # ACK 메시지가 형식에 맞는지 확인
        if not valid:   # 유효하지 않으면
            self.quit() # 게임 종료

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc) # 보드 정보 업데이트
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    # 화면의 버튼을 누르면 선택지를 전송하는 함수
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3) # selection을 3으로 나눈 몫과 나머지
        ###################  Fill Out  #######################

        # send message and check ACK
        send = self.create_send(row, col)    # row, col에 따라 SEND 메시지 생성
        self.socket.send(str(send).encode()) # 메시지 인코딩하여 소켓에 전송
        
        # ACK 확인
        ack = self.socket.recv(SIZE).decode() # 소켓에서 ACK 메시지 받기
        return check_ack_format(ack, self.recv_ip)     # ACK 메시지가 형식에 맞는지 여부 반환
        ######################################################          
    
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        # if get == False: 위너, result 주는 게 먼저, 이후 받음
        if not get:
            # winner = ME
            # result message 만들어서 보냄
            result_send = self.create_result(winner)
            self.socket.send(str(result_send).encode())

            # 상대방이 보내는 result message 받아서
            result_receive = self.socket.recv(SIZE).decode()

            # 유효한지 확인한 후
            result_receive_info = check_result_format(result_receive, self.recv_ip)
            if result_receive_info == False:
                return False
            # result가 같은지 확인해서 결과 반환
            elif result_receive_info[1] == 'YOU':
                return True
            else:
                return False
        else:
            # winner = YOU
            # 상대방이 보내는 result message 받아서
            result_receive = self.socket.recv(SIZE).decode()
            # 유효한지 확인한 후
            result_receive_info = check_result_format(result_receive, self.recv_ip)
            if result_receive_info == False:
                return False

            # 나의 result 만들어서 send
            result_send = self.create_result(winner)
            self.socket.send(str(result_send).encode())

            # result가 같은지 확인해서 결과 반환
            if result_receive_info[1] == 'ME':
                return True
            else:
                return False
        ######################################################           
        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        if player['img'] == 'Ryu':
            self.cell[move].configure(image=self.Ryu_img)
        else:
            self.cell[move].configure(image=self.Kim_img)
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    # SEND 메시지 작성하기
    def create_send(self, row, col):
        send = f"SEND ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row}, {col})\r\n\r\n"
        return send

    # ACK 메시지 작성하기
    def create_ack(self, msg):
        split_string = msg.split("\r\n")  # 문자열을 개행 문자("\r\n")를 기준으로 분할
        received = split_string[2] # 받은 내용
        ack = f"ACK ETTTP/1.0\r\nHost:{self.send_ip}\r\n{received}\r\n\r\n"
        return ack

    # RESULT 메시지 작성하기
    def create_result(self, winner):
        result = f"RESULT ETTTP/1.0\r\nHost:{self.send_ip}\r\nWinner:{winner}\r\n\r\n"
        return result
# End of Root class

# send message가 유효한 메세지인지 check
def check_send_format(send, recv_ip):
        # ETTTP 형식에 맞는지 확인
        send_info = check_msg(send, recv_ip)
        if send_info == False:
            return False
        # SEND 형식이 맞는지 확인
        elif send_info[0] != 'SEND':
            return False
        else:
            return send_info

# ack message가 유효한 메세지인지 check
def check_ack_format(ack, recv_ip):
    # ETTTP 형식에 맞는지 확인
    ack_info = check_msg(ack, recv_ip)
    if ack_info == False:
        return False
    # ACK 형식이 맞는지 확인
    elif ack_info[0] != 'ACK':
        return False
    else:
        return ack_info
  
# result message가 유효한 메세지인지 check  
def check_result_format(result, recv_ip):
        # ETTTP 형식에 맞는지 확인
        result_info = check_msg(result, recv_ip)
        if result_info == False:
            return False
        # RESULT 형식이 맞는지 확인
        elif result_info[0] != 'RESULT':
            return False
        else:
            return result_info
        
def check_msg(msg, recv_ip):
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    # 메세지를 적절하게 분할
    split_msg = msg.split("\r\n")

    # 5개 이상으로 분할될 시 \r\n의 개수에 이상이 있는것이므로 False 반환
    if len(split_msg) != 5:
        return False

    # 분할된 문자열들로부터 메세지 종류와 프로토콜 종류, 수신ip를 구한다.
    msg_type = split_msg[0].split(" ")[0]
    protocol_ver = split_msg[0].split(" ")[1]
    check_ip = split_msg[1][split_msg[1].find(":") + 1:]

    # 프로토콜 체크
    if protocol_ver != "ETTTP/1.0":
        return False
    # 수신ip 체크
    if check_ip != recv_ip:
        return False

    # 메세지가 유효한 경우 메세지의 info를 담아 반환할 리스트
    res_msg = [msg_type]

    # 메세지 종류가 유효한지 체크하고 메세지 종류에 따라 반환할 값 처리
    if msg_type == "SEND" or msg_type == "ACK":
        # 메세지 종류가 SEND, ACK라면 New-Move:, First--Move:를 제거하고 좌표 값의 숫자만 남김
        if split_msg[2].find("New-Move:") != -1:
            split_msg[2] = split_msg[2].replace("New-Move:", "")
        elif split_msg[2].find("First-Move:") != -1:
            split_msg[2] = split_msg[2].replace("First-Move:", "")
            res_msg = res_msg + [split_msg[2]]
        # 메세지 종류가 SEND나 ACK지만 New-Move:, First--Move:를 포함하지 않는다면 False 반환
        else:
            return False
        res_msg = res_msg + re.findall(r'\d+', split_msg[2])
    # 메세지 종류가 RESULT라면
    elif msg_type == "RESULT":
        # Winner:를 제거하고 좌표값의 숫자만 남김
        if split_msg[2].find("Winner:") != -1:
            split_msg[2] = split_msg[2].replace("Winner:", "")
            res_msg.append(split_msg[2])
        # 메세지 종류가 RESULT여도 Winner:를 포함하지 않았다면 False
        else:
            return False
    # 메세지 종류가 SEND, ACK, RESULT 중 아무것도 아니라면 False
    else: return False

    return res_msg;
    ######################################################
