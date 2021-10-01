import chess
import chess.polyglot
import random
from random import randrange
import math
import time

def evaluate(board):
    whiteTotal = 0
    blackTotal = 0
    for i in range(64):
        piece = board.piece_at(i)
        if piece == None:
            continue
        if piece.color:
            whiteTotal += piece.piece_type*10
        else:
            blackTotal += piece.piece_type*10

    if board.turn:
        return (blackTotal - whiteTotal)
    else:
        return (whiteTotal - blackTotal)
    
    
def minimax(depth, board, alpha, beta, maximizing):
    if(depth == 0):
        return evaluate(board)
    possibleMoves = board.legal_moves
    if(maximizing):
        bestMove = -9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = max(bestMove,minimax(depth - 1, board,alpha,beta, not maximizing))
            board.pop()
            alpha = max(alpha,bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(bestMove, minimax(depth - 1, board,alpha,beta, not maximizing))
            board.pop()
            beta = min(beta,bestMove)
            if(beta <= alpha):
                return bestMove
        return bestMove



def sexy_play_method(depth, board, prevMoveStack, start_time, time_to_run):
    # new strat, just try and take a higher value piece
    completed = True
    maximizing = True
    legalMoves = board.legal_moves
    bestMoveValue = -10000
    bestMove = None
    for x in legalMoves:

        if (time.time() - start_time >= time_to_run):
            completed = False
            return [completed, None]

        move = chess.Move.from_uci(str(x))

        #this is to speed things up and hopefully take greater value pieces
        fromSquare = move.from_square
        toSquare = move.to_square
        valueOfAttacker = board.piece_at(fromSquare)
        valueOfTaken = board.piece_at(toSquare)
        if valueOfTaken is not None and valueOfAttacker is not None:
            if valueOfTaken.piece_type > valueOfAttacker.piece_type:
                return [completed, move]

        board.push(move)
        value = max(bestMoveValue, minimax(depth - 1, board,-10000,10000, not maximizing))
        board.pop()
        if( value > bestMoveValue):
            #stop repeat moves
            if(len(prevMoveStack) > 2 and move in prevMoveStack):
                #prevMoveStack[-2] == move
                #print("move skipped")

                continue
            
            bestMoveValue = value
            bestMove = move
    move = chess.Move.from_uci(str(bestMove))

        
    return [completed, move]


prevMoveStack = []
def takeMove(board, time_to_run, prevMoveStack):
    start_time=time.time()

    for depth in range(1,100):
        out = sexy_play_method(depth, board, prevMoveStack, start_time, time_to_run)
        if out[0]: #If completed depth before time limit
            best_move=out[1]
        if(time.time()-start_time >= time_to_run):
            break
    prevMoveStack.append(best_move)
    return best_move


    


# prevMovStackWhite = []
# def takeMoveWhite(board):
#     move = takeMove(board, 1, prevMovStackWhite)
#     prevMovStackWhite.append(move)
#     return move


# prevMovStackBlack = []
# def takeMoveBlack(board):
#     move = takeMove(board, 1, prevMovStackBlack)
#     prevMovStackBlack.append(move)
#     return move

# board = chess.Board()
# move = chess.Move.from_uci("e2e4")
# board.push(move)
# board.push(sexy_play_method(board))
# print(board)

# board = chess.Board()
# while(True):   
#     if(board.turn):
#         move = takeMoveWhite(board)
#     else:
#         move = takeMoveBlack(board)
#     print(move)
#     board.push(move)
#     print(board)
