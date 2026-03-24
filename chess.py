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

mapper = {'P':[[9,9,9,9,9,9,9,9],
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
    [9,9,9,9,9,9,9,9]
],
'n':[[0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8],
    [0.8,1,1,1,1,1,1,0.8],
    [0.8,1.05,1.05,1.05,1.05,1.05,1.05,0.8],
    [0.8,1.05,1.1,1.1,1.1,1.1,1.05,0.8],
    [0.8,1.05,1.1,1.1,1.1,1.1,1.05,0.8],
    [0.8,1.05,1.05,1.05,1.05,1.05,1.05,0.8],
    [0.8,1,1,1,1,1,1,0.8],
    [0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8]
],
'N':[[0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8],
    [0.8,1,1,1,1,1,1,0.8],
    [0.8,1.05,1.05,1.05,1.05,1.05,1.05,0.8],
    [0.8,1.05,1.1,1.1,1.1,1.1,1.05,0.8],
    [0.8,1.05,1.1,1.1,1.1,1.1,1.05,0.8],
    [0.8,1.05,1.05,1.05,1.05,1.05,1.05,0.8],
    [0.8,1,1,1,1,1,1,0.8],
    [0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8]
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
    [1,1.05,1.05,1.05,1.05,1.05,1.05,1],
    [1,1.05,1.1,1.1,1.1,1.1,1.05,1],
    [1,1.05,1.1,1.1,1.1,1.1,1.05,1],
    [1,1.05,1.05,1.05,1.05,1.05,1.05,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
],
'Q':[[1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1.05,1.05,1.05,1.05,1.05,1.05,1],
    [1,1.05,1.1,1.1,1.1,1.1,1.05,1],
    [1,1.05,1.1,1.1,1.1,1.1,1.05,1],
    [1,1.05,1.05,1.05,1.05,1.05,1.05,1],
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

marking = 'abcdefgh'
board = []
points = 0
inCheck = False
counter = 0
bp = {}
wp = {}
canCastle = {'wk':'yes','wq':'yes','bk':'yes','bq':'yes'}
drishti = {'b':False,'w':False}
pointDist = {'p':-1,'r':-5,'b':-3.2,'n':-3,'q':-9,'k':-1,'P':1,'R':5,'B':3.2,'N':3,'Q':9,'K':1}
drishti = {'bk':False,'bq':False,'wk':False,'wq':False}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        canCastle = {'wk':'yes','wq':'yes','bk':'yes','bq':'yes'}
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
    res = compute(chance,3,'init',leg)
    move = res[1]
    print(move,res)
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
    # print(res)
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
    board.append([])
    sqCount = 0
    for i in f:
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
                
def pawn(i,j):
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
        if p < 8 and board[k][p] != ' ' and board[k][p].islower() != piece.islower():
            lmoves.append([k,p])
        p = j - 1
        if p >= 0 and board[k][p] != ' ' and board[k][p].islower() != piece.islower():
            lmoves.append([k,p])
        if s > 0 and i == 1 and board[i + 1][j] == ' ' and board[i + 2][j] == ' ':
            lmoves.append([i+2,j])
        if s < 0 and i == 6 and board[i - 1][j] == ' ' and board[i - 2][j] == ' ':
            lmoves.append([i-2,j])
    return lmoves

def straight(i,j):
    lmoves = []
    piece = board[i][j]
    l = i - 1
    m = j
    while l >= 0:
        if board[l][m] == ' ':
            lmoves.append([l,m])
        elif board[l][m].islower() != piece.islower():
            lmoves.append([l,m])
            break
        else:
            break
        l -= 1
    l = i + 1
    m = j
    while l < 8:
        if board[l][m] == ' ':
            lmoves.append([l,m])
        elif board[l][m].islower() != piece.islower():
            lmoves.append([l,m])
            break
        else:
            break
        l += 1
    l = i
    m = j - 1
    while m >= 0:
        if board[l][m] == ' ':
            lmoves.append([l,m])
        elif board[l][m].islower() != piece.islower():
            lmoves.append([l,m])
            break
        else:
            break
        m -= 1
    l = i 
    m = j + 1
    while m < 8:
        if board[l][m] == ' ':
            lmoves.append([l,m])
        elif board[l][m].islower() != piece.islower():
            lmoves.append([l,m])
            break
        else:
            break
        m += 1
    return lmoves

def diagnol(i,j):
    piece = board[i][j]
    lmoves = []

    l = i - 1
    m = j - 1

    while l >= 0 and m >= 0:
        if board[l][m] == ' ':
            lmoves.append([l,m])
        elif board[l][m].islower() != piece.islower():
            lmoves.append([l,m])
            break
        else:
            break
        l -= 1
        m -= 1

    l = i - 1
    m = j + 1

    while l >= 0 and m < 8:
        if board[l][m] == ' ':
            lmoves.append([l,m])
        elif board[l][m].islower() != piece.islower():
            lmoves.append([l,m])
            break
        else:
            break
        l -= 1
        m += 1

    l = i + 1
    m = j + 1

    while l < 8 and m < 8:
        if board[l][m] == ' ':
            lmoves.append([l,m])
        elif board[l][m].islower() != piece.islower():
            lmoves.append([l,m])
            break
        else:
            break
        l += 1
        m += 1

    l = i + 1
    m = j - 1
    
    while l < 8 and m >= 0:
        if board[l][m] == ' ':
            lmoves.append([l,m])
        elif board[l][m].islower() != piece.islower():
            lmoves.append([l,m])
            break
        else:
            break
        l += 1
        m -= 1

    return lmoves

def knight(i,j):
    piece = board[i][j]
    lmoves = []

    l = i
    m = j

    l -= 2
    if l >= 0:
        m -= 1
        if m >= 0:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
        m += 2
        if m < 8:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
    l += 4
    m = j
    if l < 8:
        m -= 1
        if m >= 0:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
        m += 2
        if m < 8:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])

    m = j
    l = i

    m -= 2
    if m >= 0:
        l -= 1
        if l >= 0:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
        l += 2
        if l < 8:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
    m += 4
    l = i
    if m < 8:
        l -= 1
        if l >= 0:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
        l += 2
        if l < 8:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])

    return lmoves

def king(i,j):
    piece = board[i][j]
    lmoves = []

    l = i
    m = j

    l -= 1
    if l >= 0:
        if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
        m -= 1
        if m >= 0:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
        m += 2
        if m < 8:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])

    l += 1
    m = j

    m -= 1
    if m >= 0:
        if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
            lmoves.append([l,m])
    m += 2
    if m < 8:
        if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
            lmoves.append([l,m])

    l = i
    m = j

    l += 1
    if l < 8:
        if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
        m -= 1
        if m >= 0:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])
        m += 2
        if m < 8:
            if board[l][m] == ' ' or board[l][m].islower() != piece.islower():
                lmoves.append([l,m])

    if piece.islower(): 
        if canCastle['bk'] == 'yes' and board[i][j+1] == ' ' and board[i][j+2] == ' ' and drishti['bk'] == False:
            lmoves.append([i,j+2])
        if canCastle['bq'] == 'yes' and board[i][j-1] == ' ' and board[i][j-2] == ' ' and board[i][j-3] == ' ' and drishti['bq'] == False:
            lmoves.append([i,j-2])
    else:
        if canCastle['wk'] == 'yes' and board[i][j+1] == ' ' and board[i][j+2] == ' ' and drishti['wk'] == False:
            lmoves.append([i,j+2])
        if canCastle['wq'] == 'yes' and board[i][j-1] == ' ' and board[i][j-2] == ' ' and board[i][j-3] == ' ' and drishti['wq'] == False:
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
    if len(move) == 7 or len(move) == 0:
        print(board[i][j],board[x][y])
    if board[i][j].lower() == 'r':
        if board[i][j].islower():
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
    if board[i][j].lower() == 'k':
        if board[i][j].islower():
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
            print(i,jr,x,yr,board[i][jr])
            undoMove(i,jr,x,yr,board[i][yr],remvi,'',cl,dept)

def makeMove(i,j,x,y,bij,remvp):
    global hashing
    global points

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
    if bij == 'k' and abs(y-j) == 2:
        print(i,j,x,y,bij,remvp)
    hashing ^= zobrist[pos.index(board[i][j])][j + i * 8]
    hashing ^= zobrist[pos.index(bij)][y + x * 8]
    points += pointDist[bij]*mapper[bij][x][y]
    points -= pointDist[board[i][j]]*mapper[board[i][j]][i][j]
    board[x][y] = str(bij)
    board[i][j] = ' '

def legalMoves(cl,check):
    global inCheck
    global points
    global drishti
    if cl:
        drishti['wk'] = 'yes'
        drishti['wq'] = 'yes'
    else:
        drishti['bk'] = 'yes'
        drishti['bq'] = 'yes'
    lega = []
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
            # print(ls)
            for k in ls:
                if board[k[0]][k[1]].lower() == 'k': 
                    return 'Illegal'
                if k[0] == 0 and key.isupper():
                    if k[1] == 1 or k[1] == 2 or k[1] == 3 or k[1] == 4:
                        drishti['bq'] = True
                    if k[1] == 6 or k[1] == 5 or k[1] == 4:
                        drishti['bk'] = True
                if k[0] == 7 and key.islower():
                    if k[1] == 1 or k[1] == 2 or k[1] == 3 or k[1] == 4:
                        drishti['wq'] = True
                    if k[1] == 6 or k[1] == 5 or k[1] == 4:
                        drishti['wk'] = True
                iterSequence = key
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
                    if board[k[0]][k[1]] != ' ':
                        points -= pointDist[board[k[0]][k[1]]]*mapper[board[k[0]][k[1]]][k[0]][k[1]]
                    lega.append((moveMaker(board[i][j],i,j,k[0],k[1],it,castle),points))
                    points += pointDist[board[i][j]]*mapper[board[i][j]][i][j]
                    points -= pointDist[it]*mapper[it][k[0]][k[1]]
                    if board[k[0]][k[1]] != ' ':
                        points += pointDist[board[k[0]][k[1]]]*mapper[board[k[0]][k[1]]][k[0]][k[1]]
    if cl:
        lega.sort(key=lambda x:x[1])
        # print(lega)
    else:
        lega.sort(key=lambda x:x[1],reverse=True)
    # print(lega)
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
    global counter
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
    checkMate = True
    iterList = leg
    # print(iterList)
    for z in iterList:
        r = 'WOWW'
        counter += 1
        move = z[0]

        j = marking.index(move[0])
        y = marking.index(move[3])
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
            if legIter != 'Illegal':
                r = compute(cl == False, depth - 1,cur,legIter)
                checkMate = False
            
            # print(r)
            if r != 'nope' and r[0] != 'nope' and r != 'WOWW':
                r = r[0]
            else:
                undoMove(i,j,x,y,bij,remvp,move,cl,depth)
                continue
        else:
            if legalMoves(cl == False,False) != 'Illegal':
                r = points
                checkMate = False
                # print(move)
            else:
                undoMove(i,j,x,y,bij,remvp,move,cl,depth)
                continue
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
    if checkMate:
        if legalMoves(cl == False,False) == 'Illegal':
            # print('mhm',cl,bp,wp,depth)
            if cl == False:
                return [-10000*(depth + 1),'10']
            return [10000*(depth + 1),'10']
        if cl == False:
            return [0,'10']
        return [0,'10']
    transPositionMap[hashing] = {'depth':depth,'move':[mnm,mxm],'score':[mn,mx]}
    if cl == False:
        return [mx,mxm]
    return [mn,mnm]