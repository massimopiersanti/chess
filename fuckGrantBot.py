import chess
import chess.polyglot
import random
from random import randrange

def evaluate(board, color):
    whiteTotal = 0
    blackTotal = 0
    for i in range(64):
        piece = board.piece_at(i)
        if piece == None:
            continue
        if piece.color:
            whiteTotal += piece.piece_type
        else:
            blackTotal += piece.piece_type
    if color == 1:
        return (blackTotal - whiteTotal)
    if color == 0:
        return (whiteTotal - blackTotal)

def maxi(depth, board, color):
    legalMoves = list(board.legal_moves)
    tableOfScores = []
    if depth == 0: 
        for move in legalMoves:
            board.push(move)
            if(board.is_checkmate()):
                return  [100000, move]
            tableOfScores.append([evaluate(board, color), move])
            board.pop()
        largestDif = [0, 0]
        for pee in tableOfScores:
            if pee[0] > largestDif[0]:
                largestDif = pee
        return largestDif
    max = [1000, legalMoves[0]]
    for move in legalMoves:
        newBoard = board.copy()
        newBoard.push(move)
        tally = mini(depth - 1, newBoard, color)
        if tally[0] > max[0]:
            max= tally
    return max

def mini(depth, board, color):
    legalMoves = list(board.legal_moves)
    tableOfScores = []
    if depth == 0: 
        for move in legalMoves:
            board.push(move)
            if(board.is_checkmate()):
                return  [10000, move]
            tableOfScores.append([evaluate(board, color), move])
            board.pop()
        largestDif = [0, 0]
        for pee in tableOfScores:
            if pee[0] > largestDif[0]:
                largestDif = pee
        return largestDif
    min = [1000,legalMoves[0]]
    for move in legalMoves:
        newBoard = board.copy()
        newBoard.push(move)
        tally = maxi(depth -1, newBoard, color)
        if tally[0] < min[0]:
            min = tally
    return min





def sexy_play_method(board, color):
    # hey grant
    temp = maxi(2, board, color)
    return temp[1]


# color = 1 
# board = chess.Board()

# while True:
#     if(board.is_checkmate() or board.is_stalemate() or board.can_claim_draw()):
#         print("game end")
#         break
        
#     temp = sexy_play_method(board, color)
#     print("********")
#     print(temp)
#     move = temp[1]
#     board.push(move)
#     print(board)
#     if color == 1:
#         color = 0
#     if color == 0:
#         color = 1