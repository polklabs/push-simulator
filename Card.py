from Consts import bcolors

class Card:
    def __init__(self, color=bcolors.ENDC, number=1, cardType = 'num'):
        self.color: str = color
        self.number: int = number
        self.type: str = cardType

    def match(self, card):
        if self.type == 'roll' or card.type == 'roll':
            return self.type == card.type
        return self.color == card.color or self.number == card.number

    def getCard(self):
        if(self.type == 'num'):
            return [f'{self.color}+-----+{bcolors.ENDC}',
                    f'{self.color}|{self.number}    |{bcolors.ENDC}',
                    f'{self.color}|  {self.number}  |{bcolors.ENDC}',
                    f'{self.color}|    {self.number}|{bcolors.ENDC}',
                    f'{self.color}+-----+{bcolors.ENDC}' ]
        elif(self.type == 'switch'):
            return [f'{self.color}+-----+{bcolors.ENDC}',
                    f'{self.color}| ^   |{bcolors.ENDC}',
                    f'{self.color}| | | |{bcolors.ENDC}',
                    f'{self.color}| └-┘ |{bcolors.ENDC}',
                    f'{self.color}+-----+{bcolors.ENDC}' ]
        elif(self.type == 'roll'):
            return [f'{self.color}+-----+{bcolors.ENDC}',
                    f'{self.color}|◘    |{bcolors.ENDC}',
                    f'{self.color}|  ██ |{bcolors.ENDC}',
                    f'{self.color}|    ◘|{bcolors.ENDC}',
                    f'{self.color}+-----+{bcolors.ENDC}' ]
        
    def getCardBack():
        color = bcolors.ENDC
        return [f'{color}+-----+{bcolors.ENDC}',
                f'{color}| P   |{bcolors.ENDC}',
                f'{color}|  US |{bcolors.ENDC}',
                f'{color}|    H|{bcolors.ENDC}',
                f'{color}+-----+{bcolors.ENDC}' ]

    def getCardEmpty():
        color = bcolors.ENDC
        return [f'{color}+-----+{bcolors.ENDC}',
                f'{color}|     |{bcolors.ENDC}',
                f'{color}|     |{bcolors.ENDC}',
                f'{color}|     |{bcolors.ENDC}',
                f'{color}+-----+{bcolors.ENDC}' ]