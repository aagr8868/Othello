import Othello

def PromptInput(game) -> (int,int):
	player = ""
	if game.WhosTurn() == 'B': player = 'Black'
	elif game.WhosTurn() == 'W': player = 'White'
	else: raise TypeError("What?")
	
	row = input(f"What row is {player} placing their piece in: ")
	col = input(f"What col is {player} placing their piece in: ")
	
	if not row.isdigit(): raise TypeError ("Must enter a positive intiger value for row")
	if not col.isdigit(): raise TypeError ("Must enter a positive intiger value for col")
	
	return (int(row),int(col))

player1 = Othello.Player('b')
player2 = Othello.Player('w')
game = Othello.Game([player1,player2],8)

game.PrintBoard()
game.PrintScores()
print("=========================")

for _ in range(game.board.size**2-4):
	row,col = PromptInput(game)
	game.TakeTurn(row,col)