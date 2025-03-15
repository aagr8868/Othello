import numpy as np
from enum import Enum

class Direction(Enum):
	N = 0
	NE = 1
	E = 2
	SE = 3
	S = 4
	SW = 5
	W = 6
	NW = 7

class Board:
	def __init__(self,size:int) -> None:
		"""
		Initalzie board class
		Input: Size of board
		Output: None
		"""
		if size % 2:
			raise ValueError(f"board must be an even sized square, recieved ({size})")
		
		# initalize board to all zeros
		self.size = size
		self.board = np.array(np.zeros([size,size]))
		
		mid = int(size / 2)
		# place down two inital black chips
		self.Place('B',mid,mid)
		self.Place('B',mid-1,mid-1)
		
		# place down two inital white chips
		self.Place('W',mid-1,mid)
		self.Place('W',mid,mid-1)
		
		return
	# ----------------------------------------------
	def Place(self,color:str,row:int,col:int) -> None:
		"""
		Placea piece on the board
		Input: color -> Color to place
		       row -> row to place piece on
			   col -> column to place piece on
		Output: None
		"""
		if row >= self.size:
			raise ValueError(f"Trying to place piece outside of board:\n \t size = {self.size} row = {row}")
		if col >= self.size:
			raise ValueError(f"Trying to place piece outside of board:\n \t size = {self.size} col = {col}")
		if len(color) != 1:
			raise ValueError(f"color must be SINGULAR CHARACTER 'B' or 'W', recieved: {color}")
		color = color.upper()
		if not color in ['B','W']:
			raise ValueError(f"color must be 'B' or 'W' not '{color}'")
		if self.board[row][col] != 0:
			raise ValueError(f"The location ({row},{col}) is already filled with a {int(self.board[row][col])} piece.\n\t1 for Black, -1 for White")

		
		if color == 'B':
			self.board[row][col] = 1
		elif color == 'W':
			self.board[row][col] = -1
		else:
			raise ValueError("How did I get here?")
		return
	# ----------------------------------------------
	def FlipPiece(self,row:int,col:int) -> None:
		"""
		Flips a pice from Black to White or White to Black
		Input: row -> row where to flip on board
		       col -> column where to flip on board
		Output: None
		"""
		if self.board[row][col] == -1: self.board[row][col] = 1
		elif self.board[row][col] == 1: self.board[row][col] = -1
		else:
			raise ValueError(f"({row},{col}) has a value of {self.board[row][col]} and thus cannot be flipped")
		return
	# ----------------------------------------------
	def GetBoardState(self) -> list[float]:
		"""
		returns the board variable
		Input: None
		Output: board list of floats of shape (size,size)
		"""
		return self.board
	
# ////////////////////////////////////////////////////////////////

class Player:
	def __init__(self, color: str, score: int = 2) -> None:
		"""
		Initalize player class
		Input: color -> player color
		       score -> player starting score (default 2)
		Output: None
		"""
		if not color.upper() in ['B','W']:
			raise ValueError(f"player must be either 'B' or 'W' not '{color}'")
		self.color = color.upper()
		self.score = score
		return
	# ----------------------------------------------
	def IncreaseScore(self,inc:int = 1) -> None:
		"""
		Increase the score of the player
		Input: inc -> how much to increase the score by
		Output: None
		"""
		self.score = self.score + inc
		return
	# ----------------------------------------------
	def DecreaseScore(self,dec:int = 1) -> None:
		"""
		Decrease the score of the player
		Input: dec -> how much to decrease the score by
		Output: None
		"""
		self.score = self.score - dec
		return

# ////////////////////////////////////////////////////////////////
	
class Game:
	def __init__(self, players:list[Player],size = 4) -> None:
		"""
		Initalize Game class
		    used as game engine
		Input: players -> list of player objects that will store scores
		       size -> size of the board, 4 X 4 by default
		Output: None
		"""
		if len(players) != 2:
			raise ValueError(f"Othello is a 2 player game not a {len(players)} player game")
		self.players = players # list of players playing
		self.whos_turn = 0 # intiger itterating to keep track of who is plaing in player list
		self.turncount = 0 # intiger keeping track of number of turns played. should not go above # of empty squares in board (12 be default)
		self.board = Board(size) #board object
		return
	# ----------------------------------------------
	def PrintBoard(self) -> None:
		"""
		prints the state of the board to terminal
		Input: None
		Output: None
		"""
		board = self.board.GetBoardState()
		cols = "  "
		for i in list(range(self.board.size)):
			cols += str(i) + " "
		print(cols)
		display = []
		for i in range(len(board)):
			row = [str(i)]
			for j in range(len(board)):
				if (board[i][j] == 1):
					row.append('B')
				elif (board[i][j] == -1):
					row.append('W')
				elif (board[i][j] == 0):
					row.append('_')
				else: raise TypeError("How? Just How.")
			display.append(row)
		for i in display:
			row = ""
			for j in i:
				row += j + ' '
			print(row)
		return
	# ----------------------------------------------
	def PrintScores(self) -> None:
		"""
		prints the scores of each player so far
		Input: None
		Output: None
		"""
		
		for player in self.players:
			print(f"{player.color} has a score of {player.score}")
		
		return
	# ----------------------------------------------
	def TakeTurn(self, row:int, col:int) -> None:
		"""
		take a turn following Othello rules
		Input: Where to palce a piece
			row: row on board
			col: column on board
		Output: None
		"""
		# place a piece
		color = self.players[self.whos_turn].color
		self.board.Place(color,row,col)
		self.players[self.whos_turn].IncreaseScore()
		# update pieces & scores
		self.UpdateFrom(color,row,col)
		# update who's turn it is
		self.whos_turn = (self.whos_turn + 1) % 2
		# update UI
		self.PrintBoard()
		self.PrintScores()
		print("=========================")
		return
	# ----------------------------------------------
	def UpdateFrom(self,color:str, row:int, col:int) -> None:
		"""
		updates any piece that must change colors along all 8 directions from (row,col) on the board
		starts by getting start and end points inbetween, then calls change to flip the pieces acordingly and update the score acordingly
		Input: row -> row where the piece was placed
		       col -> column where the piece was placed
			   color -> the color that was placed
		Output: None
		"""
		if not color.upper() in ['B', 'W']:
			raise ValueError(f"color must be 'B' or 'W' not {color}")
		color = color.upper()
		if row >= self.board.size or row < 0:
			raise ValueError(f"trying to place a piece outside of the board of size {self.board.size} (row = {row})")
		if col >= self.board.size or col < 0:
			raise ValueError(f"trying to place a piece outside of the board of size {self.board.size} (col = {col})")
		
		swapfrom = 0
		if color == 'B':
			swapfrom = -1
			swapto = 1
		elif color == 'W':
			swapfrom = 1
			swapto = -1
		else: raise TypeError("How did I get here now!?!")
		
		for d in Direction:
			start_row = row
			start_col = col
			if d == Direction.W:
				end_row = row
				end_col = col - 1
			elif d == Direction.N:
				end_row = row - 1
				end_col = col
			elif d == Direction.S:
				end_row = row + 1
				end_col = col
			elif d == Direction.E:
				end_row = row
				end_col = col + 1
			elif d == Direction.NW:
				end_row = row - 1
				end_col = col - 1
			elif d == Direction.NE:
				end_row = row - 1
				end_col = col + 1
			elif d == Direction.SW:
				end_row = row + 1
				end_col = col - 1
			elif d == Direction.SE:
				end_row = row + 1
				end_col = col + 1
			else:
				raise TypeError("Cardinal direction does not exsist 0x194-2")
			
			moved = False
			
			# find end point
			while (end_col >= 0 and end_row >= 0 and end_col < self.board.size and end_row < self.board.size and self.board.board[end_row][end_col] == swapfrom):
				if d == Direction.W:
					end_col = end_col - 1
					moved = True
				elif d == Direction.N:
					end_row = end_row - 1
					moved = True
				elif d == Direction.S:
					end_row = end_row + 1
					moved = True
				elif d == Direction.E:
					end_col = end_col + 1
					moved = True
				elif d == Direction.NW:
					end_col = end_col - 1
					end_row = end_row - 1
					moved = True
				elif d == Direction.NE:
					end_col = end_col + 1
					end_row = end_row - 1
					moved = True
				elif d == Direction.SW:
					end_col = end_col - 1
					end_row = end_row + 1
					moved = True
				elif d == Direction.SE:
					end_col = end_col + 1
					end_row = end_row + 1
					moved = True
				else: raise TypeError("Cardinal direction does not exsist 0x194-1")
				
			if moved and end_col >= 0 and end_row >= 0 and end_col < self.board.size and end_row < self.board.size and self.board.board[end_row][end_col] == swapto:
				self.change(d,(start_row,start_col),(end_row,end_col),self.players[self.whos_turn].color)
		return
	# ----------------------------------------------
	def change(self,d:Direction,start:(int,int),end:(int,int),color:str) -> None:
		"""
		Flips all chips in line-segment from start to end to color color in direction d by calling flip
		Input: d -> direcion to flip starting from start point
		       start -> tuple of starting coordinates (row,col)
			   end -> tuple of ending coordinates (row,col)
			   color -> color flipping the tokens to (player gaining points)
		Output: None
		"""
		
		if d == Direction.N:
			start = (start[0]-1,start[1])
			# end = (end[0]+1,end[1])
			pass
		elif d == Direction.E:
			start = (start[0],start[1]+1)
			# end = (end[0],end[1]-1)
			pass
		elif d == Direction.S:
			start = (start[0]+1,start[1])
			# end = (end[0]-1,end[1])
			pass
		elif d == Direction.W:
			start = (start[0],start[1]-1)
			# end = (end[0],end[1]+1)
			pass
		elif d == Direction.NE:
			start = (start[0]-1,start[1]+1)
			# end = (end[0]+1,end[1]-1)
			pass
		elif d == Direction.SE:
			start = (start[0]+1,start[1]+1)
			# end = (end[0]-1,end[1]-1)
			pass
		elif d == Direction.SW:
			start = (start[0]+1,start[1]-1)
			# end = (end[0]-1,end[1]-1)
			pass
		elif d == Direction.NW:
			start = (start[0]-1,start[1]-1)
			# end = (end[0]+1,end[1]+1)
			pass
		
		if start[0] not in range(self.board.size):
			raise ValueError(f"start point not on board {start}")
		if start[1] not in range(self.board.size):
			raise ValueError(f"start point not on board {start}")
		if end[0] not in range(self.board.size):
			raise ValueError(f"start point not on board {end}")
		if end[1] not in range(self.board.size):
			raise ValueError(f"start point not on board {end}")
		if color not in ['B','W']:
			raise ValueError(f"color {color} does not exsist")
		
		# if only flipping one piece in list
		if start == end:
			self.board.FlipPiece(end[0],end[1])
			for p in self.players:
				if p.color == color: p.IncreaseScore()
				else: p.DecreaseScore()
			return
		# if flipping multiple pieces
		at = start
		while(at != end):
			self.board.FlipPiece(at[0],at[1])
			for p in self.players:
				if p.color == color: p.IncreaseScore()
				else: p.DecreaseScore()
			if d == Direction.W:
				at = (at[0],at[1]-1)
			elif d == Direction.N:
				at = (at[0]-1,at[1])
			elif d == Direction.E:
				at = (at[0],at[1]+1)
			elif d == Direction.S:
				at = (at[0]+1,at[1])
			elif d == Direction.NW:
				at = (at[0]-1,at[1]-1)
			elif d == Direction.NE:
				at = (at[0]-1,at[1]+1)
			elif d == Direction.SE:
				at = (at[0]+1,at[1]+1)
			elif d == Direction.SW:
				at = (at[0]+1,at[1]-1)
			else:
				raise TypeError("Seriously, how did I get here?")
		return
	# ----------------------------------------------
	def WhosTurn(self) -> str:
		return self.players[self.whos_turn].color
# ////////////////////////////////////////////////////////////////