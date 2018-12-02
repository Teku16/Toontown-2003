import PandaObject, QTNode, QTQuestNode, QTEmoteNode, QTCustomNode, QTTree, FSM, State, Emote, string
from DirectGui import *
import Localizer

class ChatInputQuickTalker(PandaObject.PandaObject):
    __module__ = __name__

    def __init__(self, chatMgr):
        self.chatMgr = chatMgr
        self.whisperAvatarId = None
        self.sentenceList = []
        qtGraph = {}
        self.setupQTGraph()
        self.fsm = FSM.FSM('QuickTalker', [
         State.State('Hidden', self.__enterHidden, self.__exitHidden, [
          'Constructing']),
         State.State('Constructing', self.__enterConstructing, self.__exitConstructing, [
          'Constructing', 'SayIt', 'Hidden']),
         State.State('SayIt', self.__enterSayIt, self.__exitSayIt, [
          'Hidden'])], 'Hidden', 'Hidden')
        self.fsm.enterInitialState()
        return

    def delete(self):
        self.ignoreAll()
        for entry in self.qtGraph.values():
            entry.destroy()

        del self.qtGraph
        del self.fsm
        del self.sentenceList

    def show(self, whisperAvatarId=None):
        self.whisperAvatarId = whisperAvatarId
        self.curQTnode = self.qtGraph['start']
        if self.whisperAvatarId:
            self.curQTnode.setPos(-0.7, 0, 0.95)
        else:
            self.curQTnode.setPos(-1.05, 0, 0.92)
        self.accept('mouse1', self.__cancelButtonPressed)
        self.fsm.request('Constructing')

    def hide(self):
        self.fsm.request('Hidden')

    def getSentenceCleartext(self):
        sentence = ''
        for entry in self.sentenceList:
            sentence = sentence + entry[0].getPhrase(entry[1])

        return sentence

    def getSentenceEncoded(self):
        sentence = []
        for entry in self.sentenceList:
            sentence.append(entry[1])

        return sentence

    def cleanup(self):
        self.ignore('mouse1')
        for entry in self.sentenceList:
            entry[0].nodepath.reparentTo(hidden)

        try:
            if self.curQTnode.nodepath:
                self.curQTnode.nodepath.reparentTo(hidden)
        except AttributeError:
            pass

    def decodeQTMessage(self, msg):
        curNode = self.qtGraph['start']
        for i in range(len(msg) - 1):
            curNode = curNode[msg[i]]
            if curNode == None:
                break

        return curNode.getPhrase(msg[-1])
        return

    def setupQTGraph(self, QTDef=QTTree.QTTree):

        def addMenu(graph, menuDef):
            name = menuDef[0]
            if len(menuDef) == 2:
                subMenuName = menuDef[0]
                menuType = menuDef[1]
                if menuType == QTNode.QT_QUEST_ROOT_NODE:
                    menuNode = QTQuestNode.QTQuestNode(name)
                    graph[name] = menuNode
                    return
                else:
                    if menuType == QTNode.QT_CUSTOM_ROOT_NODE:
                        menuNode = QTCustomNode.QTCustomNode(name)
                        graph[name] = menuNode
                        return
                    else:
                        if menuType == QTNode.QT_EMOTE_NODE:
                            menuNode = QTEmoteNode.QTEmoteNode(0)
                            graph[name] = menuNode
                            return
                        else:
                            if type(menuType) == type(0):
                                menuNode = QTEmoteNode.QTEmoteNode(menuType, speaking=1)
                                graph[name] = menuNode
                                return
            else:
                if len(menuDef) == 3:
                    subMenuName = menuDef[0]
                    menuType = menuDef[1]
                    menuEntries = menuDef[2]
                    if menuType == QTNode.QT_EMOTE_ROOT_NODE:
                        menuNode = QTEmoteNode.QTEmoteNode(0, emoteRoot=menuEntries)
                        graph[name] = menuNode
                        return
                    else:
                        if menuType == QTNode.QT_EMOTE_SPEAK_ROOT_NODE:
                            menuNode = QTEmoteNode.QTEmoteNode(Localizer.EmoteFuncDict[string.lower(name)], emoteRoot=menuEntries, speaking=1, emoteAnim=subMenuName)
                            graph[name] = menuNode
                            return
            entries = menuDef[-1]
            menuNode = QTNode.QTNode(name)
            graph[name] = menuNode
            for i in entries:
                if type(i) == type(''):
                    menuNode[i] = QTNode.QTSend
                else:
                    addMenu(graph, i)
                    subMenuName = i[0]
                    graph[name] = menuNode
                    if len(i) == 3:
                        menuNode.addMenu(subMenuName, graph[subMenuName], i[1])
                    else:
                        if len(i) == 2 and type(i[1]) == type(0):
                            menuNode.addMenu(subMenuName, graph[subMenuName], QTNode.QT_TEXT_NODE)
                        else:
                            menuNode.addMenu(subMenuName, graph[subMenuName])

        self.qtGraph = {}
        tree = ['start', QTDef]
        addMenu(self.qtGraph, tree)
        self.rebuildMenus()

    def rebuildMenus(self):
        for key in self.qtGraph.keys():
            self.qtGraph[key].createMenu()

    def __selectionMade(self, qtNode, index):
        newNode = qtNode[index]
        oldNode = qtNode.selected
        if qtNode != self.curQTnode or newNode != oldNode:
            found = 0
            newList = []
            for entry in self.sentenceList:
                if entry[0] == qtNode:
                    found = 1
                if found:
                    entry[0].selected.nodepath.reparentTo(hidden)
                    entry[0].selected = None
                else:
                    newList.append(entry)

            self.sentenceList = newList
        self.curQTnode = newNode
        self.sentenceList.append([qtNode, index])
        if self.curQTnode.callback != None and not self.whisperAvatarId:
            self.curQTnode.callback()
        if self.curQTnode.isTerminal():
            if self.curQTnode.isSpeaking():
                self.fsm.request('SayIt')
            else:
                self.chatMgr.fsm.request('mainMenu')
        else:
            pos = qtNode.getPos()
            scale = 1.0 - len(self.sentenceList) * 0.14
            self.curQTnode.nodepath.setColorScale(scale, scale, scale, 1)
            if len(self.sentenceList) == 1:
                offset = 1.0
            else:
                offset = 2.0
            self.curQTnode.setPos(pos[0] + qtNode.width / offset, 0, pos[2] + qtNode.itemHeight * index)
            self.fsm.request('Constructing')
        return

    def __cancelButtonPressed(self, event=None):
        self.cleanup()
        self.chatMgr.fsm.request('mainMenu')

    def __enterHidden(self):
        self.cleanup()
        self.sentenceList = []

    def __exitHidden(self):
        pass

    def __enterConstructing(self):
        self.curQTnode.nodepath.reparentTo(aspect2d, FOREGROUND_SORT_INDEX)
        self.accept('QTNode_selected', self.__selectionMade)

    def __exitConstructing(self):
        self.ignore('QTNode_selected')

    def __enterSayIt(self):
        self.cleanup()
        if isinstance(self.curQTnode, QTQuestNode.QTQuestNode):
            finalNode = self.sentenceList[-1][0]
            index = self.sentenceList[-1][1]
            ds = finalNode.getEncodedMsg(index)
            if self.whisperAvatarId:
                self.chatMgr.sendWhisperQTQuestChatMessage(ds, self.whisperAvatarId)
            else:
                self.chatMgr.sendQTQuestChatMessage(ds)
        else:
            if isinstance(self.curQTnode, QTCustomNode.QTCustomNode):
                finalNode = self.sentenceList[-1][0]
                index = self.sentenceList[-1][1]
                ds = finalNode.getEncodedMsg(index)
                if self.whisperAvatarId:
                    self.chatMgr.sendWhisperQTCustomChatMessage(ds, self.whisperAvatarId)
                else:
                    self.chatMgr.sendQTCustomChatMessage(ds)
            else:
                ds = self.getSentenceEncoded()
                if self.whisperAvatarId:
                    self.chatMgr.sendWhisperQTChatMessage(ds, self.whisperAvatarId)
                else:
                    self.chatMgr.sendQTChatMessage(ds)
        self.chatMgr.fsm.request('mainMenu')

    def __exitSayIt(self):
        pass