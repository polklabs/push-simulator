from prettytable import PrettyTable
import os, time

from Board import Board
from Bench import Bench
from Card import Card
from Consts import bcolors, COLORS, COLOR_NAME

def sleep(type:str, ai):
    global timescale
    time.sleep(ai.SleepTime(type) * timescale)

def printCard(card: Card):
    lines = card.getCard()
    for line in lines:
        print(line)

def printStacks(board: Board, nextCard: Card):
    draw = Card.getCardBack()+[str(len(board.deck))+(' '*(7-len(str(len(board.deck)))))]
    empty = Card.getCardEmpty()
    reverse = Card(cardType='switch').getCard()+['Reverse']
    if nextCard != None:
        nextC = nextCard.getCard()+['Drawn Card']
    else:
        nextC = Card.getCardEmpty()+['Drawn Card']
    cards = [[],[],[]]
    for i in range(3):
        cards[i] = list(map(lambda val: val.getCard(), board.stacks[i]))

    height = max(len(cards[0]), len(cards[1]), len(cards[2]))
    lines = max(6, 5 + (2*(height-1)))

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

        if(board.reverse == True and i < len(reverse)):
            print(reverse[i], end="  ")
        else:
            print('       ', end="  ")

        if(i < len(nextC)):
            print(nextC[i], end="  ")
        else:
            print('       ', end="  ")

        print()

def clearBoard():
    print(bcolors.ENDC)
    os.system('cls' if os.name == 'nt' else 'clear')

def drawBoard(board: Board, playerTurn:int, nextCard: Card=None):
    clearBoard()
    x = PrettyTable()
    columns = ['Points']
    for i in range(board.players):
        if i == board.pTurn:
            columns.append(f'{bcolors.BOLD}{bcolors.UNDERLINE}Player {i+1}{bcolors.ENDC}')
        else:
            columns.append(f'Player {i+1}')
    x.field_names = columns

    x.add_row(['AI']+[x.name for x in board.playerAI])
    
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

    # print(f'\nPlayer {board.pTurn+1}\'s Turn:')
    printStacks(board, nextCard)

    printReturn(board.getReturnStats(playerTurn))
    printStats(board.nextCardStats)

    printEvents(board.events)

def printEvents(events: list[str]):
    x = PrettyTable(['Events'])
    x.align = "l"
    for row in events:
        x.add_row([row])
    print(x.get_string(end=10))

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
    x.add_row(['']*8)
    x.add_row(['ROLL', data['ROLL'], '', 'SWITCH', data['SWITCH'], '', 'BUST', data['BUST']])
    print(x)

def printReturn(stats):
    x = PrettyTable()
    x.field_names = [f'Player {stats[-1]+1}', 'Stack 1', 'Stack 2', 'Stack 3']
    x.add_row(['Min Gain']+ [s['min'] for s in stats[:-1]])
    x.add_row(['Avg Gain']+ [s['average'] for s in stats[:-1]])
    x.add_row(['Max Gain']+ [s['max'] for s in stats[:-1]])
    print(x)

def Draw(board: Board, ai):
    nextCard = board.drawCard()
    if nextCard == None:
        return False
    if nextCard.type == 'num':
        board.addEvent(f'Player {board.pTurn+1}: Choosing a stack for {nextCard.color}{nextCard.number}{bcolors.ENDC}')
    else:
        board.addEvent(f'Player {board.pTurn+1}: Choosing a stack for {nextCard.type}')
    drawBoard(board, board.pTurn, nextCard)
    sleep('placeStack_before', ai)

    if nextCard.type == 'switch':
        board.reverse = not board.reverse
    else:
        availableStacks = []
        for i in range(3):
            if board.canPlaceInStack(i, nextCard):
                availableStacks.append(i)

        if len(availableStacks) == 0:
            board.addEvent(f'Player {board.pTurn+1}: Pushed Too Far - Busted')
            drawBoard(board, board.pTurn, nextCard)
            return True
        
        stackIndex = ai.PlaceInStack(nextCard, board.stacks, availableStacks, board.nextCardStats, board.getReturnStats())
        board.placeStack(nextCard, stackIndex)

    drawBoard(board, board.pTurn)
    return False

def endgame(board: Board):
    topPlayer = 0
    topPoints = 0
    for i in range(board.players):
        pnts = board.getPlayerScore(i)
        if pnts > topPoints:
            topPlayer = i
            topPoints = pnts
    board.addEvent(f'Player {topPlayer+1}: WON with {topPoints} points!!!!')
    drawBoard(board, topPlayer)
    return board.playerAI[topPlayer].name

timescale = 1

def Game():
    board = Board()
    turn = 0
    while True:
        board.pTurn = turn % board.players
        ai = board.playerAI[board.pTurn]
        board.resetRound()
        board.addEvent(f'Player {board.pTurn+1}: Start Turn')
        drawBoard(board, board.pTurn)

        busted = False
        if ai.DrawOrBank(board.nextCardStats, board.getReturnStats()) == True:
            board.addEvent(f'Player {board.pTurn+1}: Drawing')
            drawBoard(board, board.pTurn)
            sleep('draw_before', ai)
            busted = Draw(board, ai)
            sleep('draw_after', ai)
        else:
            print('TODO: Bank points')
            time.sleep(2.5 * timescale)

        while busted == False:
            drawBoard(board, board.pTurn)
            maxStackLen = max([len(x) for x in board.stacks])
            if maxStackLen==0 or ai.DrawOrCall(board.nextCardStats, board.getReturnStats()):
                board.addEvent(f'Player {board.pTurn+1}: Drawing')
                drawBoard(board, board.pTurn)
                sleep('draw_before', ai)
                busted = Draw(board, ai)
                sleep('draw_after', ai)

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
            board.addEvent(f'Player {board.pTurn+1}: Picking a Stack')
            drawBoard(board, board.pTurn)
            sleep('pickStack_before', ai)
            stackIndex = ai.TakeStack(availableStacks, board.nextCardStats, board.getReturnStats())
            newPoints = board.ApplyStack(stackIndex, board.pTurn)
            availableStacks.remove(stackIndex)
            board.addEvent(f'Player {board.pTurn+1}: Took Stack {stackIndex+1}: {newPoints} Points')
            drawBoard(board, board.pTurn)
            sleep('pickStack_after', ai)

        otherPlayers = [(board.pTurn+1)%board.players, (board.pTurn+2)%board.players]
        if board.reverse == False:
            otherPlayers.reverse()
        
        for p in otherPlayers:
            if len(availableStacks) > 0:
                board.addEvent(f'Player {p+1}: Picking a Stack')
                drawBoard(board, p)
                otherAI = board.playerAI[p]
                sleep('pickStack_before', otherAI)
                stackIndex = otherAI.TakeStack(availableStacks, board.nextCardStats, board.getReturnStats(p))
                newPoints = board.ApplyStack(stackIndex, p)
                availableStacks.remove(stackIndex)
                board.addEvent(f'Player {p+1}: Took Stack {stackIndex+1}: {newPoints} Points')
                drawBoard(board, p)
                sleep('pickStack_after', otherAI)

        # input('Continue:')
        if len(board.deck) == 0:
            return endgame(board)
        turn += 1

def main():
    wins = dict()
    for i in range(10):
        winner = Game()
        if winner not in wins:
            wins[winner] = 0
        wins[winner] += 1

    table = PrettyTable()
    for c in wins.keys():
        table.add_column(c, [])
    table.add_row([wins[c] for c in wins.keys()])
    print(table)

main()