# CS111 SP17 
# Intro to CS final project collaboration
# Emma Qin
# A program that runs the game Connect Four.

import random
import copy

class Board:
    """
    This is the class board, with instance variables width, height, and boardConfig. 
    A board instance stores a particular board. boardConfig stores the current board 
    configuration: -1 represents empty space, 0 represents player0's piece, 1 represents
    player1's piece.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.boardConfig = [[-1] * self.height for index in range(self.width)]
        # self note: boardConfig[col][row]
    
    def getWidth(self):
        return self.width
        
    def getHeight(self):
        return self.height
    
    def isLegal(self, move):
        """
        This function determines if a move is legal.
        It returns true if the move is legal, and false if it is not.
        """
        if 0 <= move < self.width:
            if self.boardConfig[move][0] == -1:
                return True
        return False
                
    def play(self, playerNum, move):
        """
        This function allows players to play. It takes two inputs: who is playing and
        where that player chooses to play. It returns the successful state of the play
        and the coordinates of the play if successful.
        """
        # update with isLegal
        if self.isLegal(move):
            row = 0
            # while the space below is empty
            while ((row+1 < self.height) and (self.boardConfig[move][row + 1] == -1)):
                row += 1
            self.boardConfig[move][row] = playerNum  
            return True, move, row
        return False, None, None
    
    def playerXIsWin(self, X, col, row):
        """
        (col, row) was the last move. Return True if playerX wins after that move.
        It checks winning on horizontal, vertical, and both diagonals.
        """
        # if last move was not made by the player
        if self.boardConfig[col][row] != X: return False
        
        # horizontal check
        horizontalAccumulator = 1
        # check left side
        nextCol = col - 1
        while nextCol >= 0 and self.boardConfig[nextCol][row] == X:
            nextCol -= 1
            horizontalAccumulator += 1
        # check right side
        nextCol = col + 1
        while nextCol < self.width and self.boardConfig[nextCol][row] == X:
            nextCol += 1
            horizontalAccumulator += 1
        if horizontalAccumulator >= 4: return True
        
        # vertical check
        verticalAccumulator = 1
        # check downwards
        nextRow = row + 1
        while nextRow < self.height and self.boardConfig[col][nextRow] == X:
            nextRow += 1
            verticalAccumulator += 1
        if verticalAccumulator >= 4: return True
        
        # main diagonal check
        mainDiagonalAccumulator = 1
        # check left-up
        nextCol, nextRow = col - 1, row - 1
        while nextCol >= 0 \
          and nextRow >= 0 \
          and self.boardConfig[nextCol][nextRow] == X:
            nextCol -= 1
            nextRow -= 1
            mainDiagonalAccumulator += 1
        # check right-down
        nextCol, nextRow = col + 1, row + 1
        while nextCol < self.width \
          and nextRow < self.height \
          and self.boardConfig[nextCol][nextRow] == X:
            nextCol += 1
            nextRow += 1
            mainDiagonalAccumulator += 1
        if mainDiagonalAccumulator >= 4: return True
        
        # vice diagonal check
        viceDiagonalAccumulator = 1
        # check left-down
        nextCol, nextRow = col - 1, row + 1
        while nextCol >= 0 \
          and nextRow < self.height \
          and self.boardConfig[nextCol][nextRow] == X:
            nextCol -= 1
            nextRow += 1
            viceDiagonalAccumulator += 1
        # check right-up
        nextCol, nextRow = col + 1, row - 1
        while nextCol < self.width \
          and nextRow >= 0 \
          and self.boardConfig[nextCol][nextRow] == X:
            nextCol += 1
            nextRow -= 1
            viceDiagonalAccumulator += 1
        if viceDiagonalAccumulator >= 4: return True
        
        # if all winning checks failed, then the player didn't win
        return False
    
    def isTie(self):
        """
        It is tie when the board is full.
        """
        for col in range(0, self.getWidth()):
            if self.boardConfig[col][0] == -1: return False
        return True
            
    
    def printBoard(self):
        """
        It prints game board. x represents player0's piece. o represents player1's piece.
        Column indices are also printed below for readability.
        """
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.boardConfig[col][row] == -1: print(' ', end = '')
                if self.boardConfig[col][row] == 0: print('x', end = '')
                if self.boardConfig[col][row] == 1: print('o', end = '')
            print('')
        for num in range(0, self.width):
            print(num, end = '')
        print ('')
    
    
class GameState:
    """
    Each GameState instance is a state of the game. Each instance stores the board,
    both players, and the current player to play.
    """
    def __init__(self, board, player0Type, player1Type, currentPlayer = 0):
        self.board = board
        self.player0 = Player(player0Type, 0)
        self.player1 = Player(player1Type, 1)
        self.currentPlayer = currentPlayer
    
    def takeATurn(self):
        """
        This function lets the current player to take a turn. Then it checks whether the
        game ends after the turn. If the game ends, this function returns 1 if player0
        wins, -1 if player1 wins, 0 if the game is a tie. If the game doesn't end after 
        the move, this function updates the gameState and returns None.
        """
        if self.currentPlayer == 0:
            nextMove = self.player0.getMove(self.board)
        if self.currentPlayer == 1:
            nextMove = self.player1.getMove(self.board)
        success, col, row = self.board.play(self.currentPlayer, nextMove)
        # if the move was not legal
        if not success:
            print("please enter a valid move")
            return None
        if self.board.playerXIsWin(self.currentPlayer, col, row):
            if self.currentPlayer == 0: return 1
            if self.currentPlayer == 1: return -1
        if self.board.isTie(): return 0
        # if the game doesn't end after the last move
        self.currentPlayer = 1 - self.currentPlayer 
        return None
        
    def playOut(self):
        """
        This function lets the players take turns to play out the game to a result.
        The result is in the same form as takeATurn.
        """
        result = None
        while (result == None):
            result = self.takeATurn()
        return result


class Player:
    """
    Each player instance represents a player. Each player has his/her/its own type and 
    knows if he/she/it is player0 or player1. 
    """
    def __init__(self, playerType, playerNum):
        """
        There are three types of players available: human players - controlled by users.
        AI players - our intelligent agents, and random players - make random moves.
        """
        if playerType == "human": self.type = "human"
        if playerType == "AI": self.type = "AI"
        if playerType == "random": self.type = "random"
        self.num = playerNum
    
    def getMove(self, board):
        """
        This function defines strategies of three types of players. Human players manually 
        input their moves. AI players try out legal moves and continue with random and then
        choose one with the best result. Random player randomly take a legal move.
        This function returns the column index of move chosen.
        """
        # human players choose manually
        if self.type == "human":
            board.printBoard()
            move = int(input("what's your next move?"))
        
        if self.type == "AI":
            legalMoves = []
            scores = []
            for move in range(0, board.getWidth()):
                if board.isLegal(move):
                    legalMoves.append(move)
                    scores.append(0)
            # try each legal move
            for move in legalMoves:
                newBoard = copy.deepcopy(board)
                success, col, row = newBoard.play(self.num, move)
                # if AI wins immediately after this move
                if newBoard.playerXIsWin(self.num, col, row): 
                    scores[legalMoves.index(move)] = 9999
                else:       # try 1000 random games if AI takes the move
                    for trial in range(0, 1000):
                        testGame = GameState(copy.deepcopy(newBoard), "random", "random", 1 - self.num)
                        scores[legalMoves.index(move)] += ((-1) ** self.num) * testGame.playOut()
            # find the best score
            bestScore = -9999
            for score in scores:
                if score > bestScore:
                    bestScore = score
            # find the move that leads to the best score. If there is a tie, choose 
            # randomly among the best.
            bestScoreIndices = []
            for index in range(0, len(scores)):
                if scores[index] == bestScore: 
                    bestScoreIndices.append(index)
            bestScoreIndex = random.choice(bestScoreIndices)
            move = legalMoves[bestScoreIndex]
                    
        # random players choose randomly from legal moves
        if self.type == "random":
            legalMoves = []
            for move in range(0, board.getWidth()):
                if board.isLegal(move):
                    legalMoves.append(move)
            move = random.choice(legalMoves)
        
        return move

    
def main():
    """
    Main funcation creates a board with 8 * 8.
    It will randomly decide which player goes first.
    It will print the board after each move.
    It will print the result of the game.
    """
    print("Connect Four is a two-player game. Players\n\
can drop pieces from the top into a \n\
vertically suspended grid. The pieces \n\
fall and occupy the lowest available \n\
spaces in the grid. The player who\n\
first connects four pieces in the horizontal,\n\
vertical, or diagonal line will WIN the game.")
    print("First player plays x and second player plays o.")
    emptyBoard = Board(8, 8)
    randomNum = random.random()
    if randomNum < 0.5:
        print ("You go first.")
        newGame = GameState(emptyBoard, "human", "AI") 
        result = newGame.playOut()
        if result == 1: 
            print("human wins")
        if result == -1: 
            print("AI wins")
        if result == 0:
            print("It's a tie")
    else: 
        print ("You go second.")
        newGame = GameState(emptyBoard, "AI", "human")
        result = newGame.playOut()
        if result == 1: 
            print("AI wins")
        if result == -1: 
            print("human wins")
        if result == 0:
            print("It's a tie")

if __name__ == "__main__":
    main()

   
