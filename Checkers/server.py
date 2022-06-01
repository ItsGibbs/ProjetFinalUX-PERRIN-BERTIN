import socket, multiprocessing, pickle
from copy import deepcopy
import pygame
from checkers.board import Board
from _thread import *

host = '152.228.134.120'
port = 1234
#nb_workers = 10
ThreadCount = 0

board = Board()
nb_player = 0

def client_handler(conn):
	
	while True:
		buff = conn.recv(4096)
		message  = pickle.loads(buff)
		print(message)
		if message[0] == "yo":
			global nb_player
			nb_player += 1
			msg = pickle.dumps([nb_player])
			conn.sendall(msg)
		else:
			check = False
			board.board = message[0]
			if ((message[1], message[2]) in board.get_valid_moves(message[3])):
				check = True
				valid_move = board.get_valid_moves(message[3])
				board.move(message[3], message[1], message[2])
				skipped = valid_move[(message[1], message[2])]
				if skipped:
					board.remove(skipped)
				#change_turn()
				check = board.board
#			if is_move_valid():
			msg = pickle.dumps(check)
			conn.sendall(msg)

def accept_connections(s):
	Client, address = s.accept()
	print('Connected to: ' + address[0] + ':' + str(address[1]))
	start_new_thread(client_handler, (Client, ))

def start_server(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind((host, port))
	except socket.error as e:
		print(str(e))
	print(f'Server is listing on the port {port}...')
	s.listen()

	while True:
		accept_connections(s)
start_server(host, port)


'''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(1)
	with multiprocessing.Pool(nb_workers) as pool:
		while True:
			conn, address = s.accept()
			pool.apply(handle, (conn, address))
'''
#		with multiprocessing.Pool(nb_workers) as pool:
#			while True:
#				conn, address = s.accept()
#				pool.apply(handle, (conn, address))

'''
def handle(conn, address):
	with conn:
		buff = conn.recv(4096)
		message  = pickle.loads(buff)
		print(message)
		if message[0] == "yo":
			nb_player += 1
			msg = pickle.dumps(nb_player)
			conn.sendall(msg)
		else:
			check = False
			board.board = message[0]
			if ((message[1], message[2]) in board.get_valid_moves(message[3])):
				check = True
				valid_move = board.get_valid_moves(message[3])
				board.move(message[3], message[1], message[2])
				skipped = valid_move[(message[1], message[2])]
				if skipped:
					board.remove(skipped)
				#change_turn()
				check = board.board
#			if is_move_valid():
			msg = pickle.dumps(check)
			conn.sendall(msg)
'''
#def is_move_valid():
#	currBoard = message
#	wantedBoard = msg



