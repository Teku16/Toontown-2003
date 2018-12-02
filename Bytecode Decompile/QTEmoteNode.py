import ToontownGlobals, types, QTNode, Localizer
from PythonUtil import Functor
import Emote
from DirectGui import *
import string

def inBadState(toon):
    if toon.playingAnim in ['run', 'swim', 'jump', 'sad', 'teleport', 'openBook', 'closeBook', 'readBook'] or toon.hp <= 0:
        return 1
    else:
        return 0


def doEmote(index, extraFunc=None):
    try:
        lt = toonbase.localToon
    except:
        return
    else:
        if not toonbase.emotionsEnabled or not Emote.IsEnabled(index):
            return

    lt.b_setEmoteState(index, animMultiplier=lt.animMultiplier)


class QTEmoteNode(QTNode.QTNode, PandaObject.PandaObject):
    __module__ = __name__

    def __init__(self, emoteIndex=0, emoteRoot=None, speaking=0, emoteAnim=None):
        QTNode.QTNode.__init__(self, 'emoteNode')
        self.emoteRoot = emoteRoot
        self.emoteIndex = emoteIndex
        self.emoteAnim = emoteAnim
        self.speaking = speaking
        if self.emoteRoot != None:
            self.accept('emotesChanged', self.__createEmoteMenu)
        if self.emoteRoot == None:
            self.callback = self.getEmoteCallback()
        return

    def destroy(self):
        self.ignoreAll()
        QTNode.QTNode.destroy(self)

    def __setitem__(self, key, value):
        raise RuntimeError, 'cannot __setitem__ on a QTEmoteNode'

    def getEmoteCallback(self):
        return Functor(doEmote, self.emoteIndex)

    def isTerminal(self):
        return self == QTEmoteSend or self.emoteRoot == None or QTNode.QTNode.isTerminal(self)
        return

    def __createEmoteMenu(self):
        try:
            lt = toonbase.localToon
        except:
            return
        else:
            self.phraseList = []
            self.actionList = []

            def addMsg(msg, index=None):
                for phrase in self.phraseList:
                    if msg == phrase[0]:
                        return

                if index != None:
                    emoteIndex = index
                else:
                    emoteIndex = self.emoteIndex
                nodeType = QTNode.QT_TEXT_NODE
                self.phraseList.append([msg, QTEmoteNode(emoteIndex, speaking=self.speaking), nodeType])
                return

            def addTease():
                msg = '   ?   '
                nodeType = QTNode.QT_DISABLED_NODE
                self.phraseList.append([msg, QTNode.QTSend, nodeType])

            if not self.speaking and lt.emoteAccess != None:
                for i in range(len(lt.emoteAccess)):
                    if lt.emoteAccess[i]:
                        addMsg(Localizer.EmoteList[i], i)
                    else:
                        addTease()

            for key in self.emoteRoot:
                addMsg(key)

        self.createMenu()
        return


QTEmoteSend = QTEmoteNode('emoteSend', speaking=1)