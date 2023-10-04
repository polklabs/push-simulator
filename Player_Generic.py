from Player import Player
from Card import Card

class PlayerGeneric(Player):
    name = 'Generic'

    # bustBreak: At what percent chance of the next card to bust should the AI give up
    # takeStack: 'min' | 'avg' | 'max' which value to use to grab stack by
    # splitValue: this value and lower cards will be ignored and 'given' to other players
    def __init__(self, bustBreak:int=10, takeStack:str='min', splitValue:int=2):
        self.bustBreak = bustBreak
        self.takeStack = takeStack
        self.splitValue = splitValue

    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        return True
    
    # Return true to draw
    def DrawOrCall(self, stacks: list[Card], nextData: dict, returnData: list):
        if nextData['BUST'] > self.bustBreak:
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

        if card.type == 'num' and card.number > self.splitValue:
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
        sorted_data = sorted(indexed_data, key=lambda x: x[1][self.takeStack], reverse=True)
        sorted_indexes = [index for index, _ in sorted_data]

        for i in sorted_indexes:
            if i in stackIds:
                return i
        return stackIds[0]