import ToontownGlobals, types, QTNode, Localizer
from DirectGui import *

def decodeQTCustomMsg(messageIndex):
    return Localizer.CustomQTStrings.get(messageIndex, None)
    return


class QTCustomNode(QTNode.QTNode, PandaObject.PandaObject):
    __module__ = __name__

    def __init__(self, name, customRoot=1):
        QTNode.QTNode.__init__(self, name)
        self.encodedMsgList = []
        self.customRoot = customRoot
        if self.customRoot:
            self.accept('customMessagesChanged', self.__customMessagesChanged)
            self.__customMessagesChanged()

    def destroy(self):
        self.ignoreAll()
        QTNode.QTNode.destroy(self)

    def __setitem__(self, key, value):
        raise RuntimeError, 'cannot __setitem__ on a QTCustomNode'

    def addMenu(self, key, value, type=None):
        raise RuntimeError, 'cannot addMenu on a QTCustomNode'

    def getPhrase(self, index):
        raise RuntimeError, 'cannot getPhrase on a QTCustomNode'

    def isTerminal(self):
        return self == QTCustomSend or QTNode.QTNode.isTerminal(self)

    def getEncodedMsg(self, i):
        return self.encodedMsgList[i]

    def __customMessagesChanged(self):
        try:
            lt = toonbase.localToon
        except:
            return
        else:
            self.phraseList = []
            self.encodedMsgList = []

            def addMsg(msg, index):
                for phrase in self.phraseList:
                    if msg == phrase[0]:
                        return

                self.phraseList.append([msg, QTCustomSend, QTNode.QT_TEXT_NODE])
                self.encodedMsgList.append(index)

            for messageIndex in lt.customMessages:
                message = Localizer.CustomQTStrings.get(messageIndex, None)
                if message:
                    addMsg(message, messageIndex)

        self.createMenu()
        return


QTCustomSend = QTCustomNode('customSend', customRoot=0)