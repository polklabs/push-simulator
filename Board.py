from Bench import Bench
from Card import Card
from Consts import bcolors, COLORS, COLOR_NAME
from StatsForNerds import calculateNextCardStats, calculateReturnPointStats
from Player import Player
from Player_IDK import PlayerIDK
from Player_Random import PlayerRandom
from Player_Greedy import PlayerGreedy
from Player_Real import PlayerReal
from Player_Scared import PlayerScared
import random

class Board:
    def __init__(self, players=3):
        self.stacks: list[list[Card]] = [[],[],[]]
        self.reverse: bool = False
        self.deck: list[Card] = self.buildDeck()
        self.discard: list[Card] = []
        self.events: list[str] = []

        self.pTurn: int = 0
        self.players: int = players
        self.playerAI: list[Player] = []
        self.playerInfo: list[Bench] = []
        self.playerStackReturnStats = []
        for i in range(players):
            self.playerInfo.append(Bench())
            self.playerStackReturnStats.append(calculateReturnPointStats(self, i))
        self.playerAI = [PlayerGreedy(), PlayerScared(), PlayerRandom()]

        self.resetRound()

    def getReturnStats(self, playerNum:int=None):
        if playerNum == None:
            playerNum = self.pTurn
        return self.playerStackReturnStats[playerNum]

    def resetRound(self):
        self.stacks: list[list[Card]] = [[],[],[]]
        self.reverse: bool = False
        self.nextCardStats = calculateNextCardStats(self)
        for i in range(self.players):
            self.playerStackReturnStats.append(calculateReturnPointStats(self, i))

    def rollDie(self):
        return random.choice(['Purple', 'Blue', 'Green', 'Yellow', 'Red', 'None'])
    
    def addEvent(self, event: str):
        self.events.insert(0,'> ' + event)

    def drawCard(self):
        if len(self.deck) == 0:
            return None
        toReturn = self.deck[0]
        self.deck.remove(toReturn)
        self.discard.append(toReturn)
        self.nextCardStats = calculateNextCardStats(self)
        return toReturn
    
    def canPlaceInStack(self, stackIndex, card):
        if stackIndex >= 3:
            return None
        matches = [c for c in self.stacks[stackIndex] if c.match(card)]
        return len(matches) == 0

    def placeStack(self, card: Card, index: int):
        if index > 2:
            return
        self.stacks[index].append(card)
        self.nextCardStats = calculateNextCardStats(self)
        for i in range(self.players):
            self.playerStackReturnStats[i] = calculateReturnPointStats(self, i)

    def ApplyStack(self, stackIndex: int, playerNum: int):
        points = self.playerInfo[playerNum].points
        newPoints = 0
        hasRollCard = False
        for card in self.stacks[stackIndex]:
            if card.type == 'num':
                points[COLORS.index(card.color)] += card.number
                newPoints += card.number
            elif card.type == 'roll':
                hasRollCard = True
        if hasRollCard == True:
            color = self.rollDie()
            if color != 'None':
                colorIndex = COLOR_NAME.index(color)
                newPoints -= points[colorIndex]
                self.addEvent(f'Player {playerNum+1}: Rolled {COLORS[colorIndex]}{color}{bcolors.ENDC}, {-points[colorIndex]} Points')
                points[colorIndex] = 0
            else:
                self.addEvent(f'Player {playerNum+1}: Rolled {color}, -0 Points')
        self.stacks[stackIndex] = []
        for i in range(self.players):
            self.playerStackReturnStats[i] = calculateReturnPointStats(self, i)
        return newPoints

    def getPlayerScore(self, i: int, colorIndex:int=-1):
        if i >= self.players:
            return 0
        if colorIndex == -1:
            return sum(self.playerInfo[i].points)
        else:
            return self.playerInfo[i].points[colorIndex]
        
    def buildDeck(self):
        deck = []
        for i in range(1, 7):
            for j in range(3):
                deck.append(Card(bcolors.GREEN, i))
                deck.append(Card(bcolors.YELLOW, i))
                deck.append(Card(bcolors.RED, i))
                deck.append(Card(bcolors.BLUE, i))
                deck.append(Card(bcolors.PURPLE, i))
        for i in range(18):
            deck.append(Card(cardType='roll'))
        for i in range(12):
            deck.append(Card(cardType='switch'))
        random.shuffle(deck)
        return deck