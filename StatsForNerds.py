from Consts import COLOR_NAME, COLORS

def chanceToBust(board):
    if len(board.deck) == 0:
        return 0

    smallestStack = min([len(x) for x in board.stacks])
    # smallestStack = min(len(board.stacks[0]),len(board.stacks[1]),len(board.stacks[2]))
    if smallestStack == 0:
        return 0
    
    toBust = 0
    for c in board.deck:
        for i in range(4):
            if i<3 and board.canPlaceInStack(i, c):
                break
        if i == 3:
            # print(c.color, c.number, bcolors.ENDC)
            toBust += 1

    return round((toBust/len(board.deck))*100, 2)

def calculateNextCardStats(board):
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

# Calculates the expected return value of every stack
def calculateReturnPointStats(board, playerNum: int):
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