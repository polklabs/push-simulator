from Player import Player
from Card import Card
import random

class PlayerGreedy(Player):
    name = 'Greedy'

    def __init__(self, bustBreak:int=25):
        self.bustBreak = bustBreak

    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        return True
    
    # Return true to draw
    def DrawOrCall(self, stacks: list[Card], nextData: dict, returnData: list):
        if nextData['BUST'] <= self.bustBreak:
            return True
        return False
    
    def PlaceInStack(self, card: Card, stacks: list[Card], stackIds: list[int], nextData: dict, returnData: list):
        if card.type == 'num':
            return stackIds[0]
        return stackIds[-1]
    
    def TakeStack(self, stackIds: list[int], nextData: dict, returnData: list):
        # Take stack with max possible points
        indexed_data = list(enumerate(returnData[:-1]))
        sorted_data = sorted(indexed_data, key=lambda x: x[1]['max'], reverse=True)
        sorted_indexes = [index for index, _ in sorted_data]

        for i in sorted_indexes:
            if i in stackIds:
                return i
        return stackIds[0]