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
'k':[[1.1,1.1,1.05,1,1,1.05,1.1,1.1],
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
    [1.1,1.1,1.05,1,1,1.05,1.1,1.1]
]}

marking = 'abcdefgh'
board = []
points = 0
inCheck = False
counter = 0
bp = {}
wp = {}
pointDist = {'p':-1,'r':-5,'b':-3.2,'n':-3,'q':-9,'k':-1,'P':1,'R':5,'B':3.2,'N':3,'Q':9,'K':1}

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
    # if hashing in staleMate:
    #     staleMate[hashing] += 1
    # print(fen)
    if colour == 'true':
        chance = True
    else:
        chance = False
    leg = legalMoves(chance,False)
    # print(leg)
    res = compute(chance,3,'init',leg)
    move = res[1]
    # print(move,res)
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

    return lmoves

def moveMaker(n,i,j,x,y,prom):
    if prom != n:
        return marking[j] + str(8 - i) + n + marking[y] + str(8 - x) + prom
    return marking[j] + str(8 - i) + n + marking[y] + str(8 - x)

def undoMove(i,j,x,y,bij,remvp,move,cl):
    global hashing
    global points
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
    if len(move) == 6:
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

def legalMoves(cl,check):
    global inCheck
    global points
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
                iterSequence = key
                if key == 'p' and i == 6:
                    iterSequence = 'nbqr'
                elif key == 'P' and i == 1:
                    iterSequence = 'NBQR'
                # print(iterSequence)
                for it in iterSequence:
                    points -= pointDist[board[i][j]]*mapper[board[i][j]][i][j]
                    points += pointDist[it]*mapper[it][k[0]][k[1]]
                    if board[k[0]][k[1]] != ' ':
                        points -= pointDist[board[k[0]][k[1]]]*mapper[board[k[0]][k[1]]][k[0]][k[1]]
                    lega.append((moveMaker(board[i][j],i,j,k[0],k[1],it),points))
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
        # print(move,bij,wp)
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
        board[x][y] = str(bij)
        board[i][j] = ' '
        # print(max(staleMate.values()))
        if hashing in staleMate:
            staleMate[hashing] += 1
            if staleMate[hashing] >= 3:
                undoMove(i,j,x,y,bij,remvp,move,cl)
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
                undoMove(i,j,x,y,bij,remvp,move,cl)
                continue
        else:
            if legalMoves(cl == False,False) != 'Illegal':
                r = points
                checkMate = False
                # print(move)
            else:
                undoMove(i,j,x,y,bij,remvp,move,cl)
                continue
        if curv != 'init':
            if cl == False:
                if r > curv:
                    undoMove(i,j,x,y,bij,remvp,move,cl)
                    return 'nope'
            else:
                if r < curv:
                    undoMove(i,j,x,y,bij,remvp,move,cl)
                    return 'nope'
        undoMove(i,j,x,y,bij,remvp,move,cl)
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