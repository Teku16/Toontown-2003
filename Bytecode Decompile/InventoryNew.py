from DirectGui import *
from ToontownBattleGlobals import *
import InventoryBase, Localizer, BlinkingArrows
from IntervalGlobal import *
import ToontownGlobals

class InventoryNew(InventoryBase.InventoryBase, DirectFrame):
    __module__ = __name__
    PressableTextColor = Vec4(1, 1, 1, 1)
    PressableGeomColor = Vec4(1, 1, 1, 1)
    PressableImageColor = Vec4(0, 0.6, 1, 1)
    NoncreditPressableImageColor = Vec4(0.3, 0.6, 0.6, 1)
    DeletePressableImageColor = Vec4(0.7, 0.1, 0.1, 1)
    UnpressableTextColor = Vec4(1, 1, 1, 0.3)
    UnpressableGeomColor = Vec4(1, 1, 1, 0.3)
    UnpressableImageColor = Vec4(0.3, 0.3, 0.3, 0.8)
    BookUnpressableTextColor = Vec4(1, 1, 1, 1)
    BookUnpressableGeomColor = Vec4(1, 1, 1, 1)
    BookUnpressableImage0Color = Vec4(0, 0.6, 1, 1)
    BookUnpressableImage2Color = Vec4(0.1, 0.7, 1, 1)
    TrackYOffset = 0.0
    TrackYSpacing = -0.12
    ButtonXOffset = -0.31
    ButtonXSpacing = 0.193

    def __init__(self, toon, invStr=None):
        InventoryBase.InventoryBase.__init__(self, toon, invStr)
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(InventoryNew)
        self.battleCreditLevel = None
        self.detailCredit = None
        self.__battleCreditMultiplier = 1
        self.__invasionCreditMultiplier = 1
        self.tutorialFlag = 0
        self.activateMode = 'book'
        self.load()
        self.hide()
        return
        return

    def setBattleCreditMultiplier(self, mult):
        self.__battleCreditMultiplier = mult

    def getBattleCreditMultiplier(self):
        return self.__battleCreditMultiplier

    def setInvasionCreditMultiplier(self, mult):
        self.__invasionCreditMultiplier = mult

    def getInvasionCreditMultiplier(self):
        return self.__invasionCreditMultiplier

    def show(self):
        if self.tutorialFlag:
            self.tutArrows.arrowsOn(-0.33, -0.12, 180, -0.33, -0.24, 180, onTime=1.0, offTime=0.2)
            if self.numItem(THROW_TRACK, 0) == 0:
                self.tutArrows.arrow1.reparentTo(hidden)
            else:
                self.tutArrows.arrow1.reparentTo(self.battleFrame, 1)
            if self.numItem(SQUIRT_TRACK, 0) == 0:
                self.tutArrows.arrow2.reparentTo(hidden)
            else:
                self.tutArrows.arrow2.reparentTo(self.battleFrame, 1)
            self.tutText.show()
            self.tutText.reparentTo(aspect2d)
            self.tutText.reparentTo(self.battleFrame, 1)
        DirectFrame.show(self)

    def hide(self):
        if self.tutorialFlag:
            self.tutArrows.arrowsOff()
            self.tutText.hide()
        DirectFrame.hide(self)

    def updateTotalPropsText(self):
        self.totalLabel['text'] = Localizer.InventoryTotalGags % (self.totalProps, self.toon.getMaxCarry())
        return

    def unload(self):
        del self.invModels
        self.buttonModels.removeNode()
        del self.buttonModels
        del self.upButton
        del self.downButton
        del self.rolloverButton
        del self.flatButton
        del self.invFrame
        del self.battleFrame
        del self.purchaseFrame
        del self.storePurchaseFrame
        del self.deleteEnterButton
        del self.deleteExitButton
        del self.detailFrame
        del self.detailNameLabel
        del self.detailAmountLabel
        del self.detailDataLabel
        del self.totalLabel
        del self.trackRows
        del self.trackNameLabels
        del self.trackBars
        del self.buttons
        InventoryBase.InventoryBase.unload(self)
        DirectFrame.destroy(self)
        return

    def load(self):
        invModel = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        self.invModels = []
        for track in range(len(AvPropsNew)):
            itemList = []
            for item in range(len(AvPropsNew[track])):
                itemList.append(invModel.find('**/' + AvPropsNew[track][item]))

            self.invModels.append(itemList)

        invModel.removeNode()
        del invModel
        self.buttonModels = loader.loadModelOnce('phase_3.5/models/gui/inventory_gui')
        self.rowModel = self.buttonModels.find('**/InventoryRow')
        self.upButton = self.buttonModels.find('**/InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')
        self.flatButton = self.buttonModels.find('**/InventoryButtonFlat')
        self.invFrame = DirectFrame(relief=None, parent=self)
        self.battleFrame = None
        self.purchaseFrame = None
        self.storePurchaseFrame = None
        trashcanGui = loader.loadModelOnce('phase_3/models/gui/trashcan_gui')
        self.deleteEnterButton = DirectButton(parent=self.invFrame, image=(trashcanGui.find('**/TrashCan_CLSD'), trashcanGui.find('**/TrashCan_OPEN'), trashcanGui.find('**/TrashCan_RLVR')), text=('', Localizer.InventoryDelete, Localizer.InventoryDelete), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.1, text_pos=(0, -0.1), text_font=getInterfaceFont(), textMayChange=0, relief=None, pos=(-1, 0, -0.35), scale=1.0)
        self.deleteExitButton = DirectButton(parent=self.invFrame, image=(trashcanGui.find('**/TrashCan_OPEN'), trashcanGui.find('**/TrashCan_CLSD'), trashcanGui.find('**/TrashCan_RLVR')), text=('', Localizer.InventoryDone, Localizer.InventoryDone), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.1, text_pos=(0, -0.1), text_font=getInterfaceFont(), textMayChange=0, relief=None, pos=(-1, 0, -0.35), scale=1.0)
        trashcanGui.removeNode()
        self.deleteHelpText = DirectLabel(parent=self.invFrame, relief=None, pos=(0.272, 0.3, -0.907), text=Localizer.InventoryDeleteHelp, text_fg=(0, 0, 0, 1), text_scale=0.08, textMayChange=0)
        self.deleteHelpText.hide()
        self.detailFrame = DirectFrame(parent=self.invFrame, relief=None, pos=(1.05, 0, -0.08))
        self.detailNameLabel = DirectLabel(parent=self.detailFrame, text='', text_fg=(0.05, 0.14, 0.4, 1), scale=0.05, pos=(0.01, 0, 0), text_font=getInterfaceFont(), relief=None, image=self.invModels[0][0])
        self.detailAmountLabel = DirectLabel(parent=self.detailFrame, text='', text_fg=(0.05, 0.14, 0.4, 1), scale=0.05, pos=(0.19, 0, -0.19), text_font=getInterfaceFont(), text_align=TextNode.ARight, relief=None)
        self.detailDataLabel = DirectLabel(parent=self.detailFrame, text='', text_fg=(0.05, 0.14, 0.4, 1), scale=0.05, pos=(-0.19, 0, -0.24), text_font=getInterfaceFont(), text_align=TextNode.ALeft, relief=None)
        self.detailCreditLabel = DirectLabel(parent=self.detailFrame, text=Localizer.InventorySkillCreditNone, text_fg=(0.05, 0.14, 0.4, 1), scale=0.05, pos=(-0.19, 0, -0.39), text_font=getInterfaceFont(), text_align=TextNode.ALeft, relief=None)
        self.detailCreditLabel.hide()
        self.totalLabel = DirectLabel(text='', parent=self.detailFrame, pos=(0.005, 0, -0.095), scale=0.05, text_fg=(0.05, 0.14, 0.4, 1), text_font=getInterfaceFont(), relief=None)
        self.updateTotalPropsText()
        self.trackRows = []
        self.trackNameLabels = []
        self.trackBars = []
        self.buttons = []
        for track in range(0, len(Tracks)):
            trackFrame = DirectFrame(parent=self.invFrame, image=self.rowModel, pos=(0, 0.3, self.TrackYOffset + track * self.TrackYSpacing), image_color=(TrackColors[track][0], TrackColors[track][1], TrackColors[track][2], 1), state=NORMAL, relief=None)
            trackFrame.bind(WITHIN, self.enterTrackFrame, extraArgs=[track])
            trackFrame.bind(WITHOUT, self.exitTrackFrame, extraArgs=[track])
            self.trackRows.append(trackFrame)
            self.trackNameLabels.append(DirectLabel(text=Tracks[track].upper(), parent=self.trackRows[track], pos=(-0.72, -0.1, 0.01), scale=0.05, relief=None, text_fg=(0.2, 0.2, 0.2, 1), text_font=getInterfaceFont(), text_align=TextNode.ALeft, textMayChange=0))
            self.trackBars.append(DirectWaitBar(parent=self.trackRows[track], pos=(-0.58, -0.1, -0.025), relief=SUNKEN, frameSize=(-0.6, 0.6, -0.1, 0.1), borderWidth=(0.02, 0.02), scale=0.25, frameColor=(TrackColors[track][0] * 0.6, TrackColors[track][1] * 0.6, TrackColors[track][2] * 0.6, 1), barColor=(TrackColors[track][0] * 0.9, TrackColors[track][1] * 0.9, TrackColors[track][2] * 0.9, 1), text='0 / 0', text_scale=0.16, text_fg=(0, 0, 0, 0.8), text_align=TextNode.ACenter, text_pos=(0, -0.05)))
            self.buttons.append([])
            for item in range(0, len(Levels[track])):
                button = DirectButton(parent=self.trackRows[track], image=(self.upButton, self.downButton, self.rolloverButton, self.flatButton), geom=self.invModels[track][item], text='50', text_scale=0.04, text_align=TextNode.ARight, geom_scale=0.75, geom_pos=(-0.01, -0.1, 0), text_fg=Vec4(1, 1, 1, 1), text_pos=(0.07, -0.04), relief=None, image_color=(0, 0.6, 1, 1), pos=(self.ButtonXOffset + item * self.ButtonXSpacing, -0.1, 0), command=self.__handleSelection, extraArgs=[track, item])
                button.bind(ENTER, lambda x, track=track, item=item, button=button, self=self: self.showDetail(track, item))
                button.bind(EXIT, lambda x, track=track, item=item, button=button, self=self: self.hideDetail())
                self.buttons[track].append(button)

        return
        return

    def __handleSelection(self, track, level):
        if self.activateMode == 'purchaseDelete' or self.activateMode == 'bookDelete' or self.activateMode == 'storePurchaseDelete':
            if self.numItem(track, level):
                self.useItem(track, level)
                self.updateGUI(track, level)
                messenger.send('inventory-deletion', [track, level])
                self.showDetail(track, level)
        else:
            if self.activateMode == 'purchase' or self.activateMode == 'storePurchase':
                messenger.send('inventory-selection', [track, level])
                self.showDetail(track, level)
            else:
                messenger.send('inventory-selection', [track, level])
        return

    def __handleRun(self):
        messenger.send('inventory-run')
        return

    def __handleSOS(self):
        messenger.send('inventory-sos')
        return

    def __handlePass(self):
        messenger.send('inventory-pass')
        return

    def __handleBackToPlayground(self):
        messenger.send('inventory-back-to-playground')
        return

    def showDetail(self, track, level):
        self.totalLabel.hide()
        self.detailNameLabel.show()
        self.detailNameLabel.configure(text=AvPropStrings[track][level], image_image=self.invModels[track][level])
        self.detailNameLabel.configure(image_scale=20, image_pos=(-0.2, 0, -2.2))
        self.detailAmountLabel.show()
        self.detailAmountLabel.configure(text=Localizer.InventoryDetailAmount % {'numItems': self.numItem(track, level), 'maxItems': self.getMax(track, level)})
        self.detailDataLabel.show()
        self.detailDataLabel.configure(text=Localizer.InventoryDetailData % {'accuracy': AvTrackAccStrings[track], 'damageString': self.getToonupDmgStr(track, level), 'damage': getAvPropDamage(track, level, self.toon.experience.getExp(track)), 'singleOrGroup': self.getSingleGroupStr(track, level)})
        if self.itemIsCredit(track, level):
            self.setDetailCredit(track, (level + 1) * self.__battleCreditMultiplier * self.__invasionCreditMultiplier)
        else:
            self.setDetailCredit(track, None)
        self.detailCreditLabel.show()
        return
        return

    def setDetailCredit(self, track, credit):
        if credit != None:
            if self.toon.earnedExperience:
                maxCredit = ExperienceCap - self.toon.earnedExperience[track]
                credit = min(credit, maxCredit)
            credit = int(credit * 10 + 0.5)
            if credit % 10 == 0:
                credit /= 10
            else:
                credit /= 10.0
        if self.detailCredit == credit:
            return
        if credit != None:
            self.detailCreditLabel['text'] = Localizer.InventorySkillCredit % credit
            if self.detailCredit == None:
                self.detailCreditLabel['text_fg'] = (
                 0.05, 0.14, 0.4, 1)
        else:
            self.detailCreditLabel['text'] = Localizer.InventorySkillCreditNone
            self.detailCreditLabel['text_fg'] = (0.5, 0.0, 0.0, 1.0)
        self.detailCredit = credit
        return

    def hideDetail(self):
        self.totalLabel.show()
        self.detailNameLabel.hide()
        self.detailAmountLabel.hide()
        self.detailDataLabel.hide()
        self.detailCreditLabel.hide()
        return

    def noDetail(self):
        self.totalLabel.hide()
        self.detailNameLabel.hide()
        self.detailAmountLabel.hide()
        self.detailDataLabel.hide()
        self.detailCreditLabel.hide()
        return

    def setActivateMode(self, mode, heal=1, trap=1, lure=1, bldg=0, creditLevel=None, tutorialFlag=0):
        self.notify.debug('setActivateMode() mode:%s heal:%s trap:%s lure:%s bldg:%s' % (mode, heal, trap, lure, bldg))
        self.previousActivateMode = self.activateMode
        self.activateMode = mode
        self.deactivateButtons()
        self.heal = heal
        self.trap = trap
        self.lure = lure
        self.bldg = bldg
        self.battleCreditLevel = creditLevel
        self.tutorialFlag = tutorialFlag
        self.__activateButtons()
        return None
        return

    def setActivateModeBroke(self):
        if self.activateMode == 'storePurchase':
            self.setActivateMode('storePurchaseBroke')
        else:
            if self.activateMode == 'purchase':
                self.setActivateMode('purchaseBroke')
            else:
                self.notify.error('Unexpected mode in setActivateModeBroke(): %s' % self.activateMode)

    def deactivateButtons(self):
        if self.previousActivateMode == 'book':
            self.bookDeactivateButtons()
        else:
            if self.previousActivateMode == 'bookDelete':
                self.bookDeleteDeactivateButtons()
            else:
                if self.previousActivateMode == 'purchaseDelete':
                    self.purchaseDeleteDeactivateButtons()
                else:
                    if self.previousActivateMode == 'purchase':
                        self.purchaseDeactivateButtons()
                    else:
                        if self.previousActivateMode == 'purchaseBroke':
                            self.purchaseBrokeDeactivateButtons()
                        else:
                            if self.previousActivateMode == 'battle':
                                self.battleDeactivateButtons()
                            else:
                                if self.previousActivateMode == 'storePurchaseDelete':
                                    self.storePurchaseDeleteDeactivateButtons()
                                else:
                                    if self.previousActivateMode == 'storePurchase':
                                        self.storePurchaseDeactivateButtons()
                                    else:
                                        if self.previousActivateMode == 'storePurchaseBroke':
                                            self.storePurchaseBrokeDeactivateButtons()
                                        else:
                                            self.notify.error('No such mode as %s' % self.previousActivateMode)
        return None
        return

    def __activateButtons(self):
        if hasattr(self, 'activateMode'):
            if self.activateMode == 'book':
                self.bookActivateButtons()
            else:
                if self.activateMode == 'bookDelete':
                    self.bookDeleteActivateButtons()
                else:
                    if self.activateMode == 'purchaseDelete':
                        self.purchaseDeleteActivateButtons()
                    else:
                        if self.activateMode == 'purchase':
                            self.purchaseActivateButtons()
                        else:
                            if self.activateMode == 'purchaseBroke':
                                self.purchaseBrokeActivateButtons()
                            else:
                                if self.activateMode == 'battle':
                                    self.battleActivateButtons()
                                else:
                                    if self.activateMode == 'storePurchaseDelete':
                                        self.storePurchaseDeleteActivateButtons()
                                    else:
                                        if self.activateMode == 'storePurchase':
                                            self.storePurchaseActivateButtons()
                                        else:
                                            if self.activateMode == 'storePurchaseBroke':
                                                self.storePurchaseBrokeActivateButtons()
                                            else:
                                                self.notify.error('No such mode as %s' % self.activateMode)
        return None
        return

    def bookActivateButtons(self):
        self.setPos(0, 0, 0.52)
        self.setScale(1.0)
        self.detailFrame.setPos(0.1, 0, -0.855)
        self.detailFrame.setScale(0.75)
        self.deleteEnterButton.hide()
        self.deleteEnterButton.setPos(1.029, 0, -0.639)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.hide()
        self.deleteExitButton.setPos(1.029, 0, -0.639)
        self.deleteExitButton.setScale(0.75)
        self.invFrame.reparentTo(self)
        self.invFrame.setPos(0, 0, 0)
        self.invFrame.setScale(1)
        self.deleteEnterButton['command'] = self.setActivateMode
        self.deleteEnterButton['extraArgs'] = ['bookDelete']
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        self.makeBookUnpressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return None
        return

    def bookDeactivateButtons(self):
        self.deleteEnterButton['command'] = None
        return
        return

    def bookDeleteActivateButtons(self):
        messenger.send('enterBookDelete')
        self.setPos(-0.2, 0, 0.4)
        self.setScale(0.8)
        self.deleteEnterButton.hide()
        self.deleteEnterButton.setPos(1.029, 0, -0.639)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.show()
        self.deleteExitButton.setPos(1.029, 0, -0.639)
        self.deleteExitButton.setScale(0.75)
        self.deleteHelpText.show()
        self.invFrame.reparentTo(self)
        self.invFrame.setPos(0, 0, 0)
        self.invFrame.setScale(1)
        self.deleteExitButton['command'] = self.setActivateMode
        self.deleteExitButton['extraArgs'] = [self.previousActivateMode]
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0:
                            self.makeUnpressable(button)
                        else:
                            self.makeDeletePressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return

    def bookDeleteDeactivateButtons(self):
        messenger.send('exitBookDelete')
        self.deleteHelpText.hide()
        self.deleteDeactivateButtons()
        return

    def purchaseDeleteActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if self.purchaseFrame == None:
            self.loadPurchaseFrame()
        self.purchaseFrame.show()
        self.invFrame.reparentTo(self.purchaseFrame)
        self.invFrame.setPos(-0.23, 0, 0.50756)
        self.invFrame.setScale(0.793894)
        self.detailFrame.setPos(1.1, 0, 0)
        self.detailFrame.setScale(1.25)
        self.deleteEnterButton.hide()
        self.deleteEnterButton.setPos(-0.441, 0, -0.917)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.show()
        self.deleteExitButton.setPos(-0.441, 0, -0.917)
        self.deleteExitButton.setScale(0.75)
        self.deleteExitButton['command'] = self.setActivateMode
        self.deleteExitButton['extraArgs'] = [self.previousActivateMode]
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0:
                            self.makeUnpressable(button)
                        else:
                            self.makeDeletePressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return
        return

    def purchaseDeleteDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.purchaseFrame.hide()
        self.deleteDeactivateButtons()
        return

    def storePurchaseDeleteActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if self.storePurchaseFrame == None:
            self.loadStorePurchaseFrame()
        self.storePurchaseFrame.show()
        self.invFrame.reparentTo(self.storePurchaseFrame)
        self.invFrame.setPos(-0.23, 0, 0.50756)
        self.invFrame.setScale(0.793894)
        self.detailFrame.setPos(1.1, 0, 0)
        self.detailFrame.setScale(1.25)
        self.deleteEnterButton.hide()
        self.deleteEnterButton.setPos(-0.441, 0, -0.917)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.show()
        self.deleteExitButton.setPos(-0.441, 0, -0.917)
        self.deleteExitButton.setScale(0.75)
        self.deleteExitButton['command'] = self.setActivateMode
        self.deleteExitButton['extraArgs'] = [self.previousActivateMode]
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0:
                            self.makeUnpressable(button)
                        else:
                            self.makeDeletePressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return
        return

    def storePurchaseDeleteDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.storePurchaseFrame.hide()
        self.deleteDeactivateButtons()
        return

    def storePurchaseBrokeActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if self.storePurchaseFrame == None:
            self.loadStorePurchaseFrame()
        self.storePurchaseFrame.show()
        self.invFrame.reparentTo(self.storePurchaseFrame)
        self.invFrame.setPos(-0.23, 0, 0.50756)
        self.invFrame.setScale(0.793894)
        self.detailFrame.setPos(1.1, 0, 0)
        self.detailFrame.setScale(1.25)
        self.deleteEnterButton.show()
        self.deleteEnterButton.setPos(-0.441, 0, -0.917)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.hide()
        self.deleteExitButton.setPos(-0.441, 0, -0.917)
        self.deleteExitButton.setScale(0.75)
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        self.makeUnpressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return
        return

    def storePurchaseBrokeDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.storePurchaseFrame.hide()
        return

    def deleteActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0, 0, 0)
        self.setScale(1)
        self.deleteEnterButton.hide()
        self.deleteExitButton.show()
        self.deleteExitButton['command'] = self.setActivateMode
        self.deleteExitButton['extraArgs'] = [self.previousActivateMode]
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0:
                            self.makeUnpressable(button)
                        else:
                            self.makePressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return None
        return

    def deleteDeactivateButtons(self):
        self.deleteExitButton['command'] = None
        return
        return

    def purchaseActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if self.purchaseFrame == None:
            self.loadPurchaseFrame()
        self.purchaseFrame.show()
        self.invFrame.reparentTo(self.purchaseFrame)
        self.invFrame.setPos(-0.23, 0, 0.50756)
        self.invFrame.setScale(0.793894)
        self.detailFrame.setPos(1.1, 0, 0)
        self.detailFrame.setScale(1.25)
        totalProps = self.totalProps
        maxProps = self.toon.getMaxCarry()
        self.deleteEnterButton.show()
        self.deleteEnterButton.setPos(-0.441, 0, -0.917)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.hide()
        self.deleteExitButton.setPos(-0.441, 0, -0.917)
        self.deleteExitButton.setScale(0.75)
        self.deleteEnterButton['command'] = self.setActivateMode
        self.deleteEnterButton['extraArgs'] = ['purchaseDelete']
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) >= self.getMax(track, level) or totalProps == maxProps:
                            self.makeUnpressable(button)
                        else:
                            self.makePressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return None
        return

    def purchaseDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.purchaseFrame.hide()
        return

    def storePurchaseActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if self.storePurchaseFrame == None:
            self.loadStorePurchaseFrame()
        self.storePurchaseFrame.show()
        self.invFrame.reparentTo(self.storePurchaseFrame)
        self.invFrame.setPos(-0.23, 0, 0.50756)
        self.invFrame.setScale(0.793894)
        self.detailFrame.setPos(1.1, 0, 0)
        self.detailFrame.setScale(1.25)
        totalProps = self.totalProps
        maxProps = self.toon.getMaxCarry()
        self.deleteEnterButton.show()
        self.deleteEnterButton.setPos(-0.441, 0, -0.917)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.hide()
        self.deleteExitButton.setPos(-0.441, 0, -0.917)
        self.deleteExitButton.setScale(0.75)
        self.deleteEnterButton['command'] = self.setActivateMode
        self.deleteEnterButton['extraArgs'] = ['storePurchaseDelete']
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) >= self.getMax(track, level) or totalProps == maxProps:
                            self.makeUnpressable(button)
                        else:
                            self.makePressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return None
        return

    def storePurchaseDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.storePurchaseFrame.hide()
        return

    def purchaseBrokeActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if self.purchaseFrame == None:
            self.loadPurchaseFrame()
        self.purchaseFrame.show()
        self.invFrame.reparentTo(self.purchaseFrame)
        self.invFrame.setPos(-0.23, 0, 0.50756)
        self.invFrame.setScale(0.793894)
        self.detailFrame.setPos(1.1, 0, 0)
        self.detailFrame.setScale(1.25)
        self.deleteEnterButton.show()
        self.deleteEnterButton.setPos(-0.441, 0, -0.917)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.hide()
        self.deleteExitButton.setPos(-0.441, 0, -0.917)
        self.deleteExitButton.setScale(0.75)
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        self.makeUnpressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return
        return

    def purchaseBrokeDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.purchaseFrame.hide()
        return

    def battleActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0, 0, 0.1)
        self.setScale(1)
        if self.battleFrame == None:
            self.loadBattleFrame()
        self.battleFrame.show()
        self.battleFrame.setScale(0.9)
        self.invFrame.reparentTo(self.battleFrame)
        self.invFrame.setPos(-0.25, 0, 0.35)
        self.invFrame.setScale(1)
        self.detailFrame.setPos(1.05, 0, -0.08)
        self.detailFrame.setScale(1)
        self.deleteEnterButton.hide()
        self.deleteExitButton.hide()
        if self.bldg == 1:
            self.runButton.hide()
            self.sosButton.hide()
            self.passButton.show()
        else:
            if self.tutorialFlag == 1:
                self.runButton.hide()
                self.sosButton.hide()
                self.passButton.hide()
            else:
                self.runButton.show()
                self.sosButton.show()
                self.passButton.show()
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in range(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0 or track == HEAL_TRACK and not self.heal or track == TRAP_TRACK and not self.trap or track == LURE_TRACK and not self.lure:
                            self.makeUnpressable(button)
                        else:
                            if self.itemIsCredit(track, level):
                                self.makePressable(button)
                            else:
                                self.makeNoncreditPressable(button)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        return None
        return

    def battleDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.battleFrame.hide()
        return

    def itemIsUsable(self, track, level):
        curSkill = self.toon.experience.getExp(track)
        if curSkill < Levels[track][level]:
            return 0
        else:
            return 1

    def itemIsCredit(self, track, level):
        if self.toon.earnedExperience:
            if self.toon.earnedExperience[track] >= ExperienceCap:
                return 0
        if self.battleCreditLevel == None:
            return 1
        else:
            return level < self.battleCreditLevel
        return

    def getCurAndNextExpValues(self, track):
        curSkill = self.toon.experience.getExp(track)
        retVal = MaxSkill
        for amount in Levels[track]:
            if curSkill < amount:
                retVal = amount
                return (
                 curSkill, retVal)

        return (
         curSkill, retVal)

    def makePressable(self, button):
        button.configure(image0_image=self.upButton, image2_image=self.rolloverButton, text_color=self.PressableTextColor, geom_color=self.PressableGeomColor, commandButtons=(LMB,))
        button.configure(image_color=self.PressableImageColor)
        return

    def makeNoncreditPressable(self, button):
        button.configure(image0_image=self.upButton, image2_image=self.rolloverButton, text_color=self.PressableTextColor, geom_color=self.PressableGeomColor, commandButtons=(LMB,))
        button.configure(image_color=self.NoncreditPressableImageColor)
        return

    def makeDeletePressable(self, button):
        button.configure(image0_image=self.upButton, image2_image=self.rolloverButton, text_color=self.PressableTextColor, geom_color=self.PressableGeomColor, commandButtons=(LMB,))
        button.configure(image_color=self.DeletePressableImageColor)
        return

    def makeUnpressable(self, button):
        button.configure(text_color=self.UnpressableTextColor, geom_color=self.UnpressableGeomColor, image_image=self.flatButton, commandButtons=())
        button.configure(image_color=self.UnpressableImageColor)
        return

    def makeBookUnpressable(self, button):
        button.configure(text_color=self.BookUnpressableTextColor, geom_color=self.BookUnpressableGeomColor, image_image=self.flatButton, commandButtons=())
        button.configure(image0_color=self.BookUnpressableImage0Color, image2_color=self.BookUnpressableImage2Color)
        return

    def hideTrack(self, trackIndex):
        self.trackNameLabels[trackIndex].show()
        self.trackBars[trackIndex].hide()
        for levelIndex in range(0, len(Levels[trackIndex])):
            self.buttons[trackIndex][levelIndex].hide()

    def showTrack(self, trackIndex):
        self.trackNameLabels[trackIndex].show()
        self.trackBars[trackIndex].show()
        for levelIndex in range(0, len(Levels[trackIndex])):
            self.buttons[trackIndex][levelIndex].show()

        curExp, nextExp = self.getCurAndNextExpValues(trackIndex)
        self.trackBars[trackIndex]['range'] = nextExp
        self.trackBars[trackIndex]['text'] = Localizer.InventoryTrackExp % {'curExp': curExp, 'nextExp': nextExp}
        return

    def updateInvString(self, invString):
        InventoryBase.InventoryBase.updateInvString(self, invString)
        self.updateGUI()
        return None
        return

    def updateButtonText(self, track, level):
        button = self.buttons[track][level]
        button['text'] = str(self.numItem(track, level))
        return

    def buttonBoing(self, track, level):
        button = self.buttons[track][level]
        oldScale = button.getScale()
        s = Sequence(button.scaleInterval(0.1, oldScale * 1.333, blendType='easeOut'), button.scaleInterval(0.1, oldScale, blendType='easeIn'), name='inventoryButtonBoing-' + str(self.this))
        s.play()

    def updateGUI(self, track=None, level=None):
        self.updateTotalPropsText()
        if track == None and level == None:
            for track in range(len(Tracks)):
                curExp, nextExp = self.getCurAndNextExpValues(track)
                self.trackBars[track]['text'] = Localizer.InventoryTrackExp % {'curExp': curExp, 'nextExp': nextExp}
                self.trackBars[track]['value'] = curExp
                for level in range(0, len(Levels[track])):
                    self.updateButtonText(track, level)

        else:
            if track != None and level != None:
                self.updateButtonText(track, level)
            else:
                self.notify.error('Invalid use of updateGUI')
        self.__activateButtons()
        return
        return

    def getSingleGroupStr(self, track, level):
        if track == HEAL_TRACK:
            if isGroup(track, level):
                return Localizer.InventoryAffectsAllToons
            else:
                return Localizer.InventoryAffectsOneToon
        else:
            if isGroup(track, level):
                return Localizer.InventoryAffectsAllCogs
            else:
                return Localizer.InventoryAffectsOneCog

    def getToonupDmgStr(self, track, level):
        if track == HEAL_TRACK:
            return Localizer.InventoryHealString
        else:
            return Localizer.InventoryDamageString

    def deleteItem(self, track, level):
        if self.numItem(track, level) > 0:
            self.useItem(track, level)
            self.updateGUI(track, level)
        return

    def loadBattleFrame(self):
        battleModels = loader.loadModelOnce('phase_3.5/models/gui/battle_gui')
        self.battleFrame = DirectFrame(relief=None, image=battleModels.find('**/BATTLE_Menu'), image_scale=0.8, parent=self)
        self.runButton = DirectButton(parent=self.battleFrame, relief=None, pos=(0.68, 0, -0.396), text=Localizer.InventoryRun, text_scale=0.05, text_pos=(0, -0.02), text_fg=Vec4(1, 1, 1, 1), textMayChange=0, image=(self.upButton, self.downButton, self.rolloverButton), image_scale=1.05, image_color=(0, 0.6, 1, 1), command=self.__handleRun)
        self.sosButton = DirectButton(parent=self.battleFrame, relief=None, pos=(0.91, 0, -0.396), text=Localizer.InventorySOS, text_scale=0.05, text_pos=(0, -0.02), text_fg=Vec4(1, 1, 1, 1), textMayChange=0, image=(self.upButton, self.downButton, self.rolloverButton), image_scale=1.05, image_color=(0, 0.6, 1, 1), command=self.__handleSOS)
        self.passButton = DirectButton(parent=self.battleFrame, relief=None, pos=(0.91, 0, -0.237), text=Localizer.InventoryPass, text_scale=0.05, text_pos=(0, -0.02), text_fg=Vec4(1, 1, 1, 1), textMayChange=0, image=(self.upButton, self.downButton, self.rolloverButton), image_scale=1.05, image_color=(0, 0.6, 1, 1), command=self.__handlePass)
        self.tutText = DirectFrame(parent=self.battleFrame, relief=None, pos=(0.15, 0, -0.1133), scale=0.143, image=getDefaultDialogGeom(), image_scale=5.125, image_pos=(0, 0, -0.65), image_color=ToontownGlobals.GlobalDialogColor, text=Localizer.InventoryClickToAttack, textMayChange=0)
        self.tutText.hide()
        self.tutArrows = BlinkingArrows.BlinkingArrows(parent=self.battleFrame)
        battleModels.removeNode()
        self.battleFrame.hide()
        return
        return

    def loadPurchaseFrame(self):
        purchaseModels = loader.loadModelOnce('phase_4/models/gui/purchase_gui')
        self.purchaseFrame = DirectFrame(relief=None, image=purchaseModels.find('**/PurchasePanel'), image_pos=(-0.21, 0, 0.08), parent=self)
        self.purchaseFrame.setX(-0.06)
        self.purchaseFrame.hide()
        purchaseModels.removeNode()
        return
        return

    def loadStorePurchaseFrame(self):
        storePurchaseModels = loader.loadModelOnce('phase_4/models/gui/gag_shop_purchase_gui')
        self.storePurchaseFrame = DirectFrame(relief=None, image=storePurchaseModels.find('**/gagShopPanel'), image_pos=(-0.21, 0, 0.18), parent=self)
        self.storePurchaseFrame.hide()
        storePurchaseModels.removeNode()
        return
        return

    def buttonLookup(self, track, level):
        return self.invModels[track][level]

    def enterTrackFrame(self, track, guiItem):
        messenger.send('enterTrackFrame', [track])

    def exitTrackFrame(self, track, guiItem):
        messenger.send('exitTrackFrame', [track])