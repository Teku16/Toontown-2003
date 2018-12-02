from ShowBaseGlobal import *
import PandaObject, AvatarDNA, StateData
from DirectGui import *
import Localizer

class GenderShop(PandaObject.PandaObject, StateData.StateData):
    __module__ = __name__

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.shopsVisited = []
        self.toon = None
        self.gender = 'm'
        return
        return

    def enter(self):
        base.disableMouse()
        return None
        return

    def showButtons(self):
        return None
        return

    def exit(self):
        return None
        return

    def load(self):
        return

    def unload(self):
        return

    def setGender(self, choice):
        self.__setGender(choice)

    def __setGender(self, choice):
        if choice == -1:
            self.gender = 'm'
        else:
            self.gender = 'f'
        messenger.send(self.doneEvent)