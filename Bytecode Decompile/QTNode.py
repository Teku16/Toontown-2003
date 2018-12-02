import ToontownGlobals, types, Localizer
from DirectGui import *
from IntervalGlobal import *
QT_DISABLED_NODE = 'd'
QT_TEXT_NODE = 't'
QT_MENU_NODE = 'm'
QT_TEXT_MENU_NODE = 'tm'
QT_EMOTE_ROOT_NODE = 'er'
QT_EMOTE_SPEAK_ROOT_NODE = 'es'
QT_EMOTE_NODE = 'e'
QT_QUEST_ROOT_NODE = 'q'
QT_CUSTOM_ROOT_NODE = 'c'
MENU_NODES_LIST = [
 QT_MENU_NODE, QT_EMOTE_ROOT_NODE, QT_EMOTE_SPEAK_ROOT_NODE]

class QTNode:
    __module__ = __name__
    font = ToontownGlobals.getToonFont()

    def __init__(self, name):
        self.name = name
        self.width = 0.0
        self.selected = None
        self.itemHeight = 0.0
        self.phraseList = []
        self.nodepath = None
        self.callback = None
        self.speaking = 1
        self.buttons = []
        self.pos = (0, 0, 0)
        self.popupInfo = None
        return

    def __findPhrasePair(self, key):
        phrasePair = None
        if isinstance(key, types.StringType):
            for pp in self.phraseList:
                if pp[0] == key:
                    phrasePair = pp
                    break

        else:
            if key < len(self.phraseList):
                phrasePair = self.phraseList[key]
        return phrasePair
        return

    def __getitem__(self, key):
        phrasePair = self.__findPhrasePair(key)
        if phrasePair == None:
            return None
        else:
            return phrasePair[1]
        return

    def __setitem__(self, key, value):
        phrasePair = self.__findPhrasePair(key)
        if phrasePair == None:
            self.phraseList.append([key, value, QT_TEXT_NODE])
        else:
            phrasePair[1] = value
            phrasePair[2] = QT_TEXT_NODE
        return

    def addMenu(self, key, value, type=QT_MENU_NODE):
        phrasePair = self.__findPhrasePair(key)
        if phrasePair == None:
            phrasePair = self.phraseList.append([key, value, type])
        else:
            phrasePair[1] = value
            phrasePair[2] = type
        return

    def getPhrase(self, index):
        pp = self.__findPhrasePair(index)
        if pp == None:
            return ''
        else:
            if pp[2] in MENU_NODES_LIST:
                return ''
            else:
                return pp[0]
        return

    def __createDisplayText(self, phrasePair):
        text = phrasePair[0]
        if phrasePair[2] in MENU_NODES_LIST:
            pass
        else:
            if not phrasePair[1].isTerminal():
                text = text + '...'
        return text

    def isTerminal(self):
        return self == QTSend

    def isSpeaking(self):
        return self.speaking

    def createMenu(self):
        self.deleteMenu()
        self.nodepath = hidden.attachNewNode('QTNode-' + self.name)
        l = r = t = b = 0
        text = TextNode('qtmenu')
        text.freeze()
        text.setFont(QTNode.font)
        for pp in self.phraseList:
            dText = self.__createDisplayText(pp)
            text.setText(dText)
            bounds = text.getCardActual()
            if pp[2] in MENU_NODES_LIST:
                arrowPad = 1.0
            else:
                arrowPad = 0.0
            l = min(l, bounds[0])
            r = max(r, bounds[1] + arrowPad)
            b = min(b, bounds[2])
            t = max(t, bounds[3])

        del text
        z = 0
        sf = 0.055
        padx = 0.25
        padz = 0.1
        self.width = (r + padx) * sf
        self.itemHeight = dz = -(padz + padz + (t - b)) * sf
        index = 0
        for pp in self.phraseList:
            frameColor = (
             0.8, 0.8, 1, 1)
            rolloverColor = (0.9, 0.9, 1, 1)
            text_fg = (0, 0, 0, 1.0)
            state = NORMAL
            dText = self.__createDisplayText(pp)
            if pp[2] in MENU_NODES_LIST:
                relief = RAISED
                image = ('phase_3/models/props/page-arrow', 'poly')
                image_pos = (r - padx, 0, (t - b) / 4.0)
            else:
                relief = FLAT
                image = None
                image_pos = (0, 0, 0)
                if pp[2] == QT_DISABLED_NODE:
                    frameColor = (
                     (
                      0.8, 0.8, 0.8, 0.5),)
                    rolloverColor = (0.9, 0.9, 1, 0.5)
                    text_fg = (0.5, 0.5, 0.5, 1.0)
                    relief = SUNKEN
            btn = DirectButton(parent=self.nodepath, state=state, text=dText, image=image, image_pos=image_pos, text_font=QTNode.font, text_align=TextNode.ALeft, textMayChange=0, frameColor=frameColor, frameSize=(l - padx, r + padx, b - padz, t + padz), relief=relief, pos=(0.0, 0.0, z), text_fg=text_fg, scale=0.055, extraArgs=[index])
            btn.frameStyle[2].setColor(rolloverColor[0], rolloverColor[1], rolloverColor[2], rolloverColor[3])
            btn.updateFrameStyle()
            btn.bind(EXIT, self.__buttonExited, extraArgs=[index, pp[2]])
            btn.bind(ENTER, self.__buttonEntered, extraArgs=[index, pp[2]])
            btn.bind(B1PRESS, self.__buttonSelected, extraArgs=[index, pp[2]])
            self.buttons.append(btn)
            z = z + dz
            index += 1

        return

    def setPos(self, x, y, z):
        self.pos = Point3(x, y, z)
        self.nodepath.setPos(x, y, z)

    def getPos(self):
        return self.pos

    def deleteMenu(self):
        for button in self.buttons:
            button.destroy()

        self.buttons = []
        if self.nodepath:
            self.nodepath.removeNode()
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        return

    def destroy(self):
        self.deleteMenu()
        del self.buttons
        del self.nodepath

    def enterPopupInfo(self):
        if self.popupInfo == None:
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            self.popupInfo = DirectFrame(parent=hidden, relief=None, state='normal', text=Localizer.QTPopupEmoteMessage, frameSize=(-1, 1, -1, 1), geom=getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(0.88, 1, 0.45), geom_pos=(0, 0, -0.08), text_scale=0.08)
            DirectButton(self.popupInfo, image=okButtonImage, relief=None, text=Localizer.QTPopupEmoteMessageOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.16), command=self.__handlePopupEmoteMessageOK)
            buttons.removeNode()
        self.popupInfo.reparentTo(aspect2d)
        return

    def __handlePopupEmoteMessageOK(self):
        self.popupInfo.reparentTo(hidden)

    def __buttonSelected(self, index, type, event):
        if type == QT_DISABLED_NODE:
            self.enterPopupInfo()
            return
        messenger.send('QTNode_selected', [self, index])
        self.selected = self[index]

    def __buttonEntered(self, index, type, event):
        if self.selected:
            try:
                self.selected.nodepath.reparentTo(hidden)
            except AttributeError:
                pass

        if type == QT_DISABLED_NODE:
            pass
        else:
            if type != QT_TEXT_NODE:
                self.__buttonSelected(index, type, event)

    def __buttonExited(self, index, type, event):
        pass


QTSend = QTNode('send')