import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLACK, CYAN
from checkers.board import Board
from datetime import datetime
import socket

host = '152.228.134.120'
port = 1548

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    # Update board
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

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
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    # Move and change turn
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    table = ' '.join(self.board)
                    s.connect((host, port))
                    s.sendall(table)
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped: 
                self.board.remove(skipped)
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