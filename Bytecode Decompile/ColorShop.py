from ShowBaseGlobal import *
import PandaObject, AvatarDNA, StateData
from DirectGui import *
from MakeAToonGlobals import *
import whrandom, Localizer

class ColorShop(PandaObject.PandaObject, StateData.StateData):
    __module__ = __name__

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.toon = None
        self.colorAll = 1
        return
        return

    def getGenderColorList(self, dna):
        if self.dna.getGender() == 'm':
            return AvatarDNA.defaultBoyColorList
        else:
            return AvatarDNA.defaultGirlColorList

    def enter(self, toon, shopsVisited=[]):
        base.disableMouse()
        self.toon = toon
        self.dna = toon.getStyle()
        colorList = self.getGenderColorList(self.dna)
        if COLORSHOP not in shopsVisited:
            self.headChoice = whrandom.choice(colorList)
            self.armChoice = self.headChoice
            self.legChoice = self.headChoice
            self.startColor = self.headChoice
            self.__swapHeadColor(0)
            self.__swapArmColor(0)
            self.__swapLegColor(0)
            self.allLButton['state'] = DISABLED
            self.headLButton['state'] = DISABLED
            self.armLButton['state'] = DISABLED
            self.legLButton['state'] = DISABLED
        else:
            try:
                self.headChoice = colorList.index(self.dna.headColor)
                self.armChoice = colorList.index(self.dna.armColor)
                self.legChoice = colorList.index(self.dna.legColor)
            except:
                self.headChoice = whrandom.choice(colorList)
                self.armChoice = self.headChoice
                self.legChoice = self.headChoice
                self.__swapHeadColor(0)
                self.__swapArmColor(0)
                self.__swapLegColor(0)

        self.acceptOnce('last', self.__handleBackward)
        self.acceptOnce('next', self.__handleForward)
        return

    def showButtons(self):
        if self.colorAll:
            self.allLButton.show()
            self.allRButton.show()
            self.headLButton.hide()
            self.headRButton.hide()
            self.armLButton.hide()
            self.armRButton.hide()
            self.legLButton.hide()
            self.legRButton.hide()
        else:
            self.allLButton.hide()
            self.allRButton.hide()
            self.headLButton.show()
            self.headRButton.show()
            self.armLButton.show()
            self.armRButton.show()
            self.legLButton.show()
            self.legRButton.show()
        self.toggleAllButton.show()
        return

    def hideButtons(self):
        self.allLButton.hide()
        self.allRButton.hide()
        self.headLButton.hide()
        self.headRButton.hide()
        self.armLButton.hide()
        self.armRButton.hide()
        self.legLButton.hide()
        self.legRButton.hide()
        self.toggleAllButton.hide()

    def exit(self):
        self.ignore('last')
        self.ignore('next')
        self.ignore('enter')
        try:
            del self.toon
        except:
            print 'ColorShop: toon not found'

        self.hideButtons()
        return

    def load(self):
        self.gui = loader.loadModelOnce('phase_3/models/gui/create_a_toon_gui')
        guiRArrowDown = self.gui.find('**/CrtATn_R_Arrow_DN')
        guiRArrowRollover = self.gui.find('**/CrtATn_R_Arrow_RLVR')
        guiRArrowUp = self.gui.find('**/CrtATn_R_Arrow_UP')
        self.headLButton = DirectButton(relief=None, image=(guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), image_scale=(-1, 1, 1), text=Localizer.ColorShopHead, text_scale=0.0625, text_pos=(0.025, 0), text_fg=(0.8, 0.1, 0, 1), pos=(-0.9, 0, 0.3), command=self.__swapHeadColor, extraArgs=[-1])
        self.headRButton = DirectButton(relief=None, image=(guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), text=Localizer.ColorShopHead, text_scale=0.0625, text_pos=(-0.025, 0), text_fg=(0.8, 0.1, 0, 1), pos=(0, 0, 0.3), command=self.__swapHeadColor, extraArgs=[1])
        self.armLButton = DirectButton(relief=None, image=(guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), image_scale=(-1, 1, 1), text=Localizer.ColorShopBody, text_scale=0.0625, text_pos=(0.025, 0), text_fg=(0.8, 0.1, 0, 1), pos=(-0.9, 0, -0.1), command=self.__swapArmColor, extraArgs=[-1])
        self.armRButton = DirectButton(relief=None, image=(guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), text=Localizer.ColorShopBody, text_scale=0.0625, text_pos=(-0.025, 0), text_fg=(0.8, 0.1, 0, 1), pos=(0, 0, -0.1), command=self.__swapArmColor, extraArgs=[1])
        self.allLButton = DirectButton(relief=None, image=(guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), image_scale=(-1, 1, 1), text=Localizer.ColorShopToon, text_scale=0.0625, text_pos=(0.025, 0), text_fg=(0.8, 0.1, 0, 1), pos=(-0.9, 0, -0.1), command=self.__swapAllColor, extraArgs=[-1])
        self.allRButton = DirectButton(relief=None, image=(guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), text=Localizer.ColorShopToon, text_scale=0.0625, text_pos=(-0.025, 0), text_fg=(0.8, 0.1, 0, 1), pos=(0, 0, -0.1), command=self.__swapAllColor, extraArgs=[1])
        self.legLButton = DirectButton(relief=None, image=(guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), image_scale=(-1, 1, 1), text=Localizer.ColorShopLegs, text_scale=0.0625, text_pos=(0.025, 0), text_fg=(0.8, 0.1, 0, 1), pos=(-0.9, 0, -0.5), command=self.__swapLegColor, extraArgs=[-1])
        self.legRButton = DirectButton(relief=None, image=(guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), text=Localizer.ColorShopLegs, text_scale=0.0625, text_pos=(-0.025, 0), text_fg=(0.8, 0.1, 0, 1), pos=(0, 0, -0.5), command=self.__swapLegColor, extraArgs=[1])
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        self.toggleAllButton = DirectButton(parent=aspect2d, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.8, 1.1, 1.1), pos=(-0.1, 0, 0.55), text=Localizer.ColorShopParts, text_scale=0.06, text_pos=(0.0, -0.02), command=self.__toggleAllColor)
        guiButton.removeNode()
        self.headLButton.hide()
        self.headRButton.hide()
        self.armLButton.hide()
        self.armRButton.hide()
        self.legLButton.hide()
        self.legRButton.hide()
        self.allLButton.hide()
        self.allRButton.hide()
        self.toggleAllButton.hide()
        return
        return

    def unload(self):
        self.gui.removeNode()
        del self.gui
        self.headLButton.destroy()
        self.headRButton.destroy()
        self.armLButton.destroy()
        self.armRButton.destroy()
        self.legLButton.destroy()
        self.legRButton.destroy()
        self.allLButton.destroy()
        self.allRButton.destroy()
        self.toggleAllButton.destroy()
        del self.headLButton
        del self.headRButton
        del self.armLButton
        del self.armRButton
        del self.legLButton
        del self.legRButton
        del self.allLButton
        del self.allRButton
        del self.toggleAllButton
        return None
        return

    def __toggleAllColor(self):
        if self.colorAll:
            self.colorAll = 0
            self.toggleAllButton['text'] = Localizer.ColorShopAll
        else:
            self.colorAll = 1
            self.toggleAllButton['text'] = Localizer.ColorShopParts
            self.legChoice = self.armChoice = self.headChoice
            self.__swapAllColor(0)
        self.showButtons()

    def __swapAllColor(self, offset):
        colorList = self.getGenderColorList(self.dna)
        length = len(colorList)
        choice = (self.headChoice + offset) % length
        self.__updateScrollButtons(choice, length, self.allLButton, self.allRButton)
        self.__swapHeadColor(offset)
        self.__swapArmColor(offset)
        self.__swapLegColor(offset)

    def __swapHeadColor(self, offset):
        colorList = self.getGenderColorList(self.dna)
        length = len(colorList)
        self.headChoice = (self.headChoice + offset) % length
        self.__updateScrollButtons(self.headChoice, length, self.headLButton, self.headRButton)
        newColor = colorList[self.headChoice]
        self.dna.headColor = newColor
        self.toon.swapToonColor(self.dna)

    def __swapArmColor(self, offset):
        colorList = self.getGenderColorList(self.dna)
        length = len(colorList)
        self.armChoice = (self.armChoice + offset) % length
        self.__updateScrollButtons(self.armChoice, length, self.armLButton, self.armRButton)
        newColor = colorList[self.armChoice]
        self.dna.armColor = newColor
        self.toon.swapToonColor(self.dna)

    def __swapLegColor(self, offset):
        colorList = self.getGenderColorList(self.dna)
        length = len(colorList)
        self.legChoice = (self.legChoice + offset) % length
        self.__updateScrollButtons(self.legChoice, length, self.legLButton, self.legRButton)
        newColor = colorList[self.legChoice]
        self.dna.legColor = newColor
        self.toon.swapToonColor(self.dna)

    def __updateScrollButtons(self, choice, length, lButton, rButton):
        if choice == (self.startColor - 1) % length:
            rButton['state'] = DISABLED
        else:
            rButton['state'] = NORMAL
        if choice == self.startColor % length:
            lButton['state'] = DISABLED
        else:
            lButton['state'] = NORMAL

    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)