from ShowBaseGlobal import *
from DirectGui import *

class PatternPad(DirectFrame):
    __module__ = __name__
    ButtonNames = (
     'upButton', 'rightButton', 'downButton', 'leftButton')
    buttonNormalScale = 1.0
    buttonPressScale = 1.1
    buttonNormalColor = Point4(1, 1, 1, 1)
    buttonDisabledColor = Point4(0.7, 0.7, 0.7, 1)

    def __init__(self, parent=aspect2d, **kw):
        self.__pressHandlers = (
         lambda db, self=self: self.__pressButton(0),
         lambda db, self=self: self.__pressButton(1),
         lambda db, self=self: self.__pressButton(2),
         lambda db, self=self: self.__pressButton(3))
        self.__releaseHandlers = (
         lambda db, self=self: self.__releaseButton(0),
         lambda db, self=self: self.__releaseButton(1),
         lambda db, self=self: self.__releaseButton(2),
         lambda db, self=self: self.__releaseButton(3))
        self.__enterHandlers = (
         lambda db, self=self: self.__enterButton(0),
         lambda db, self=self: self.__enterButton(1),
         lambda db, self=self: self.__enterButton(2),
         lambda db, self=self: self.__enterButton(3))
        self.__exitHandlers = (
         lambda db, self=self: self.__exitButton(0),
         lambda db, self=self: self.__exitButton(1),
         lambda db, self=self: self.__exitButton(2),
         lambda db, self=self: self.__exitButton(3))
        optiondefs = (
         (
          'callbacks', None, self.setCallbacks), ('pressHandlers', self.__pressHandlers, self.setPressHandlers), ('releaseHandlers', self.__releaseHandlers, self.setReleaseHandlers), ('enterHandlers', self.__enterHandlers, self.setEnterHandlers), ('exitHandlers', self.__exitHandlers, self.setExitHandlers), ('frameColor', (0, 0, 0, 0), None), ('buttons_clickSound', None, None), ('buttons_rolloverSound', None, None))
        self.defineoptions(kw, optiondefs, dynamicGroups=('buttons',))
        DirectFrame.__init__(self, parent)
        gui = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        self['geom'] = gui.find('**/pink_circle')
        bnames = (
         'trumpet', 'guitar', 'drums', 'piano')
        bpos = ((-0.005, 0, 0.305), (0.448, 0, 0.09), (0.029, 0, -0.348), (-0.419, 0, 0.043))
        for i in range(0, len(bnames)):
            buttonGeom = gui.find('**/' + bnames[i])
            buttonGeomRollover = gui.find('**/' + bnames[i] + '_rollover')
            buttonGeomPressed = buttonGeomRollover
            buttonGeomDisabled = buttonGeom
            self.createcomponent(self.ButtonNames[i], (), 'buttons', DirectButton, (), parent=self, pos=bpos[i], frameColor=(0, 0, 0, 0), pressEffect=0, image=(buttonGeom, buttonGeomPressed, buttonGeomRollover, buttonGeomDisabled), image3_color=self.buttonDisabledColor)

        buttonGeomDisabled.removeNode()
        gui.removeNode()
        self.initialiseoptions(PatternPad)
        self.setPressCallback(None)
        self.setReleaseCallback(None)
        self.setEnterCallback(None)
        self.setExitCallback(None)
        return

    def destroy(self):
        del self.__pressHandlers
        del self.__releaseHandlers
        del self.__enterHandlers
        del self.__exitHandlers
        self.setPressCallback(None)
        self.setReleaseCallback(None)
        self.setEnterCallback(None)
        self.setExitCallback(None)
        for name in self.ButtonNames:
            self.destroycomponent(name)

        DirectFrame.destroy(self)
        return

    def __getButtons(self):
        buttons = []
        for name in self.ButtonNames:
            buttons.append(self.component(name))

        return buttons

    def disable(self):
        buttons = self.__getButtons()
        for button in buttons:
            button['state'] = DISABLED

    def enable(self):
        buttons = self.__getButtons()
        for button in buttons:
            button['state'] = NORMAL

    def setPressCallback(self, callback):
        self.__clientPressCallback = callback

    def setReleaseCallback(self, callback):
        self.__clientReleaseCallback = callback

    def setEnterCallback(self, callback):
        self.__clientEnterCallback = callback

    def setExitCallback(self, callback):
        self.__clientExitCallback = callback

    def setCallbacks(self):
        buttons = self.__getButtons()
        if self['callbacks'] == None:
            for button in buttons:
                button['command'] = None

        for i in range(0, len(buttons)):
            buttons[i]['command'] = self['callbacks'][i]

        return

    def __bindButtonHandlers(self, event, handlerTypeName):
        buttons = self.__getButtons()
        if self[handlerTypeName] == None:
            for button in buttons:
                button.unbind(event)

        for i in range(0, len(buttons)):
            buttons[i].bind(event, self[handlerTypeName][i])

        return

    def setPressHandlers(self):
        self.__bindButtonHandlers(B1PRESS, 'pressHandlers')

    def setReleaseHandlers(self):
        self.__bindButtonHandlers(B1RELEASE, 'releaseHandlers')

    def setEnterHandlers(self):
        self.__bindButtonHandlers(ENTER, 'enterHandlers')

    def setExitHandlers(self):
        self.__bindButtonHandlers(EXIT, 'exitHandlers')

    def __pressButton(self, index):
        button = self.__getButtons()[index]
        button.setScale(self.buttonPressScale)
        if self.__clientPressCallback != None:
            self.__clientPressCallback(index)
        return

    def __releaseButton(self, index):
        button = self.__getButtons()[index]
        button.setScale(self.buttonNormalScale)
        if self.__clientReleaseCallback != None:
            self.__clientReleaseCallback(index)
        return

    def __enterButton(self, index):
        if self.__clientEnterCallback != None:
            self.__clientEnterCallback(index)
        return

    def __exitButton(self, index):
        if self.__clientExitCallback != None:
            self.__clientExitCallback(index)
        return

    def simButtonPress(self, index):
        button = self.__getButtons()[index]
        button.setScale(self.buttonPressScale)
        button.component('image3').setColor(self.buttonNormalColor)

    def simButtonRelease(self, index):
        button = self.__getButtons()[index]
        button.setScale(self.buttonNormalScale)
        button.component('image3').setColor(self.buttonDisabledColor)