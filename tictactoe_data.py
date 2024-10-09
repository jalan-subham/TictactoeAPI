import numpy as np
import random

def generate_random_board():
    board = [random.choice(['X', 'O']) for _ in range(9)]
    return [board[i:i+3] for i in range(0, 9, 3)]

def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('-' * 5)

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != 0:
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        return board[0][2]
    return None

def classify_board(board):
    winner = check_winner(board)
    if winner:
        return f"{winner} wins"
    elif all(cell != ' ' for row in board for cell in row):
        return "Tie"
    else:
        return "Incomplete game"

# Generate and classify 5 random boards
batch2 = []

def not_considered(boards,l):
    for r in boards:
        if sum(r.reshape(9)==l.reshape(9)) ==9:
            return False

    return True


def add_move(board,move,batch,winningAllowed = False):
    newboards = []
    board = board.reshape(9)
    for r in range(9):
        if board[r] == 0:
            newboard = board.copy()
            newboard[r] = move
            newboard = newboard.reshape((3,3))
            if not winningAllowed :
                if not_considered(batch,newboard) and (check_winner(newboard)==None):
                    newboards.append(newboard)
            else:
                if not_considered(batch, newboard):
                    newboards.append(newboard)
    return newboards

def sure_win(board,batch):
    board = board.reshape(9)
    newboards = add_move(board,1,batch,True)
    for r in newboards:
        if check_winner(r) == 1:
            return True

    return False


def sure_tie(board,batch):
    newboards =  add_move(board,1,batch,True)
    for r in newboards:
        if check_winner(r) != None or sum(r.reshape(9)==np.zeros(9))>1:
            return False
    return True

def sure_loss(board,batch):
    newboard1  = add_move(board,1,batch,True)
    if len(newboard1) == 1:
        return False
    find_win = False
    for boarde in newboard1:
        newboards = add_move(boarde,-1,batch,True)
        find_win = False
        for r in newboards:
            if check_winner(r) == -1:
                find_win = True
        if not find_win:
            return False
    if find_win:
        return True
    return False

def create_batch(batch_no):
    batches = [[np.zeros(9).reshape(3,3)]]
    for r in range(batch_no):
        newbatch = []
        for k in batches[-1]:
            newbatch = newbatch + add_move(k, 1, newbatch)
        batches.append(newbatch)
        newbatch = []
        for k in batches[-1]:
            newbatch = newbatch + add_move(k, -1, newbatch)
        batches.append(newbatch)

    return batches[-1]

def label_batch(batch):
    labelTable = ['Dont Know' for r in range(len(batch))]
    for r in range(len(batch)):
        if sure_win(batch[r],batch) :
            labelTable[r] = "Sure Win"
        elif sure_loss(batch[r],batch):
            labelTable[r] = "Sure Loss"
        elif sure_tie(batch[r],batch):
            labelTable[r] = "Sure Tie"
    return labelTable


def create_data(batch_no):
    batch=create_batch(batch_no)
    labels = label_batch(batch)
    data = []
    for r in range(len(batch)):
        list1 = [l for l in batch[r].reshape(9)]
        list1.append(labels[r])
        data.append(list1)

    return data

class Batch0:
    pass