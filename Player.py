from Card import Card

class Player:
    name = 'Player'

    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        raise Exception("NotImplementedException")
    
    # Return true to draw
    def DrawOrCall(self, stacks: list[Card], nextData: dict, returnData: list):
        raise Exception("NotImplementedException")
    
    def PlaceInStack(self, card: Card, stacks: list[Card], stackIds: list[int], nextData: dict, returnData: list):
        raise Exception("NotImplementedException")
    
    def TakeStack(self, stackIds: list[int], nextData: dict, returnData: list):
        raise Exception("NotImplementedException")
    
    def SleepTime(self, sleepType):
        if sleepType == 'draw_before':
            return 1
        if sleepType == 'draw_after':
            return 1
        if sleepType == 'placeStack_before':
            return 2
        if sleepType == 'pickStack_before':
            return 2.5
        if sleepType == 'pickStack_after':
            return 2.5