import ToontownGlobals, types, QTNode, Localizer, Quests
from DirectGui import *

def decodeQTQuestMsg(msg):
    if len(msg) == 0:
        return Localizer.QTQuestNodeNeedATask
    if len(msg) != 4:
        return None
    questId, toNpcId, toonProgress, index = msg
    quest = Quests.getQuest(questId)
    if not quest:
        return None
    msgs = quest.getQTStrings(toNpcId, toonProgress)
    if type(msgs) != type([]):
        msgs = [
         msgs]
    if index >= len(msgs):
        return None
    return msgs[index]
    return


class QTQuestNode(QTNode.QTNode, PandaObject.PandaObject):
    __module__ = __name__

    def __init__(self, name, questRoot=1):
        QTNode.QTNode.__init__(self, name)
        self.encodedMsgList = []
        self.questRoot = questRoot
        if self.questRoot:
            self.accept('questsChanged', self.__questsChanged)
            self.__questsChanged()

    def destroy(self):
        self.ignoreAll()
        QTNode.QTNode.destroy(self)

    def __setitem__(self, key, value):
        raise RuntimeError, 'cannot __setitem__ on a QTQuestNode'

    def addMenu(self, key, value, type=None):
        raise RuntimeError, 'cannot addMenu on a QTQuestNode'

    def getPhrase(self, index):
        raise RuntimeError, 'cannot getPhrase on a QTQuestNode'

    def isTerminal(self):
        return self == QTQuestSend or QTNode.QTNode.isTerminal(self)

    def getEncodedMsg(self, i):
        return self.encodedMsgList[i]

    def __questsChanged(self):
        try:
            lt = toonbase.localToon
        except:
            return
        else:
            self.phraseList = []
            self.encodedMsgList = []

            def addMsg(msg, packet):
                for phrase in self.phraseList:
                    if msg == phrase[0]:
                        return

                self.phraseList.append([msg, QTQuestSend, QTNode.QT_TEXT_NODE])
                self.encodedMsgList.append(packet)

            for quest in lt.quests:
                questId, fromNpcId, toNpcId, rewardId, toonProgress = quest
                q = Quests.getQuest(questId)
                if q is None:
                    continue
                msgs = q.getQTStrings(toNpcId, toonProgress)
                if type(msgs) != type([]):
                    msgs = [
                     msgs]
                for i in xrange(len(msgs)):
                    addMsg(msgs[i], [questId, toNpcId, toonProgress, i])

            needToontask = 1
            try:
                needToontask = len(lt.quests) != lt.questCarryLimit
            except:
                pass

            if needToontask:
                addMsg(Localizer.QTQuestNodeNeedATask, [])

        self.createMenu()
        return


QTQuestSend = QTQuestNode('questSend', questRoot=0)