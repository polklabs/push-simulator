from prettytable import PrettyTable
import random, os, time

from Board import Board
from Bench import Bench
from Card import Card
from Consts import bcolors, COLORS, COLOR_NAME

def printCard(card: Card):
    lines = card.getCard()
    for line in lines:
        print(line)

def printStacks(board: Board):
    draw = Card.getCardBack(len(board.deck))
    empty = Card.getCardEmpty()
    reverse = Card(cardType='switch').getCard()
    cards = [[],[],[]]
    for i in range(3):
        cards[i] = list(map(lambda val: val.getCard(), board.stacks[i]))

    height = max(len(cards[0]), len(cards[1]), len(cards[2]))
    lines = max(5, 5 + (2*(height-1)))

    stackIndex = [0,0,0]

    for i in range(lines):
        if i != 0 and i % 2 == 0:
            for j in range(3):
                if len(cards[j]) > stackIndex[j]+1:
                    stackIndex[j] += 1

        if(i < len(draw)):
            print(draw[i], end="  ")
        else:
            print('       ', end="  ")

        for j in range(3):
            if len(cards[j])>0:
                if (i < (stackIndex[j]*2) + len(cards[j][stackIndex[j]])):
                    print(cards[j][stackIndex[j]][i-(stackIndex[j]*2)], end="  ")
                else:
                    print('       ', end="  ")
            else:
                if(i < len(empty)):
                    print(empty[i], end="  ")
                else:
                    print('       ', end="  ")

        if board.reverse == True:
            if(i < len(reverse)):
                print(reverse[i], end="  ")
            else:
                print('       ', end="  ")

        print()

def clearBoard():
    print(bcolors.ENDC)
    os.system('cls' if os.name == 'nt' else 'clear')

def drawBoard(board: Board, nextCard: Card=None, returnStats:dict=None, stats:dict=None):
    clearBoard()
    x = PrettyTable()
    columns = ['Points']
    for i in range(board.players):
        columns.append(f'Player {i+1}')
    x.field_names = columns
    
    for c in range(5):
        points = [f'{COLORS[c]}{COLOR_NAME[c]}{bcolors.ENDC}']
        for i in range(board.players):
            points.append(f'{COLORS[c]}{board.getPlayerScore(i, c)}{bcolors.ENDC}')
        x.add_row(points)
    points = [f'Total']
    for i in range(board.players):
        points.append(f'{board.getPlayerScore(i, -1)}')
    x.add_row(points)
    print(x)

    print(f'\nPlayer {board.pTurn+1}\'s Turn:')
    printStacks(board)

    if returnStats != None:
        printReturn(returnStats)

    if stats != None:
        printStats(stats)

    if nextCard != None:
        print('\nCard Drawn')
        printCard(nextCard)

def calculateStats(board: Board):
    dl = len(board.deck)
    data = dict()
    if dl == 0:
        data['SWITCH'] = 0
    else:
        alreadyDrawn = len([c for c in board.discard if c.type == 'switch'])
        data['SWITCH'] = round(((12-alreadyDrawn)/dl)*100,2)

    if dl == 0:
        data['ROLL'] = 0
    else:
        alreadyDrawn = len([c for c in board.discard if c.type == 'roll'])
        data['ROLL'] = round(((18-alreadyDrawn)/dl)*100,2)

    if dl == 0:
        data['NUM'] = 0
    else:
        alreadyDrawn = len([c for c in board.discard if c.type == 'num'])
        data['NUM'] = round(((90-alreadyDrawn)/dl)*100,2)

    for n in range(6):
        for c in range(len(COLORS)):
            if dl == 0:
                data[f'{n+1}_{COLOR_NAME[c]}'] = 0
            else:
                alreadyDrawn = len([card for card in board.discard if card.color == COLORS[c] and card.number == n+1])
                data[f'{n+1}_{COLOR_NAME[c]}'] = round(((3-alreadyDrawn)/dl)*100, 2)      

    data['BUST'] = chanceToBust(board)
    return data

def printStats(data):
    x = PrettyTable()
    x.field_names = ['%', '1', '2', '3', '4', '5', '6', 'Total']
    for c in range(len(COLORS)):
        r = [COLORS[c]+COLOR_NAME[c]]
        for n in range(6):
            r.append(data[f'{n+1}_{COLOR_NAME[c]}'])
        r.append(str(round(sum(r[1:]),2))+bcolors.ENDC)
        x.add_row(r)
    total = ['Total']
    transposed_matrix = zip(*x.rows)
    totalRows = [col for col in transposed_matrix]
    total += [round(sum(col),2) for col in totalRows[1:-1]] + [data['NUM']]
    x.add_row(total)
    x.add_row(['ROLL', data['ROLL']]+['']*6)
    x.add_row(['SWITCH', data['SWITCH']]+['']*6)
    x.add_row(['BUST', data['BUST']]+['']*6)
    print(x)

# Calculates the expected return value of every stack
def calculateReturn(board: Board, playerNum: int):
    data = [dict(), dict(), dict(), playerNum]
    for i in range(3):
        points = [p for p in board.playerInfo[playerNum].points]
        totalPoints = sum([p.number for p in board.stacks[i] if p.type == 'num'])
        for card in board.stacks[i]:
            if card.type == 'num':
                points[COLORS.index(card.color)] += card.number
        hasRollCard = len([c for c in board.stacks[i] if c.type == 'roll']) > 0
        if hasRollCard == True:
            maxPoints = max(points)

            t = 0
            for x in range(5):
                t += points[x]
            t = t/6
        else:
            maxPoints = 0
            t = 0

        data[i]['average'] = round(totalPoints - t,2)
        data[i]['min'] = totalPoints - maxPoints
        data[i]['max'] = totalPoints # Always totalPoints cause we're assuming I never get a bad roll
        # print(totalPoints)
    return data

def printReturn(stats):
    x = PrettyTable()
    x.field_names = [f'Player {stats[-1]+1}', 'Stack 1', 'Stack 2', 'Stack 3']
    x.add_row(['Min Gain']+ [s['min'] for s in stats[:-1]])
    x.add_row(['Avg Gain']+ [s['average'] for s in stats[:-1]])
    x.add_row(['Max Gain']+ [s['max'] for s in stats[:-1]])
    print(x)

def canPlaceInStack(board, stackIndex, card):
    if stackIndex >= 3:
        return None
    matches = [c for c in board.stacks[stackIndex] if c.match(card)]
    return len(matches) == 0

def chanceToBust(board: Board):
    if len(board.deck) == 0:
        return 0

    smallestStack = min([len(x) for x in board.stacks])
    # smallestStack = min(len(board.stacks[0]),len(board.stacks[1]),len(board.stacks[2]))
    if smallestStack == 0:
        return 0
    
    toBust = 0
    for c in board.deck:
        for i in range(4):
            if i<3 and canPlaceInStack(board, i, c):
                break
        if i == 3:
            # print(c.color, c.number, bcolors.ENDC)
            toBust += 1

    return round((toBust/len(board.deck))*100, 2)

def Draw(board: Board, ai):
    nextCard = board.drawCard()
    if nextCard == None:
        return False
    returnStats = calculateReturn(board, board.pTurn)
    stats = calculateStats(board)
    drawBoard(board, nextCard, returnStats=returnStats)
    print(f'\nPlayer {board.pTurn+1} is choosing a stack for card')
    time.sleep(2 * timescale)

    if nextCard.type == 'switch':
        board.reverse = not board.reverse
    else:
        availableStacks = []
        for i in range(3):
            if canPlaceInStack(board, i, nextCard):
                availableStacks.append(i)

        if len(availableStacks) == 0:
            returnStats = calculateReturn(board, board.pTurn)
            drawBoard(board, returnStats=returnStats)
            print('\nPushed Too Far: Busted')
            printCard(nextCard)
            return True
        
        stackIndex = ai.PlaceInStack(availableStacks, stats, returnStats)
        board.placeStack(nextCard, stackIndex)

    returnStats = calculateReturn(board, board.pTurn)
    stats = calculateStats(board)
    drawBoard(board, returnStats=returnStats, stats=stats)
    return False

def endgame(board: Board):
    topPlayer = 0
    topPoints = 0
    for i in range(board.players):
        pnts = board.getPlayerScore(i)
        if pnts > topPoints:
            topPlayer = i
            topPoints = pnts
    print(f'\n\nPlayer {topPlayer+1} WON with {topPoints} points!!!!')
    exit()

timescale = 0.05
board = Board()
turn = 0
while True:
    board.pTurn = turn % board.players
    ai = board.playerAI[board.pTurn]
    board.resetRound()
    returnStats = calculateReturn(board, board.pTurn)
    stats = calculateStats(board)
    drawBoard(board, returnStats=returnStats, stats=stats)

    busted = False
    if ai.DrawOrBank(stats, returnStats) == True:
        print(f'Player {board.pTurn+1} is drawing')
        time.sleep(2.5 * timescale)
        busted = Draw(board, ai)
        time.sleep(2.5 * timescale)
    else:
        print('TODO: Bank points')
        time.sleep(2.5 * timescale)

    while busted == False:
        returnStats = calculateReturn(board, board.pTurn)
        stats = calculateStats(board)
        drawBoard(board, returnStats=returnStats, stats=stats)
        if ai.DrawOrCall(stats, returnStats):
            print(f'Player {board.pTurn+1} is drawing')
            time.sleep(2.5 * timescale)
            busted = Draw(board, ai)
            time.sleep(2.5 * timescale)

            if len(board.deck) == 0:
                break
        else:
            break

    availableStacks = []
    for i in range(3):
        if len(board.stacks[i]) > 0:
            availableStacks.append(i)

    pickStrings = []
    if busted == False:
        returnStats = calculateReturn(board, board.pTurn)
        stats = calculateStats(board)
        drawBoard(board, returnStats=returnStats, stats=stats)
        print(f'Player {board.pTurn+1} is picking a stack')
        time.sleep(2.5 * timescale)
        stackIndex = ai.TakeStack(availableStacks, stats, returnStats)
        newPoints = board.ApplyStack(stackIndex, board.pTurn)
        availableStacks.remove(stackIndex)
        drawBoard(board, returnStats=returnStats, stats=stats)
        pickStrings.insert(0, f'Player {board.pTurn+1} took stack {stackIndex+1}: {newPoints} points')
        print('\n'.join(pickStrings))
        time.sleep(2.5 * timescale)

    otherPlayers = [(board.pTurn+1)%board.players, (board.pTurn+2)%board.players]
    if board.reverse == False:
        otherPlayers.reverse()
    
    for p in otherPlayers:
        if len(availableStacks) > 0:
            returnStats = calculateReturn(board, p)
            stats = calculateStats(board)
            drawBoard(board, returnStats=returnStats, stats=stats)
            print(f'Player {p+1} is picking a stack')
            print('\n'.join(pickStrings))
            time.sleep(2.5 * timescale)
            otherAI = board.playerAI[p]
            stackIndex = otherAI.TakeStack(availableStacks, stats, returnStats)
            newPoints = board.ApplyStack(stackIndex, p)
            availableStacks.remove(stackIndex)
            drawBoard(board, returnStats=returnStats, stats=stats)
            pickStrings.insert(0, f'Player {p+1} took stack {stackIndex+1}: {newPoints} points')
            print('\n'.join(pickStrings))
            time.sleep(2.5 * timescale)

    # input('Continue:')
    if len(board.deck) == 0:
        endgame(board)
    turn += 1
