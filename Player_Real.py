from Player import Player
import inquirer

class PlayerReal(Player):
    # Return true to draw
    def DrawOrBank(self, nextData: dict, returnData: list):
        questions = [
        inquirer.List('draw',
                        message="Draw Card or Bank Points?",
                        choices=['Draw', 'Bank'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        return answers['draw'] == 'Draw'
    
    # Return true to draw
    def DrawOrCall(self, nextData: dict, returnData: list):
        questions = [
        inquirer.List('draw',
                        message="Draw Card or Call?",
                        choices=['Draw', 'Call'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        return answers['draw'] == 'Draw'
    
    def PlaceInStack(self, stackIds: list[int], nextData: dict, returnData: list):
        choices = []
        for i in stackIds:
            choices.append(i+1)
        questions = [
        inquirer.List('place',
                        message="Place card in stack?",
                        choices=choices,
                    ),
        ]
        answers = inquirer.prompt(questions)
        return answers['place']-1
    
    def TakeStack(self, stackIds: list[int], nextData: dict, returnData: list):
        choices = []
        for i in stackIds:
            choices.append(i+1)
        questions = [
        inquirer.List('place',
                        message="Take Stack?",
                        choices=choices,
                    ),
        ]
        answers = inquirer.prompt(questions)
        return answers['place']-1

    def SleepTime(self, sleepType):
        return 0