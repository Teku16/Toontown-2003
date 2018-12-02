from ShowBaseGlobal import *
from PandaObject import *

class ArrowKeys(PandaObject):
    __module__ = __name__
    UP_KEY = 'arrow_up'
    DOWN_KEY = 'arrow_down'
    LEFT_KEY = 'arrow_left'
    RIGHT_KEY = 'arrow_right'
    UP_INDEX = 0
    DOWN_INDEX = 1
    LEFT_INDEX = 2
    RIGHT_INDEX = 3
    NULL_HANDLERS = (
     None, None, None, None)

    def __init__(self):
        self.__upPressed = 0
        self.__downPressed = 0
        self.__leftPressed = 0
        self.__rightPressed = 0
        self.setPressHandlers(self.NULL_HANDLERS)
        self.setReleaseHandlers(self.NULL_HANDLERS)
        self.origMb = base.buttonThrower.node().getModifierButtons()
        base.buttonThrower.node().setModifierButtons(ModifierButtons())
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)

    def destroy(self):
        base.buttonThrower.node().setModifierButtons(self.origMb)
        events = [
         self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY]
        for event in events:
            self.ignore(event)
            self.ignore(event + '-up')

    def upPressed(self):
        return self.__upPressed

    def downPressed(self):
        return self.__downPressed

    def leftPressed(self):
        return self.__leftPressed

    def rightPressed(self):
        return self.__rightPressed

    def setPressHandlers(self, handlers):
        self.__checkCallbacks(handlers)
        self.__pressHandlers = handlers

    def setReleaseHandlers(self, handlers):
        self.__checkCallbacks(handlers)
        self.__releaseHandlers = handlers

    def clearPressHandlers(self):
        self.setPressHandlers(self.NULL_HANDLERS)

    def clearReleaseHandlers(self):
        self.setReleaseHandlers(self.NULL_HANDLERS)

    def __checkCallbacks(self, callbacks):
        for callback in callbacks:
            pass

    def __doCallback(self, callback):
        if callback:
            callback()

    def __upKeyPressed(self):
        self.ignore(self.UP_KEY)
        self.accept(self.UP_KEY + '-up', self.__upKeyReleased)
        self.__upPressed = 1
        self.__doCallback(self.__pressHandlers[self.UP_INDEX])

    def __downKeyPressed(self):
        self.ignore(self.DOWN_KEY)
        self.accept(self.DOWN_KEY + '-up', self.__downKeyReleased)
        self.__downPressed = 1
        self.__doCallback(self.__pressHandlers[self.DOWN_INDEX])

    def __leftKeyPressed(self):
        self.ignore(self.LEFT_KEY)
        self.accept(self.LEFT_KEY + '-up', self.__leftKeyReleased)
        self.__leftPressed = 1
        self.__doCallback(self.__pressHandlers[self.LEFT_INDEX])

    def __rightKeyPressed(self):
        self.ignore(self.RIGHT_KEY)
        self.accept(self.RIGHT_KEY + '-up', self.__rightKeyReleased)
        self.__rightPressed = 1
        self.__doCallback(self.__pressHandlers[self.RIGHT_INDEX])

    def __upKeyReleased(self):
        self.ignore(self.UP_KEY + '-up')
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.__upPressed = 0
        self.__doCallback(self.__releaseHandlers[self.UP_INDEX])

    def __downKeyReleased(self):
        self.ignore(self.DOWN_KEY + '-up')
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.__downPressed = 0
        self.__doCallback(self.__releaseHandlers[self.DOWN_INDEX])

    def __leftKeyReleased(self):
        self.ignore(self.LEFT_KEY + '-up')
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.__leftPressed = 0
        self.__doCallback(self.__releaseHandlers[self.LEFT_INDEX])

    def __rightKeyReleased(self):
        self.ignore(self.RIGHT_KEY + '-up')
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)
        self.__rightPressed = 0
        self.__doCallback(self.__releaseHandlers[self.RIGHT_INDEX])