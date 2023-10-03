from Player import Player

class PlayerReal(Player):
    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        r = input('Draw[1: Default] or Bank[2]:').lower()
        if r in ['y', 'yes', '1', 'draw', '']:
            return True
        return False
    
    # Return true to draw
    def DrawOrCall(self, nextData: dict, returnData: list):
        r = input('Draw[1: Default] or Call[2]:').lower()
        if r in ['y', 'yes', '1', 'draw', '']:
            return True
        return False
    
    def PlaceInStack(self, stacksIds: list[int], nextData: dict, returnData: list):
        for i in stacksIds:
            print(f'Stack {i+1}[{i+1}]')
        while True:
            try:
                r = input('Choice:').lower()
                if int(r)-1 in stacksIds:
                    return int(r)-1
            except:
                print('Not valid')
    
    def TakeStack(self, stackIds: list[int], nextData: dict, returnData: list):
        for i in stackIds:
            print(f'Stack {i+1}[{i+1}]')
        while True:
            try:
                r = input('Choice:').lower()
                if int(r)-1 in stackIds:
                    return int(r)-1
            except:
                print('Not valid')

    def SleepTime(self, sleepType):
        return 0