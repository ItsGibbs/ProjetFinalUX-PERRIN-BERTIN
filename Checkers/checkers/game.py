import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLACK, CYAN
from checkers.board import Board
from datetime import datetime
import socket
import pickle

host = '152.228.134.120'
port = 1234

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        daplayer = pickle.dumps(["yo"])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(daplayer)
            buff = s.recv(4096)
            daturn = pickle.loads(buff)
            print(daturn)
            self.player = daturn

    def get_new_board(self):
        while 1:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    buff = s.recv(4096)
                    newboard = pickle.loads(buff)
                    if newboard != None:
                        self.board.board = newboard
                        break
            except:
                pass


    # Update board
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        if (self.turn == RED and self.player == 1) or (self.turn == WHITE and self.player == 2):
            self.get_new_board()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.last_board = Board()

    # Winner
    def winner(self):
        return self.board.winner()

    # Reset
    def reset(self):
        self._init()

    # Select a piece
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            '''currboard = pickle.dumps(self.board.board)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    s.send(currboard)'''
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    # Move and change turn
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0:
        #and (row, col) in self.valid_moves:
            #daboard = str(self.board)
            #print(self.board.board)
            daboard = pickle.dumps([self.board.board, row, col, self.selected])
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    s.send(daboard)
                    buff = s.recv(4096)
                    damove = pickle.loads(buff)
                    print(damove)
                    if damove != False:
                        self.board.board = damove

                        '''self.board.move(self.selected, row, col)
                        #self.last_board = self.board.board
                        #self.board.move(damove, row, col)
                        skipped = self.valid_moves[(row, col)]
                        if skipped: 
                            self.board.remove(skipped)'''
                        self.change_turn()
        else:
            return False
            
        return True

    # Draw where the player can move
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, CYAN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    # Change player turn
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    # Get board
    def get_board(self):
        return self.board

    # Mave the AI move
    def ai_move(self, board):
        self.board = board
        self.change_turn()