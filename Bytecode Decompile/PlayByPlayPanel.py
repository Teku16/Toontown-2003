from DirectObject import *
from ShowBaseGlobal import *
from ToontownBattleGlobals import *
from ToontownGlobals import *
from SuitBattleGlobals import *
import DirectNotifyGlobal, OnscreenText

class PlayByPlayText(OnscreenText.OnscreenText):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayByPlayText')

    def __init__(self):
        OnscreenText.OnscreenText.__init__(self, mayChange=1, pos=(0.0, 0.75), scale=0.1, font=getSignFont())
        return None
        return