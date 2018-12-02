from DirectFrame import *

class DirectLabel(DirectFrame):
    __module__ = __name__

    def __init__(self, parent=aspect2d, **kw):
        optiondefs = (
         (
          'pgFunc', PGItem, None), ('numStates', 1, None), ('state', self.inactiveInitState, None), ('activeState', 0, self.setActiveState))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(DirectLabel)
        return

    def setActiveState(self):
        self.guiItem.setState(self['activeState'])