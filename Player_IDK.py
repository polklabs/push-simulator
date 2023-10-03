class PlayerIDK:
    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        return True
    
    # Return true to draw
    def DrawOrCall(self, nextData: dict, returnData: list):
        return True
    
    def PlaceInStack(self, stacksIds: list[int], nextData: dict, returnData: list):
        return stacksIds[0]
    
    def TakeStack(self, stackIds: list[int], nextData: dict, returnData: list):
        return stackIds[0]