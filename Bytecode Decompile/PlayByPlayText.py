from DirectObject import *
from ShowBaseGlobal import *
from ToontownBattleGlobals import *
from ToontownGlobals import *
from SuitBattleGlobals import *
from IntervalGlobal import *
import DirectNotifyGlobal, string, OnscreenText, BattleBase

class PlayByPlayText(OnscreenText.OnscreenText):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayByPlayText')

    def __init__(self):
        OnscreenText.OnscreenText.__init__(self, mayChange=1, pos=(0.0, 0.75), scale=0.2, fg=(1, 0, 0, 1), font=getSignFont(), wordwrap=13)
        return None
        return

    def getShowInterval(self, text, duration):
        intervalList = [
         FunctionInterval(self.hide), WaitInterval(duration * 0.3), FunctionInterval(self.setText, extraArgs=[text]), FunctionInterval(self.show), WaitInterval(duration * 0.7), FunctionInterval(self.hide)]
        track = Track(intervalList)
        return track

    def getToonsDiedInterval(self, textList, duration):
        intervalList = [
         FunctionInterval(self.hide), WaitInterval(duration * 0.3)]
        waitGap = 0.6 / len(textList) * duration
        for text in textList:
            newList = [
             FunctionInterval(self.setText, extraArgs=[text]), FunctionInterval(self.show), WaitInterval(waitGap), FunctionInterval(self.hide)]
            intervalList += newList

        intervalList.append(WaitInterval(duration * 0.1))
        track = Track(intervalList)
        return track