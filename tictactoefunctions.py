import numpy as np 
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.functional import  softmax
import tictactoe_data
from torch import tensor


FILE_PATH = "tictactoeVerTestPercentage0DNN_[1584, 720, 360, 216, 180, 108, 72, 36, 16]_100Batch_epoch1000_0.001_model_state_dict.pth"
ROUND = 3


class NeuralNet(nn.Module):
    def __init__(self,input_dim, outputDim, units_per_layer):
        super(NeuralNet, self).__init__()
        self.Layers = nn.ModuleList()
        self.Layers.append(nn.Linear(input_dim, units_per_layer[0]))
        for r in range(1,len(units_per_layer)):
            self.Layers.append(nn.Linear(units_per_layer[r-1], units_per_layer[r]))
        self.Layers.append(nn.Linear(units_per_layer[-1], outputDim))
        self.Dropout1 = torch.nn.Dropout(p=0.5)


    def forward(self, x):
        for r in range(len(self.Layers)-1):
            if not 0:
                x = self.Dropout1(F.relu(self.Layers[r](x)))
            else:
                x = (F.relu(self.Layers[r](x)))
        x = self.Layers[-1](x)
        return x

def resolveMinLoss(losslist,winlist):
    print("------RESOLVE MIN LOSS--------")
    loss1 = np.argmin(losslist)
    print(f"ARGMIN: {loss1}")
    for r in range((losslist.size)):
        if r!=loss1 and losslist[loss1]==losslist[r]:
            print(f"IF STATEMENT: {losslist[loss1]}=={losslist[r]} | r = {r}")
            print("--------------------")
            return loss1 if winlist[loss1]>=winlist[r] else r
    print("--------------------")
    return loss1
def resolveMaxWin(losslist,winlist):
    win1 = np.argmax(winlist)
    for r in range((winlist.size)):
        if r!=win1 and winlist[win1]==winlist[r]:
            return win1 if losslist[win1]<=losslist[r] else r
    return win1
def getMovePosition(board1,board2):
    poslist = [board1==board2]

    return np.argmin(poslist)
# Runs the forward passs and makes the move with the highest 'Sure win'
def computer_move(board,firstmove):

    layer_list = [1584, 720, 360, 216, 180, 108, 72, 36, 16]

    model = NeuralNet(9,4, layer_list)
    model.load_state_dict(torch.load(FILE_PATH))
    model.eval()


    board_ = np.array(board)
    possible_moves = tictactoe_data.add_move(board_, 1, [], True)
    move_probs_win = []
    move_probs_loss = []
    move_probs_tie = []
    move_probs_dk = []
    r = torch.from_numpy(np.array(board_).reshape(9))
    r = r.type(torch.float32)
    with torch.no_grad():
        model.eval()
        # prob = softmax(model.forward(r))
        currentsituation = softmax(model.forward(r))


    for r in possible_moves:
        r = torch.from_numpy(r.reshape(9))
        r = r.type(torch.float32)
        with torch.no_grad():
            model.eval()
            # prob = softmax(model.forward(r))
            prob = (model.forward(r))
            move_probs_dk.append((prob[0]).item())
            move_probs_tie.append((prob[2]).item())
            move_probs_win.append((prob[1]).item())
            move_probs_loss.append((prob[3]).item())
    move_probs_win = np.array([round(l.item(),ROUND) for l in softmax(tensor(move_probs_win))])
    move_probs_loss = np.array([round(l.item(),ROUND) for l in softmax(tensor(move_probs_loss))])
    move_probs_dk = np.array([round(l.item(),ROUND) for l in softmax(tensor(move_probs_dk))])
    move_probs_tie = np.array([round(l.item(),ROUND) for l in softmax(tensor(move_probs_tie))])


    # maxwin = self.resolveMaxWin(move_probs_loss,move_probs_win)
    # minloss = self.resolveMinLoss(move_probs_loss,move_probs_win)
    def max2(list1):
        max1 = float("-inf")
        max1ind = -1
        max2 = float('-inf')
        max2ind = -1
        for r in range(len(list1)):
            if list1[r]>max1:
                max1 = list1[r]
                max1ind = r
                max2 = max1
                max2ind = max1ind
            elif list1[r]>max2:
                max2 = list1[r]
                max2ind = r
        return max1ind,max2ind

    def min2(list1):
        min1 = float("inf")
        min1ind = -1
        min2 = float('inf')
        min2ind = -1
        for r in range(len(list1)):
            if list1[r]<min1:
                min1 = list1[r]
                min1ind = r
                min2 = min1
                min2ind = min1ind
            elif list1[r]<min2:
                min2 = list1[r]
                min2ind = r
        return min1ind,min2ind

    minloss , minloss2 = min2(move_probs_loss)
    maxwin, maxwin2 = max2(move_probs_win)
    minwin = np.argmin(move_probs_win)
    maxloss,maxloss2 = max2(move_probs_loss)
    option1 =  currentsituation[0].item() +currentsituation[3].item() # 3 Corresponds to Loss
    option2 =  currentsituation[2].item()+ currentsituation[1].item() # 1 Corresponds to Win
    playedIndex = 0
    
    if firstmove:
        MAX_WIN = False
        MIN_LOSS = True
    else :
        MIN_LOSS = False 
        MAX_WIN = True

    #
    print("DK --- TIE --- WIN --- LOSS --- SUM")
    print(f" {(currentsituation[0].item()):.6f} --- {(currentsituation[2].item()):.6f} ---"
            f" {currentsituation[1].item():.6f} --- {(currentsituation[3].item()):.6f} ---")
    print("---------------------------------------------------")

    for r in range(len(move_probs_loss)):

        print(f" {(move_probs_dk[r]):.6f} --- {(move_probs_tie[r]):.6f} ---"
                f" {move_probs_win[r]:.6f} --- {(move_probs_loss[r]):.6f} ---"
                f" {move_probs_win[r]+move_probs_dk[r] + move_probs_loss[r] + move_probs_tie[r]}"
                f" Position: {getMovePosition(board_,possible_moves[r].reshape(9)) + 1}")
    print("----------------------------------")
    print(f"Considering: {(option2):.6f} --- {(option1):.6f} | Played:{getMovePosition(board_,possible_moves[playedIndex].reshape(9)) + 1}")
    # print(f"Considering: {(winPlusTie[winPlusTieIndex]):.6f} | Played:{self.getMovePosition(board_, possible_moves[winPlusTieIndex].reshape(9)) + 1}")
    if MIN_LOSS:
        index = minloss
        print("MIN LOSS")
    elif MAX_WIN:
        index = maxwin
        print("MAX WIN")
    move = possible_moves[index].reshape(9)
    print(move)
    move = np.argmin(board_==move) + 1

    
    return move