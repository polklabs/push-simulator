from Player import Player
from Card import Card
import random

class PlayerScared(Player):
    name = 'Scared'

    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        return True
    
    # Return true to draw
    def DrawOrCall(self, stacks: list[Card], nextData: dict, returnData: list):
        if nextData['BUST'] > 0:
            return False
        
        rollCards = 0
        for s in stacks[1:]:
            rollCards += len([c for c in s if c.type == 'roll'])
        if rollCards >= (len(stacks)-1) and nextData['ROLL'] > 0:
            return False

        return True
    
    def PlaceInStack(self, card: Card, stacks: list[Card], stackIds: list[int], nextData: dict, returnData: list):
        indexed_data = list(enumerate(returnData[:-1]))
        sorted_data = sorted(indexed_data, key=lambda x: x[1]['min'], reverse=True)
        sorted_indexes = [index for index, _ in sorted_data]

        if card.type == 'num':
            for i in sorted_indexes:
                if i in stackIds:
                    return i
        sorted_indexes.reverse()
        for i in sorted_indexes:
            if i in stackIds:
                return i
        return stackIds[0]
    
    def TakeStack(self, stackIds: list[int], nextData: dict, returnData: list):
        # Take stack with highest guaranteed points
        indexed_data = list(enumerate(returnData[:-1]))
        sorted_data = sorted(indexed_data, key=lambda x: x[1]['min'], reverse=True)
        sorted_indexes = [index for index, _ in sorted_data]

        for i in sorted_indexes:
            if i in stackIds:
                return i
        return stackIds[0]