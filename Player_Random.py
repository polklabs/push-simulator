from Player import Player
from Card import Card
import random

class PlayerRandom(Player):
    name = 'Random'

    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        return True
    
    # Return true to draw
    def DrawOrCall(self, nextData: dict, returnData: list):
        return random.choice([True, False])
    
    def PlaceInStack(self, card: Card, stacks: list[Card], stackIds: list[int], nextData: dict, returnData: list):
        return random.choice(stackIds)
    
    def TakeStack(self, stackIds: list[int], nextData: dict, returnData: list):
        return random.choice(stackIds)