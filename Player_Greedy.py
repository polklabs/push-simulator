from Player import Player
from Card import Card
import random

class PlayerGreedy(Player):
    name = 'Greedy'
    
    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        return True
    
    # Return true to draw
    def DrawOrCall(self, nextData: dict, returnData: list):
        if nextData['BUST'] < 30:
            return True
        return False
    
    def PlaceInStack(self, card: Card, stacks: list[Card], stackIds: list[int], nextData: dict, returnData: list):
        if card.type == 'num':
            return stackIds[0]
        return stackIds[-1]
    
    def TakeStack(self, stackIds: list[int], nextData: dict, returnData: list):
        maxPoints = 0
        maxPointIndex = 0
        for i in range(len(returnData[:-1])):
            if returnData[i]['max'] > maxPoints:
                maxPoints = returnData[i]['max']
                maxPointIndex = i
        if maxPointIndex in stackIds:
            return maxPointIndex
        return stackIds[0]