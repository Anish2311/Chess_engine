from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import copy
import random

transPositionMap = {}
staleMate = {}
zobrist = [[random.getrandbits(64) for _ in range(64)] for _ in range(12)]
# print(zobrist)
hashing = 0
pos = 'pPrRnNbBqQkK'

mapper = {'P':[[4.7,4.7,4.7,4.7,4.7,4.7,4.7,4.7],
    [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2],
    [1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],
    [1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0]],
'p':[[0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05],
    [1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],
    [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2],
    [4.7,4.7,4.7,4.7,4.7,4.7,4.7,4.7]
],
'n':[[0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95]
],
'N':[[0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,1,1,1,1,1,1,0.95],
    [0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95]
],
'b':[[1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1.05,1.05,1.05,1.05,1.05,1.05,1],
    [1,1.05,1.1,1.1,1.1,1.1,1.05,1],
    [1,1.05,1.1,1.1,1.1,1.1,1.05,1],
    [1,1.05,1.05,1.05,1.05,1.05,1.05,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
],
'B':[[1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1.05,1.05,1.05,1.05,1.05,1.05,1],
    [1,1.05,1.1,1.1,1.1,1.1,1.05,1],
    [1,1.05,1.1,1.1,1.1,1.1,1.05,1],
    [1,1.05,1.05,1.05,1.05,1.05,1.05,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
],
'r':[[1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05],
    [1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],
    [1,1,1,1,1,1,1,1]
],
'R':[[1,1,1,1,1,1,1,1],
    [1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],
    [1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
],
'q':[[1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
],
'Q':[[1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
],
'k':[[1.5,1.5,1.05,1,1,1.05,1.5,1.5],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
],
'K':[
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1.5,1.5,1.05,1,1,1.05,1.5,1.5]
]}
numberMap = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
marking = 'abcdefgh'
board = []
points = 0
bcheck = False
wcheck = False
bl = []
wl = []
counter = 0
bp = {}
wp = {}
canCastle = {'wk':'no','wq':'no','bk':'no','bq':'no'}
pointDist = {'p':-1,'r':-5,'b':-3.2,'n':-3,'q':-9,'k':-1,'P':1,'R':5,'B':3.2,'N':3,'Q':9,'K':1}
wattack = []
battack = []
will = {}
bill = {}
depth = 3
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health() :
    return "ok"

@app.post("/upload")
async def upload_file(
    fenn: str = Form(...),
    colour: str = Form(...),
    starting: str = Form(...)):
    global counter
    global bp
    global wp
    global hashing
    global canCastle
    global depth
    print(">>> /upload called. Starting computation.")
    fen = fenn
    board.clear()
    bp = {'p':[],'r':[],'b':[],'n':[],'q':[],'k':[]}
    wp = {'P':[],'R':[],'B':[],'N':[],'Q':[],'K':[]}
    transPositionMap.clear()
    hashing = 0
    counter = 0
    fenConvert(fen)
    # print(hashing)
    if starting == 'true':
        staleMate.clear()
        staleMate[hashing] = 1
    canCastle = {'wk':'no','wq':'no','bk':'no','bq':'no'}
    # if hashing in staleMate:
    #     staleMate[hashing] += 1
    # print(fen)
    if colour == 'true':
        chance = True
    else:
        chance = False
    legalMoves(chance == False,False)
    leg = legalMoves(chance,False)
    # print(leg)
    res = compute(chance,depth,'init',leg)
    move = res[1]
    print(res)
    # print(move,res,canCastle)
    j = marking.index(move[0])
    y = marking.index(move[3])
    i = 8 - int(move[1])
    x = 8 - int(move[4])
    remvp = str(board[x][y])
    bij = move[2]
    if len(move) == 6:
        bij = move[5]
    # print(move,bij,wp)
    if remvp != ' ':
        hashing ^= zobrist[pos.index(remvp)][y + x * 8]
    hashing ^= zobrist[pos.index(board[i][j])][j + i * 8]
    hashing ^= zobrist[pos.index(bij)][y + x * 8]
    # print(hashing)
    if hashing in staleMate:
        staleMate[hashing] += 1
    else:
        staleMate[hashing] = 1
    # print(counter)
    # print(staleMate)
    print(res)
    if board[i][j].lower() == 'r':
        if board[i][j].islower():
            if j == 0:
                canCastle['bq'] = 'no'
            elif j == 7:
                canCastle['bk'] = 'no'
        else:
            if j == 0:
                canCastle['wq'] = 'no'
            elif j == 7:
                canCastle['wk'] = 'no'
    if board[i][j].lower() == 'k':
        if board[i][j].islower():
            canCastle['bk'] = 'no'
            canCastle['bq'] = 'no'
        else:
            canCastle['wk'] = 'no'
            canCastle['wq'] = 'no'
    return {'move':res[1]}

def fenConvert(f):
    global points
    global hashing
    points = 0
    board.append([])
    sqCount = 0
    fe = f.split()
    iterF = fe[0]
    if len(fe) > 1:
        if ('K' in fe[1]):
            canCastle['wk'] = 'yes'
        if ('k' in fe[1]):
            canCastle['bk'] = 'yes'
        if ('Q' in fe[1]):
            canCastle['wq'] = 'yes'
        if ('q' in fe[1]):
            canCastle['bq'] = 'yes'
    for i in iterF:
        if i == '/':
            board.append([])
        else:
            if i.isdigit():
                board[-1].extend([' ']*int(i))
                sqCount += int(i)
            else:
                points += pointDist[i]*mapper[i][len(board)-1][len(board[-1])]
                sqCount += 1
                hashing ^= zobrist[pos.index(i)][sqCount - 1]
                if i in bp:
                    bp[i].append([len(board)-1,len(board[-1])])
                elif i in wp:
                    wp[i].append([len(board)-1,len(board[-1])])
                board[-1].append(i)
    if bp['k'][0] == [0,4]:
        if [0,0] not in bp['r']:
            canCastle
                
def pawn(i,j):
    global wcheck
    global bcheck
    global wl
    global bl
    lmoves = []
    piece = board[i][j]
    # print(piece,i,j)
    s = -1
    if piece.islower():
        s = 1
    k = i + s
    if k >= 0 and k < 8:
        if board[k][j] == ' ':
            lmoves.append([k,j])
        p = j + 1
        if p < 8:
            if board[k][p] != ' ':
                if board[k][p].islower() != piece.islower():
                    lmoves.append([k,p])
                    if board[k][p].lower() == 'k':
                        if piece.islower():
                            wcheck = True
                            wl.append([i,j])
                        else:
                            bcheck = True
                            bl.append([i,j])
            if s == -1:
                wattack.append([k,p])
            else:
                battack.append([k,p])

        p = j - 1
        if p >= 0:
            if board[k][p] != ' ':
                if board[k][p].islower() != piece.islower():
                    lmoves.append([k,p])
                    if board[k][p].lower() == 'k':
                        if piece.islower():
                            wcheck = True
                            wl.append([i,j])
                        else:
                            bcheck = True
                            bl.append([i,j])
            if s == -1:
                wattack.append([k,p])
            else:
                battack.append([k,p])
        if s > 0 and i == 1 and board[i + 1][j] == ' ' and board[i + 2][j] == ' ':
            lmoves.append([i+2,j])
        if s < 0 and i == 6 and board[i - 1][j] == ' ' and board[i - 2][j] == ' ':
            lmoves.append([i-2,j])
    return lmoves

def straight(i,j):
    global wcheck
    global bcheck
    global wl
    global bl
    global will
    global bill
    lmoves = []
    piece = board[i][j]
    l = i - 1
    m = j
    pieceCounter = 'a'
    path = [[i,j]]
    while l >= 0:
        path.append([l,m])
        if board[l][m] == ' ':
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        elif board[l][m].islower() != piece.islower():
            path.pop()
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend(path)
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend(path)
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
                pieceCounter = m + l * 8
            else:
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        will[pieceCounter] = path
                    else:
                        bill[pieceCounter]=path
                break
        else:
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
            break
        l -= 1
    l = i + 1
    m = j
    pieceCounter = 'a'
    path = [[i,j]]


    while l < 8:
        path.append([l,m])
        if board[l][m] == ' ':
            if  pieceCounter == 'a':
                lmoves.append([l,m])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        elif board[l][m].islower() != piece.islower():
            path.pop()
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend(path)
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend(path)
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
                pieceCounter = m + l * 8
            else:
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        will[pieceCounter] = path
                    else:
                        bill[pieceCounter]=path
                break
        else:
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
            break
        l += 1
    l = i
    m = j - 1
    pieceCounter = 'a'
    path = [[i,j]]

    while m >= 0:
        path.append([l,m])

        if board[l][m] == ' ':
            if  pieceCounter == 'a':
                lmoves.append([l,m])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        elif board[l][m].islower() != piece.islower():
            path.pop()
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend(path)
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend(path)
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
                pieceCounter = m + l * 8
            else:
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        will[pieceCounter] = path
                    else:
                        bill[pieceCounter]=path
                break
        else:
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
            break
        m -= 1
    l = i 
    m = j + 1
    pieceCounter = 'a'
    path = [[i,j]]

    while m < 8:
        path.append([l,m])

        if board[l][m] == ' ':
            if  pieceCounter == 'a':
                lmoves.append([l,m])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        elif board[l][m].islower() != piece.islower():
            path.pop()
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend(path)
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend(path)
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
                pieceCounter = m + l * 8
            else:
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        will[pieceCounter] = path
                    else:
                        bill[pieceCounter]=path
                break
        else:
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
            break
        m += 1
    return lmoves

def diagnol(i,j):
    global wcheck
    global bcheck
    global wl
    global bl
    global will
    global bill
    piece = board[i][j]
    lmoves = []

    l = i - 1
    m = j - 1
    pieceCounter = 'a'
    path = [[i,j]]

    while l >= 0 and m >= 0:
        path.append([l,m])
        if board[l][m] == ' ':
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        elif board[l][m].islower() != piece.islower():
            path.pop()
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend(path)
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend(path)
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
                pieceCounter = m + l * 8
            else:
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        will[pieceCounter] = path
                    else:
                        bill[pieceCounter]=path
                break
        else:
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
            break
        l -= 1
        m -= 1

    l = i - 1
    m = j + 1
    pieceCounter = 'a'
    path = [[i,j]]


    while l >= 0 and m < 8:
        path.append([l,m])
        if board[l][m] == ' ':
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        elif board[l][m].islower() != piece.islower():
            path.pop()
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend(path)
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend(path)
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
                pieceCounter = m + l * 8
            else:
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        will[pieceCounter] = path
                    else:
                        bill[pieceCounter]=path
                break
        else:
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
            break
        l -= 1
        m += 1

    l = i + 1
    m = j + 1
    pieceCounter = 'a'
    path = [[i,j]]


    while l < 8 and m < 8:
        path.append([l,m])
        if board[l][m] == ' ':
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        elif board[l][m].islower() != piece.islower():
            path.pop()
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend(path)
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend(path)
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
                pieceCounter = m + l * 8
            else:
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        will[pieceCounter] = path
                    else:
                        bill[pieceCounter]=path
                break
        else:
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
            break
        l += 1
        m += 1

    l = i + 1
    m = j - 1
    pieceCounter = 'a'
    path = [[i,j]]

    
    while l < 8 and m >= 0:
        path.append([l,m])
        if board[l][m] == ' ':
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        elif board[l][m].islower() != piece.islower():
            path.pop()
            if pieceCounter == 'a':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend(path)
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend(path)
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
                # print(l,m,board[l][m])
                pieceCounter = m + l * 8
            else:
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        will[pieceCounter] = path
                    else:
                        bill[pieceCounter]=path
                break
        else:
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
            break
        l += 1
        m -= 1

    return lmoves

def knight(i,j):
    global wcheck
    global bcheck
    global wl
    global bl
    global will
    global bill
    piece = board[i][j]
    lmoves = []

    l = i
    m = j

    l -= 2
    if l >= 0:
        m -= 1
        if m >= 0:
            if board[l][m] == ' ':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            elif board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            else:
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        m += 2
        if m < 8:
            if board[l][m] == ' ':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            elif board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            else:
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
    l += 4
    m = j
    if l < 8:
        m -= 1
        if m >= 0:
            if board[l][m] == ' ':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            elif board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            else:
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        m += 2
        if m < 8:
            if board[l][m] == ' ':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            elif board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            else:
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])

    m = j
    l = i

    m -= 2
    if m >= 0:
        l -= 1
        if l >= 0:
            if board[l][m] == ' ':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            elif board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            else:
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        l += 2
        if l < 8:
            if board[l][m] == ' ':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            elif board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            else:
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
    m += 4
    l = i
    if m < 8:
        l -= 1
        if l >= 0:
            if board[l][m] == ' ':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            elif board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            else:
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
        l += 2
        if l < 8:
            if board[l][m] == ' ':
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            elif board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
                if board[l][m].lower() == 'k':
                    if piece.islower():
                        if wcheck:
                            wl = []
                        else:
                            wcheck = True
                            wl.extend([[i,j]])
                    else:
                        if bcheck:
                            bl = []
                        else:
                            bcheck = True
                            bl.extend([[i,j]])
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])
            else:
                if piece.isupper():
                    wattack.append([l,m])
                else:
                    battack.append([l,m])

    return lmoves

def king(i,j):
    piece = board[i][j]
    lmoves = []

    l = i
    m = j

    l -= 1
    if l >= 0:
        if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
            if (piece.islower() and [l,m] not in wattack) or (piece.islower() == False and [l,m] not in battack):
                lmoves.append([l,m])
        if piece.isupper():
            wattack.append([l,m])
        else:
            battack.append([l,m])
        m -= 1
        if m >= 0:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                if (piece.islower() and [l,m] not in wattack) or (piece.islower() == False and [l,m] not in battack):
                    lmoves.append([l,m])
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
        m += 2
        if m < 8:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                if (piece.islower() and [l,m] not in wattack) or (piece.islower() == False and [l,m] not in battack):
                    lmoves.append([l,m])
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])

    l += 1
    m = j

    m -= 1
    if m >= 0:
        if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
            if (piece.islower() and [l,m] not in wattack) or (piece.islower() == False and [l,m] not in battack):
                lmoves.append([l,m])
        if piece.isupper():
            wattack.append([l,m])
        else:
            battack.append([l,m])
    m += 2
    if m < 8:
        if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
            if (piece.islower() and [l,m] not in wattack) or (piece.islower() == False and [l,m] not in battack):
                    lmoves.append([l,m])
        if piece.isupper():
            wattack.append([l,m])
        else:
            battack.append([l,m])

    l = i
    m = j

    l += 1
    if l < 8:
        if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
            if (piece.islower() and [l,m] not in wattack) or (piece.islower() == False and [l,m] not in battack):
                lmoves.append([l,m])
        if piece.isupper():
            wattack.append([l,m])
        else:
            battack.append([l,m])
        m -= 1
        if m >= 0:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                if (piece.islower() and [l,m] not in wattack) or (piece.islower() == False and [l,m] not in battack):
                    lmoves.append([l,m])
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
        m += 2
        if m < 8:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                if (piece.islower() and [l,m] not in wattack) or (piece.islower() == False and [l,m] not in battack):
                    lmoves.append([l,m])
            if piece.isupper():
                wattack.append([l,m])
            else:
                battack.append([l,m])
    if piece.islower(): 
        if canCastle['bk'] == 'yes' and board[i][j+1] == ' ' and board[i][j+2] == ' ' and [i,j+1] not in wattack and [i,j+2] not in wattack:
            lmoves.append([i,j+2])
        if canCastle['bq'] == 'yes' and board[i][j-1] == ' ' and board[i][j-2] == ' ' and board[i][j-3] == ' ' and [i,j-1] not in wattack and [i,j-2] not in wattack and [i,j-3] not in wattack:
            lmoves.append([i,j-2])
    else:
        if canCastle['wk'] == 'yes' and board[i][j+1] == ' ' and board[i][j+2] == ' ' and [i,j+1] not in battack and [i,j+2] not in battack:
            lmoves.append([i,j+2])
        if canCastle['wq'] == 'yes' and board[i][j-1] == ' ' and board[i][j-2] == ' ' and board[i][j-3] == ' ' and [i,j-1] not in wattack and [i,j-2] not in wattack and [i,j-3] not in wattack:
            lmoves.append([i,j-2])
    return lmoves

def moveMaker(n,i,j,x,y,prom,cas):
    if prom != n:
        return marking[j] + str(8 - i) + n + marking[y] + str(8 - x) + prom
    if cas:
        return marking[j] + str(8 - i) + n + marking[y] + str(8 - x) + 'r' + str(j)
    return marking[j] + str(8 - i) + n + marking[y] + str(8 - x)

def undoMove(i,j,x,y,bij,remvp,move,cl,dept):
    global hashing
    global points
    if board[x][y].lower() == 'r':
        if board[x][y].islower():
            if j == 0:
                if canCastle['bq'] == dept:
                    canCastle['bq'] = 'yes'
            elif j == 7:
                if canCastle['bk'] == dept:
                    canCastle['bk'] = 'yes'
        else:
            if j == 0:
                if canCastle['wq'] == dept:
                    canCastle['wq'] = 'yes'
            elif j == 7:
                if canCastle['wk'] == dept:
                    canCastle['wk'] = 'yes'
    if board[x][y].lower() == 'k':
        if board[x][y].islower():
            if canCastle['bk'] == dept:
                canCastle['bk'] = 'yes'
            if canCastle['bq'] == dept:
                canCastle['bq'] = 'yes'
        else:
            if canCastle['wk'] == dept:
                canCastle['wk'] = 'yes'
            if canCastle['wq'] == dept:
                canCastle['wq'] = 'yes'
    if len(move) >= 5:
        staleMate[hashing] -= 1
        if staleMate[hashing] == 0:
            del staleMate[hashing]
    if remvp != ' ':
        if remvp.islower():
            bp[remvp].append([x,y])
        else:
            wp[remvp].append([x,y])
        hashing ^= zobrist[pos.index(remvp)][y + x * 8]
        points += pointDist[remvp]*mapper[remvp][x][y]
    if len(move) == 6 and move[2].lower() == 'p':
        if cl :
            board[i][j] = 'p'
        else:
            board[i][j] = 'P'
    else:
        board[i][j] = bij
    board[x][y] = remvp
    points -= pointDist[bij]*mapper[bij][x][y]
    points += pointDist[board[i][j]]*mapper[board[i][j]][i][j]
    hashing ^= zobrist[pos.index(board[i][j])][j + i * 8]
    hashing ^= zobrist[pos.index(bij)][y + x * 8]
    if board[i][j].islower():
        bp[board[i][j]].append([i,j])
        bp[bij].remove([x,y])
    else:
        wp[board[i][j]].append([i,j])
        wp[bij].remove([x,y])
    if len(move) == 7:
            jr = 0
            yr = 3
            if y > j:
                jr = 7
                yr = 5
            remvi = ' '
            undoMove(i,jr,x,yr,board[i][yr],remvi,'',cl,dept)

def makeMove(i,j,x,y,bij,remvp):
    global hashing
    global points

    # print(i,j,board[i][j],bij,remvp,bp,wp)

    if remvp != ' ':
        if remvp.islower():
            bp[remvp].remove([x,y])
        else:
            wp[remvp].remove([x,y])
        hashing ^= zobrist[pos.index(remvp)][y + x * 8]
        points -= pointDist[remvp]*mapper[remvp][x][y]
        
    if board[i][j].islower():
        bp[board[i][j]].remove([i,j])
        bp[bij].append([x,y])
    else:
        wp[board[i][j]].remove([i,j])
        wp[bij].append([x,y])
    hashing ^= zobrist[pos.index(board[i][j])][j + i * 8]
    hashing ^= zobrist[pos.index(bij)][y + x * 8]
    points += pointDist[bij]*mapper[bij][x][y]
    points -= pointDist[board[i][j]]*mapper[board[i][j]][i][j]
    board[x][y] = bij
    board[i][j] = ' '

def preprocess(cl):
    global wattack
    global battack
    global wl
    global bl
    global bill
    global will
    global bcheck
    global wcheck
    if cl:
        battack = []
        will = {}
        wl = []
        wcheck = False
    else:
        bill = {}
        wattack = []
        bl = []
        bcheck = False
    if cl:
        it = copy.deepcopy(bp)
    else:
        it = copy.deepcopy(wp)
    # print(it)
    for key,val in it.items():
        for pos in val:
            i = pos[0]
            j = pos[1]
            if key.lower() == 'p':
                pawn(i,j)
            elif key.lower() == 'r':
                straight(i,j)
            elif key.lower() == 'b':
                diagnol(i,j)
            elif key.lower() == 'n':
                knight(i,j)
            elif key.lower() == 'k':
                king(i,j)
            elif key.lower() == 'q':
                diagnol(i,j) + straight(i,j)

def legalMoves(cl,check):
    global points
    global will
    global bill
    global wattack
    global battack
    global wl
    global bl
    global bcheck
    global wcheck
    lega = []
    preprocess(cl == False)
    if cl:
        it = copy.deepcopy(bp)
    else:
        it = copy.deepcopy(wp)
    # print(it)
    for key,val in it.items():
        for pos in val:
            i = pos[0]
            j = pos[1]
            if key.lower() == 'p':
                ls = pawn(i,j)
            elif key.lower() == 'r':
                ls = straight(i,j)
            elif key.lower() == 'b':
                ls = diagnol(i,j)
            elif key.lower() == 'n':
                ls = knight(i,j)
            elif key.lower() == 'k':
                ls = king(i,j)
            elif key.lower() == 'q':
                ls = diagnol(i,j) + straight(i,j)
            if (cl and j + i * 8 in bill):
                ind = 0
                while ind < len(ls):
                    if ls[ind] in bill[j + i * 8]:
                        ind += 1
                    else:
                        ls.pop(ind)
                # print(ls)
                # print(ls,bill,key,i,j)
            elif (cl == False and j + i * 8 in will):
                ind = 0
                while ind < len(ls):
                    if ls[ind] in will[j + i * 8]:
                        ind += 1
                    else:
                        ls.pop(ind)
            # if len(bill) > 0:
            #     print(bill)
            # if len(will) > 0:
            #     print(will)
                # print(ls,will,key,i,j)

            # print(ls)
            for k in ls:
                if (cl and bcheck and key.lower() != 'k'):
                    if k not in bl:
                        continue
                if (cl == False and wcheck and key.lower() != 'k'):
                    if k not in wl:
                        continue
                iterSequence = key
                gon = board[k[0]][k[1]]
                if key == 'p' and i == 6:
                    iterSequence = 'nbqr'
                elif key == 'P' and i == 1:
                    iterSequence = 'NBQR'
                # print(iterSequence)
                for it in iterSequence:
                    castle = False
                    points -= pointDist[board[i][j]]*mapper[board[i][j]][i][j]
                    points += pointDist[it]*mapper[it][k[0]][k[1]]
                    if key.lower() == 'k':
                        if abs(k[1] - j) == 2:
                            castle = True
                    if gon != ' ':
                        points -= pointDist[gon]*mapper[gon][k[0]][k[1]]
                    lega.append((moveMaker(board[i][j],i,j,k[0],k[1],it,castle),points))
                    points += pointDist[board[i][j]]*mapper[board[i][j]][i][j]
                    points -= pointDist[it]*mapper[it][k[0]][k[1]]
                    if gon != ' ':
                        points += pointDist[gon]*mapper[gon][k[0]][k[1]]
    if cl:
        lega.sort(key=lambda x:x[1])
        # print(lega)
    else:
        lega.sort(key=lambda x:x[1],reverse=True)
        # print(cl,bp,wp)
    return lega

# def playMove(move):
    # print(move,move[0])
    j = marking.index(move[0])
    y = marking.index(move[3])
    i = 8 - int(move[1])
    x = 8 - int(move[4])
    remvp = board[x][y]
    if remvp != ' ':
        if remvp.islower():
            bp[remvp].remove([x,y])
        else:
            wp[remvp].remove([x,y])
    if board[i][j].islower():
        bp[board[i][j]].remove([i,j])
        bp[board[i][j]].append([x,y])
    else:
        wp[board[i][j]].remove([i,j])
        wp[board[i][j]].append([x,y])
    
    board[x][y] = board[i][j]
    board[i][j] = ' '

def compute(cl,depth,curv,leg):
    global hashing
    global points
    if hashing in transPositionMap and transPositionMap[hashing]['depth'] >= depth:
        if cl == False:
            rs = transPositionMap[hashing]['score'][1]
            rm = transPositionMap[hashing]['move'][1]
        else:
            rs = transPositionMap[hashing]['score'][0]
            rm = transPositionMap[hashing]['move'][0]
        return [rs,rm]
    mn = 'nope'
    mnm = ''
    mx = 'nope'
    mxm = ''
    iterList = leg
    # print(iterList)
    for z in iterList:
        r = 'WOWW'
        move = z[0]
        # print(z)
        j = numberMap[move[0]]
        y = numberMap[move[3]]
        i = 8 - int(move[1])
        x = 8 - int(move[4])
        remvp = str(board[x][y])
        bij = move[2]
        if len(move) == 6:
            bij = move[5]
        if board[i][j].lower() == 'r':
            if board[i][j].islower():
                if j == 0:
                    if canCastle['bq'] == 'yes':
                        canCastle['bq'] = depth
                elif j == 7:
                    if canCastle['bk'] == 'yes':
                        canCastle['bk'] = depth
            else:
                if j == 0:
                    if canCastle['wq'] == 'yes':
                        canCastle['wq'] = depth
                elif j == 7:
                    if canCastle['wk'] == 'yes':
                        canCastle['wk'] = depth
        if board[i][j].lower() == 'k':
            if board[i][j].islower():
                # print(canCastle, 'check pannunga')
                if canCastle['bk'] == 'yes':
                    canCastle['bk'] = depth
                if canCastle['bq'] == 'yes':
                    canCastle['bq'] = depth
            else:
                if canCastle['wk'] == 'yes':
                    canCastle['wk'] = depth
                if canCastle['wq'] == 'yes':
                    canCastle['wq'] = depth
        makeMove(i,j,x,y,bij,remvp)
        if len(move) == 7:
            jr = 0
            yr = 3
            if y > j:
                jr = 7
                yr = 5
            remvp = ' '
            makeMove(i,jr,x,yr,board[i][jr],remvp)
            # print(canCastle,i,j,board)
        # print(move,bij,wp)
        # print(max(staleMate.values()))
        if hashing in staleMate:
            staleMate[hashing] += 1
            if staleMate[hashing] >= 3:
                undoMove(i,j,x,y,bij,remvp,move,cl,depth)
                return [0,move]
        else:
            staleMate[hashing] = 1
        if depth != 0:
            cur = 'init'
            if cl == False and mx != 'nope':
                cur = mx
            elif cl != False and mn != 'nope':
                cur = mn
            legIter = legalMoves(cl == False,False)
            r = compute(cl == False, depth - 1,cur,legIter)
            
            # print(r)
            if r != 'nope' and r[0] != 'nope' and r != 'WOWW':
                r = r[0]
            else:
                undoMove(i,j,x,y,bij,remvp,move,cl,depth)
                continue
        else:
            r = points
                # print(move)
        if curv != 'init':
            if cl == False:
                if r > curv:
                    undoMove(i,j,x,y,bij,remvp,move,cl,depth)
                    return 'nope'
            else:
                if r < curv:
                    undoMove(i,j,x,y,bij,remvp,move,cl,depth)
                    return 'nope'
        undoMove(i,j,x,y,bij,remvp,move,cl,depth)
        if mn == 'nope':
            mn = r
            mnm = move
        else:
            mn = min(mn,r)
            if r == mn:
                mnm = move
        if mx == 'nope':
            mx = r
            mxm = move
        else:
            mx = max(mx,r)
            if r == mx:
                mxm = move
        # print(r,move)
    if len(leg) == 0:
            # print('mhm',cl,bp,wp,depth)
        if cl == False:
            if wcheck:
                return [-10000*(depth + 1),'10']
            return [0,'10']
        else:
            if bcheck:
                return [10000*(depth + 1),'10']
            return [0,'10']
    transPositionMap[hashing] = {'depth':depth,'move':[mnm,mxm],'score':[mn,mx]}
    if cl == False:
        return [mx,mxm]
    return [mn,mnm]