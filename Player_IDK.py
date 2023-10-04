from Player import Player
from Card import Card

class PlayerIDK(Player):
    name = 'Dumb'

    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        return True
    
    # Return true to draw
    def DrawOrCall(self, stacks: list[Card], nextData: dict, returnData: list):
        return True
    
    def PlaceInStack(self, card: Card, stacks: list[Card], stackIds: list[int], nextData: dict, returnData: list):
        return stackIds[0]
    
    def TakeStack(self, stackIds: list[int], nextData: dict, returnData: list):
        return stackIds[0]