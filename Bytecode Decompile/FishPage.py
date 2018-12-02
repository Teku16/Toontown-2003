import ToontownGlobals, ShtikerPage
from DirectGui import *
import Localizer, FishingCodes, ToontownDialog
PICKER_START_POS = (
 -0.555, 0, 0)
FP_NORMAL = 0
FP_RELEASE = 1

class FishPage(ShtikerPage.ShtikerPage):
    __module__ = __name__

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.fishes = []
        self.avatar = None
        self.state = NORMAL
        return

    def setAvatar(self, av):
        self.avatar = av

    def getAvatar(self):
        return self.avatar

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.title = DirectLabel(parent=self, relief=None, text=Localizer.FishPageTitle, text_scale=0.12, pos=(0, 0, 0.6))
        self.fishPanel = DirectLabel(parent=self, pos=(0.45, 0, 0), relief=None, state=NORMAL, image=getDefaultDialogGeom(), image_scale=(0.6, 1, 0.6), text='', text_scale=0.055, text_fg=(0, 0, 0, 1), text_pos=(0, 0.225, 0), text_font=ToontownGlobals.getInterfaceFont(), text_wordwrap=7.25)
        buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
        self.fishPanelCancel = DirectButton(parent=self.fishPanel, pos=(0.25, 0, -0.25), relief=None, state=NORMAL, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), image_scale=(0.6, 1, 0.6), command=self.hideFishPanel)
        self.fishPanel.hide()
        del buttons
        self.releasePanel = DirectFrame(relief=None, geom=getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(1, 1, 1.75), text=Localizer.FishPageOverflow, text_pos=(0, 0.7), text_scale=0.07, pos=(0, 0, 0))
        self.releasePanel.hide()
        self.newFishLabel = DirectLabel(parent=self.releasePanel, relief=None, text=Localizer.FishingItemFound, text_scale=0.07, pos=(-0.3, 0, 0.45))
        self.newFishButton = DirectButton(parent=self.releasePanel, text='', text_scale=0.07, text_align=TextNode.ALeft, text1_bg=Vec4(1, 1, 0, 1), text2_bg=Vec4(0.5, 0.9, 1, 1), text3_fg=Vec4(0.4, 0.8, 0.4, 1), command=self.releaseFish, pos=(-0.25, 0, 0.325))
        self.oldFishLabel = DirectLabel(parent=self.releasePanel, relief=None, text=Localizer.FishPageOldFish, text_scale=0.07, pos=(-0.22, 0, 0.155))
        self.makePicker()
        self.updatePage()
        return

    def unload(self):
        del self.title
        del self.fishPanel
        self.releasePanel.destroy()
        del self.releasePanel
        del self.newFishLabel
        del self.newFishButton
        del self.oldFishLabel
        del self.picker
        ShtikerPage.ShtikerPage.unload(self)

    def makePicker(self):
        gui = loader.loadModelOnce('phase_3.5/models/gui/friendslist_gui')
        self.picker = DirectScrolledList(parent=self, relief=None, pos=PICKER_START_POS, incButton_image=(gui.find('**/FndsLst_ScrollUp'), gui.find('**/FndsLst_ScrollDN'), gui.find('**/FndsLst_ScrollUp_Rllvr'), gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_scale=(1.3, 1.3, -1.3), incButton_pos=(0.1, 0, -0.51), incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(gui.find('**/FndsLst_ScrollUp'), gui.find('**/FndsLst_ScrollDN'), gui.find('**/FndsLst_ScrollUp_Rllvr'), gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_scale=(1.3, 1.3, 1.3), decButton_pos=(0.1, 0, 0.51), decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(-0.237, 0, 0.361), itemFrame_scale=1.0, itemFrame_relief=SUNKEN, itemFrame_frameSize=(-0.05, 0.75, -0.83, 0.1), itemFrame_frameColor=(0.85, 0.95, 1, 1), itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=10, items=[])
        gui.removeNode()
        return

    def updatePage(self):
        self.hideFishPanel()
        newFishes = toonbase.localToon.fishes
        for fish, fishButton in self.fishes[:]:
            self.picker.removeItem(fishButton)
            fishButton.destroy()
            self.fishes.remove([fish, fishButton])

        for fish in newFishes:
            fishButton = self.makeFishButton(fish)
            self.picker.addItem(fishButton)
            self.fishes.append([fish, fishButton])

    def makeFishButton(self, fish):
        return DirectButton(relief=None, text=FishingCodes.getFishName(fish), text_scale=0.08, text_align=TextNode.ALeft, text1_bg=Vec4(1, 1, 0, 1), text2_bg=Vec4(0.5, 0.9, 1, 1), text3_fg=Vec4(0.4, 0.8, 0.4, 1), command=self.showFishPanel, extraArgs=[fish])
        return

    def showFishPanel(self, fish):
        self.fishPanel['text'] = FishingCodes.getFishName(fish)
        self.fishPanel.show()

    def hideFishPanel(self):
        self.fishPanel.hide()

    def showReleaseFishPanel(self, newFish):
        self.state = FP_RELEASE
        for fish, button in self.fishes:
            button['command'] = self.handleReleaseFish

        self.newFishButton['text'] = FishingCodes.getFishName(newFish)
        self.newFishButton['extraArgs'] = [newFish]
        self.newFishButton.resetFrameSize()
        self.releasePanel.show()
        self.releasePanel['state'] = 'normal'
        self.picker.setScale(0.8)
        self.picker.setPos(-0.1, 0, -0.35)
        self.picker.reparentTo(self.releasePanel)

    def hideReleaseFishPanel(self):
        self.releasePanel.hide()
        self.picker.setScale(1.0)
        self.picker.setPos(*PICKER_START_POS)
        self.picker.reparentTo(self)
        for fish, button in self.fishes:
            button['command'] = self.showFishPanel

        self.state = FP_NORMAL

    def handleReleaseFish(self, fish):
        self.verify = ToontownDialog.GlobalDialog(doneEvent='verifyDone', message=Localizer.FishPageVerify % FishingCodes.getFishName(fish), style=ToontownDialog.TwoChoice)
        self.verify.show()
        self.accept('verifyDone', self.handleVerifyReleaseFish, extraArgs=[fish])

    def handleVerifyReleaseFish(self, fish):
        status = self.verify.doneStatus
        self.ignore('verifyDone')
        self.verify.cleanup()
        del self.verify
        if status == 'ok':
            self.releaseFish(fish)

    def releaseFish(self, fish):
        self.avatar.fishingSpot.b_fishReleased(fish)
        self.hideReleaseFishPanel()
        if hasattr(self, 'verify'):
            self.ignore('verifyDone')
            self.verify.cleanup()
            del self.verify

    def forceReleaseFish(self):
        newFish = self.newFishButton['extraArgs']
        self.releaseFish(*newFish)