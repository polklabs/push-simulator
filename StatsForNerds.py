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

    # Pre-calculate all cards the have been seen before
    drawnCards = {'switch': 0, 'roll': 0, 'num': 0}
    for n in range(6):
        for c in range(len(COLORS)):
            drawnCards[f'{n+1}_{COLOR_NAME[c]}'] = 0
    for c in board.discard:
        if c.type == 'switch':
            drawnCards['switch'] += 1
        elif c.type == 'roll':
            drawnCards['roll'] += 1
        else:
            drawnCards['num'] += 1
            key = f'{c.number}_{COLOR_NAME[COLORS.index(c.color)]}'
            drawnCards[key] += 1

    data = dict()
    if dl == 0:
        data['SWITCH'] = 0
    else:
        data['SWITCH'] = round(((12-drawnCards['switch'])/dl)*100,2)

    if dl == 0:
        data['ROLL'] = 0
    else:
        data['ROLL'] = round(((18-drawnCards['roll'])/dl)*100,2)

    if dl == 0:
        data['NUM'] = 0
    else:
        data['NUM'] = round(((90-drawnCards['num'])/dl)*100,2)

    for n in range(6):
        for c in range(len(COLORS)):
            key = f'{n+1}_{COLOR_NAME[c]}'
            if dl == 0:
                data[key] = 0
            else:
                data[key] = round(((3-drawnCards[key])/dl)*100, 2)      

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

        data[i]['avg'] = round(totalPoints - t,2)
        data[i]['min'] = totalPoints - maxPoints
        data[i]['max'] = totalPoints # Always totalPoints cause we're assuming I never get a bad roll
        # print(totalPoints)
    return data