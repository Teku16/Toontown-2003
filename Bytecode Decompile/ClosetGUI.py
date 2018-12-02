import ClothesGUI, ClosetGlobals
from DirectGui import *
import Localizer, ToontownGlobals

class ClosetGUI(ClothesGUI.ClothesGUI):
    __module__ = __name__
    notify = directNotify.newCategory('ClosetGUI')

    def __init__(self, isOwner, doneEvent, cancelEvent, swapEvent, deleteEvent, topList=None, botList=None):
        ClothesGUI.ClothesGUI.__init__(self, ClothesGUI.CLOTHES_CLOSET, doneEvent, swapEvent)
        self.toon = None
        self.topsList = topList
        self.bottomsList = botList
        self.isOwner = isOwner
        self.deleteEvent = deleteEvent
        self.cancelEvent = cancelEvent
        self.genderChange = 0
        return

    def load(self):
        ClothesGUI.ClothesGUI.load(self)
        self.cancelButton = DirectButton(relief=None, image=(self.gui.find('**/CrtAtoon_Btn2_UP'), self.gui.find('**/CrtAtoon_Btn2_DOWN'), self.gui.find('**/CrtAtoon_Btn2_RLLVR')), pos=(0.15, 0, -0.85), command=self.__handleCancel, text=('', Localizer.MakeAToonCancel, Localizer.MakeAToonCancel), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_pos=(0, -0.03), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.cancelButton.hide()
        if self.isOwner:
            trashcanGui = loader.loadModel('phase_3/models/gui/trashcan_gui.bam')
            trashImage = (trashcanGui.find('**/TrashCan_CLSD'), trashcanGui.find('**/TrashCan_OPEN'), trashcanGui.find('**/TrashCan_RLVR'))
            self.topTrashButton = DirectButton(image=trashImage, relief=None, text_scale=0.15, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.67, 0, 0.04), command=self.__handleDelete, extraArgs=[ClosetGlobals.SHIRT], scale=(0.5, 0.5, 0.5))
            self.bottomTrashButton = DirectButton(image=trashImage, relief=None, text_scale=0.15, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.67, 0, -0.36), command=self.__handleDelete, extraArgs=[ClosetGlobals.SHORTS], scale=(0.5, 0.5, 0.5))
            self.button = DirectButton(relief=None, image=(self.gui.find('**/CrtAtoon_Btn1_UP'), self.gui.find('**/CrtAtoon_Btn1_DOWN'), self.gui.find('**/CrtAtoon_Btn1_RLLVR')), pos=(-0.15, 0, -0.85), command=self.__handleButton, text=('', Localizer.MakeAToonDone, Localizer.MakeAToonDone), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_pos=(0, -0.03), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
            trashcanGui.removeNode()
        return

    def unload(self):
        ClothesGUI.ClothesGUI.unload(self)
        self.cancelButton.destroy()
        del self.cancelButton
        if self.isOwner:
            self.topTrashButton.destroy()
            self.bottomTrashButton.destroy()
            self.button.destroy()
            del self.topTrashButton
            del self.bottomTrashButton
            del self.button

    def showButtons(self):
        ClothesGUI.ClothesGUI.showButtons(self)
        self.cancelButton.show()
        if self.isOwner:
            self.topTrashButton.show()
            self.bottomTrashButton.show()
            self.button.show()

    def hideButtons(self):
        ClothesGUI.ClothesGUI.hideButtons(self)
        self.cancelButton.hide()
        if self.isOwner:
            self.topTrashButton.hide()
            self.bottomTrashButton.hide()
            self.button.hide()

    def setupScrollInterface(self):
        self.notify.debug('setupScrollInterface')
        self.dna = self.toon.getStyle()
        self.gender = self.dna.getGender()
        self.swappedTorso = 0
        if self.topsList == None:
            self.topsList = self.toon.getClothesTopsList()
        if self.bottomsList == None:
            self.bottomsList = self.toon.getClothesBottomsList()
        self.tops = []
        self.bottoms = []
        self.tops.append([self.dna.topTex, self.dna.topTexColor, self.dna.sleeveTex, self.dna.sleeveTexColor])
        self.bottoms.append([self.dna.botTex, self.dna.botTexColor])
        i = 0
        while i < len(self.topsList):
            self.tops.append([self.topsList[i], self.topsList[i + 1], self.topsList[i + 2], self.topsList[i + 3]])
            i = i + 4

        i = 0
        while i < len(self.bottomsList):
            self.bottoms.append([self.bottomsList[i], self.bottomsList[i + 1]])
            i = i + 2

        self.topChoice = 0
        self.bottomChoice = 0
        self.swapTop(0)
        self.swapBottom(0)
        if self.isOwner:
            self.updateTrashButtons()
        self.setupButtons()
        return

    def updateTrashButtons(self):
        if len(self.tops) < 2:
            self.topTrashButton['state'] = DISABLED
        else:
            self.topTrashButton['state'] = NORMAL
        if len(self.bottoms) < 2:
            self.bottomTrashButton['state'] = DISABLED
        else:
            self.bottomTrashButton['state'] = NORMAL

    def setGender(self, gender):
        self.ownerGender = gender
        self.genderChange = 1

    def swapBottom(self, offset):
        length = len(self.bottoms)
        self.bottomChoice += offset
        if self.bottomChoice <= 0:
            self.bottomChoice = 0
        self.updateScrollButtons(self.bottomChoice, length, 0, self.bottomLButton, self.bottomRButton)
        if self.bottomChoice < 0 or self.bottomChoice >= len(self.bottoms) or len(self.bottoms[self.bottomChoice]) != 2:
            self.notify.warning('bottomChoice index is out of range!')
            return None
        self.toon.style.botTex = self.bottoms[self.bottomChoice][0]
        self.toon.style.botTexColor = self.bottoms[self.bottomChoice][1]
        if self.genderChange == 1:
            if self.bottomChoice > 0:
                self.__handleGenderBender(1)
            else:
                self.__handleGenderBender(0)
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)
            self.swappedTorso = 1
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        return

    def __handleGenderBender(self, type):
        if type == 1:
            if self.toon.style.gender != self.ownerGender and self.toon.style.gender == 'f':
                self.toon.swapToonTorso(self.toon.style.torso[0] + 's', genClothes=0)
                self.toon.loop('neutral', 0)
                self.swappedTorso = 1
            self.toon.style.gender = self.ownerGender
        else:
            self.toon.style.gender = self.gender
            if self.toon.style.gender != self.ownerGender and self.toon.style.gender == 'm':
                self.toon.swapToonTorso(self.toon.style.torso[0] + 's', genClothes=0)
                self.toon.loop('neutral', 0)
                self.swappedTorso = 1

    def removeTop(self, index):
        listLen = len(self.tops)
        if index < listLen:
            del self.tops[index]
            if self.topChoice > index:
                self.topChoice -= 1
            else:
                if self.topChoice == index:
                    self.topChoice = 0
            return 1
        return 0

    def removeBottom(self, index):
        listLen = len(self.bottoms)
        if index < listLen:
            del self.bottoms[index]
            if self.bottomChoice > index:
                self.bottomChoice -= 1
            else:
                if self.bottomChoice == index:
                    self.bottomChoice = 0
            return 1
        return 0

    def __handleButton(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleCancel(self):
        messenger.send(self.cancelEvent)

    def __handleDelete(self, t_or_b):
        messenger.send(self.deleteEvent, [t_or_b])