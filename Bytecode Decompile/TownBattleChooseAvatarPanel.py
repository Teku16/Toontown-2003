from PandaModules import *
from ToontownBattleGlobals import *
import ToontownGlobals, StateData, DirectNotifyGlobal, BattleBase
from DirectGui import *
import Localizer

class TownBattleChooseAvatarPanel(StateData.StateData):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ChooseAvatarPanel')

    def __init__(self, doneEvent, toon):
        self.notify.info('Init choose panel...')
        StateData.StateData.__init__(self, doneEvent)
        self.numAvatars = 0
        self.chosenAvatar = 0
        self.toon = toon
        return

    def load(self):
        gui = loader.loadModelOnce('phase_3.5/models/gui/battle_gui')
        self.frame = DirectFrame(relief=None, image=gui.find('**/BtlPick_TAB'), image_color=Vec4(1, 0.2, 0.2, 1))
        self.frame.hide()
        self.statusFrame = DirectFrame(parent=self.frame, relief=None, image=gui.find('**/ToonBtl_Status_BG'), image_color=Vec4(0.5, 0.9, 0.5, 1), pos=(0.611, 0, 0))
        self.textFrame = DirectFrame(parent=self.frame, relief=None, image=gui.find('**/PckMn_Select_Tab'), image_color=Vec4(1, 1, 0, 1), text='', text_fg=Vec4(0, 0, 0, 1), text_pos=(0, -0.025, 0), text_scale=0.08, pos=(-0.013, 0, 0.013))
        if self.toon:
            self.textFrame['text'] = Localizer.TownBattleChooseAvatarToonTitle
        else:
            self.textFrame['text'] = Localizer.TownBattleChooseAvatarCogTitle
        self.avatarButtons = []
        for i in range(4):
            button = DirectButton(parent=self.frame, relief=None, image=(gui.find('**/PckMn_Arrow_Up'), gui.find('**/PckMn_Arrow_Dn'), gui.find('**/PckMn_Arrow_Rlvr')), command=self.__handleAvatar, extraArgs=[i])
            if self.toon:
                button.setScale(1, 1, -1)
                button.setPos(0, 0, -0.2)
            else:
                button.setScale(1, 1, 1)
                button.setPos(0, 0, 0.2)
            self.avatarButtons.append(button)

        self.backButton = DirectButton(parent=self.frame, relief=None, image=(gui.find('**/PckMn_BackBtn'), gui.find('**/PckMn_BackBtn_Dn'), gui.find('**/PckMn_BackBtn_Rlvr')), pos=(-0.647, 0, 0.006), scale=1.05, text=Localizer.TownBattleChooseAvatarBack, text_scale=0.05, text_pos=(0.01, -0.012), text_fg=Vec4(0, 0, 0.8, 1), command=self.__handleBack)
        gui.removeNode()
        return
        return

    def unload(self):
        self.frame.destroy()
        del self.frame
        del self.statusFrame
        del self.textFrame
        del self.avatarButtons
        del self.backButton
        return

    def enter(self, numAvatars, localNum=None, luredIndices=None, trappedIndices=None, track=None):
        self.frame.show()
        invalidTargets = []
        if not self.toon:
            if len(luredIndices) > 0:
                if track == BattleBase.TRAP or track == BattleBase.LURE:
                    invalidTargets += luredIndices
            if len(trappedIndices) > 0:
                if track == BattleBase.TRAP:
                    invalidTargets += trappedIndices
        self.__placeButtons(numAvatars, invalidTargets, localNum)
        return

    def exit(self):
        self.frame.hide()
        return

    def __handleBack(self):
        doneStatus = {'mode': 'Back'}
        messenger.send(self.doneEvent, [doneStatus])
        return

    def __handleAvatar(self, avatar):
        doneStatus = {'mode': 'Avatar', 'avatar': avatar}
        messenger.send(self.doneEvent, [doneStatus])
        return

    def adjustCogs(self, numAvatars, luredIndices, trappedIndices, track):
        invalidTargets = []
        if len(luredIndices) > 0:
            if track == BattleBase.TRAP or track == BattleBase.LURE:
                invalidTargets += luredIndices
        if len(trappedIndices) > 0:
            if track == BattleBase.TRAP:
                invalidTargets += trappedIndices
        self.__placeButtons(numAvatars, invalidTargets, None)
        return
        return

    def adjustToons(self, numToons, localNum):
        self.__placeButtons(numToons, [], localNum)
        return

    def __placeButtons(self, numAvatars, invalidTargets, localNum):
        for i in range(4):
            if numAvatars > i and i not in invalidTargets and i != localNum:
                self.avatarButtons[i].show()
            else:
                self.avatarButtons[i].hide()

        if numAvatars == 1:
            self.avatarButtons[0].setX(0)
        else:
            if numAvatars == 2:
                self.avatarButtons[0].setX(0.2)
                self.avatarButtons[1].setX(-0.2)
            else:
                if numAvatars == 3:
                    self.avatarButtons[0].setX(0.4)
                    self.avatarButtons[1].setX(0.0)
                    self.avatarButtons[2].setX(-0.4)
                else:
                    if numAvatars == 4:
                        self.avatarButtons[0].setX(0.6)
                        self.avatarButtons[1].setX(0.2)
                        self.avatarButtons[2].setX(-0.2)
                        self.avatarButtons[3].setX(-0.6)
                    else:
                        self.notify.error('Invalid number of avatars: %s' % numAvatars)
        return None
        return