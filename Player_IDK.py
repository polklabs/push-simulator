class PlayerIDK:
    # Return true to draw
    def DrawOrBank(self):
        return True
    
    # Return true to draw
    def DrawOrCall(self):
        return True
    
    def PlaceInStack(self, stacksIds: list[int]):
        return stacksIds[0]
    
    def TakeStack(self, stackIds: list[int]):
        return stackIds[0]