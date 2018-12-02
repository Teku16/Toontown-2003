from DirectGui import *
import StateData, Localizer, ToontownDialog, ToontownGlobals

class DisplaySettingsDialog(DirectFrame, StateData.StateData):
    __module__ = __name__
    ApplyTimeoutSeconds = 15
    TimeoutCountdownTask = 'DisplaySettingsTimeoutCountdown'

    def __init__(self):
        DirectFrame.__init__(self, pos=(0, 0, 0.3), relief=None, image=getDefaultDialogGeom(), image_scale=(1.6, 1, 1.2), image_pos=(0, 0, -0.05), image_color=ToontownGlobals.GlobalDialogColor, text=Localizer.DisplaySettingsTitle, text_scale=0.12, text_pos=(0, 0.4), borderWidth=(0.01, 0.01), sortOrder=NO_FADE_SORT_INDEX)
        StateData.StateData.__init__(self, 'display-settings-done')
        self.initialiseoptions(DisplaySettingsDialog)
        return

    def unload(self):
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()
        DirectFrame.destroy(self)
        return

    def load(self):
        if self.isLoaded == 1:
            return None
        self.isLoaded = 1
        self.anyChanged = 0
        self.screenSizes = ((640, 480), (800, 600), (1024, 768), (1280, 1024), (1600, 1200))
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        gui = loader.loadModelOnce('phase_3.5/models/gui/friendslist_gui')
        nameShopGui = loader.loadModelOnce('phase_3/models/gui/nameshop_gui')
        circle = nameShopGui.find('**/namePanelCircle')
        innerCircle = circle.copyTo(hidden)
        innerCircle.setPos(0, 0, 0.2)
        self.c1b = circle.copyTo(self, -1)
        self.c1b.setColor(0, 0, 0, 1)
        self.c1b.setPos(0.044, 0, -0.21)
        self.c1b.setScale(0.4)
        c1f = circle.copyTo(self.c1b)
        c1f.setColor(1, 1, 1, 1)
        c1f.setScale(0.9)
        self.c2b = circle.copyTo(self, -2)
        self.c2b.setColor(0, 0, 0, 1)
        self.c2b.setPos(0.044, 0, -0.3)
        self.c2b.setScale(0.4)
        c2f = circle.copyTo(self.c2b)
        c2f.setColor(1, 1, 1, 1)
        c2f.setScale(0.9)
        self.introText = DirectLabel(parent=self, relief=None, scale=0.06, text=Localizer.DisplaySettingsIntro, text_wordwrap=25, text_align=TextNode.ALeft, pos=(-0.725, 0, 0.3))
        self.introTextSimple = DirectLabel(parent=self, relief=None, scale=0.06, text=Localizer.DisplaySettingsIntroSimple, text_wordwrap=25, text_align=TextNode.ALeft, pos=(-0.725, 0, 0.3))
        self.apiLabel = DirectLabel(parent=self, relief=None, scale=0.06, text=Localizer.DisplaySettingsApi, text_align=TextNode.ARight, pos=(-0.08, 0, 0))
        self.apiMenu = DirectOptionMenu(parent=self, relief=RAISED, scale=0.06, items=['x'], pos=(0, 0, 0))
        self.screenSizeLabel = DirectLabel(parent=self, relief=None, scale=0.06, text=Localizer.DisplaySettingsResolution, text_align=TextNode.ARight, pos=(-0.08, 0, -0.1))
        self.screenSizeLeftArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'), gui.find('**/Horiz_Arrow_DN'), gui.find('**/Horiz_Arrow_Rllvr'), gui.find('**/Horiz_Arrow_UP')), scale=(-1.0, 1.0, 1.0), pos=(0.04, 0, -0.085), command=self.__doScreenSizeLeft)
        self.screenSizeRightArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'), gui.find('**/Horiz_Arrow_DN'), gui.find('**/Horiz_Arrow_Rllvr'), gui.find('**/Horiz_Arrow_UP')), pos=(0.54, 0, -0.085), command=self.__doScreenSizeRight)
        self.screenSizeValueText = DirectLabel(parent=self, relief=None, text='x', text_align=TextNode.ACenter, text_scale=0.06, pos=(0.29, 0, -0.1))
        self.windowedButton = DirectCheckButton(parent=self, relief=None, text=Localizer.DisplaySettingsWindowed, text_align=TextNode.ALeft, text_scale=0.6, scale=0.1, boxImage=innerCircle, boxImageScale=2.5, boxImageColor=VBase4(0, 0.25, 0.5, 1), boxRelief=None, pos=(0.1, 0, -0.22), command=self.__doWindowed)
        self.fullscreenButton = DirectCheckButton(parent=self, relief=None, text=Localizer.DisplaySettingsFullscreen, text_align=TextNode.ALeft, text_scale=0.6, scale=0.1, boxImage=innerCircle, boxImageScale=2.5, boxImageColor=VBase4(0, 0.25, 0.5, 1), boxRelief=None, pos=(0.1, 0, -0.31), command=self.__doFullscreen)
        self.apply = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.6, 1, 1), text=Localizer.DisplaySettingsApply, text_scale=0.06, text_pos=(0, -0.02), pos=(0.52, 0, -0.53), command=self.__apply)
        self.cancel = DirectButton(parent=self, relief=None, text=Localizer.DisplaySettingsCancel, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.6, 1, 1), text_scale=0.06, text_pos=(0, -0.02), pos=(0.2, 0, -0.53), command=self.__cancel)
        guiButton.removeNode()
        gui.removeNode()
        nameShopGui.removeNode()
        innerCircle.removeNode()
        self.hide()
        return

    def enter(self, changeDisplaySettings):
        if self.isEntered == 1:
            return None
        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()
        self.applyDialog = None
        self.timeoutDialog = None
        self.restoreDialog = None
        self.revertDialog = None
        base.transitions.fadeScreen(0.5)
        properties = base.win.getProperties()
        self.screenSizeIndex = self.chooseClosestScreenSize(properties.getXSize(), properties.getYSize())
        self.fullscreen = properties.getFullscreen()
        self.updateApiMenu(changeDisplaySettings)
        self.updateWindowed()
        self.updateScreenSize()
        if changeDisplaySettings:
            self.introText.show()
            self.introTextSimple.hide()
            if len(self.apis) > 1:
                self.apiLabel.show()
                self.apiMenu.show()
            else:
                self.apiLabel.hide()
                self.apiMenu.hide()
            self.windowedButton.show()
            self.fullscreenButton.show()
            self.c1b.show()
            self.c2b.show()
        else:
            self.introText.hide()
            self.introTextSimple.show()
            self.apiLabel.hide()
            self.apiMenu.hide()
            self.windowedButton.hide()
            self.fullscreenButton.hide()
            self.c1b.hide()
            self.c2b.hide()
        self.anyChanged = 0
        self.show()
        return
        return

    def exit(self):
        if self.isEntered == 0:
            return None
        self.isEntered = 0
        self.cleanupDialogs()
        base.transitions.noTransitions()
        taskMgr.remove(self.TimeoutCountdownTask)
        self.ignoreAll()
        self.hide()
        messenger.send(self.doneEvent, [self.anyChanged])
        return
        return

    def cleanupDialogs(self):
        if self.applyDialog != None:
            self.applyDialog.cleanup()
            self.applyDialog = None
        if self.timeoutDialog != None:
            self.timeoutDialog.cleanup()
            self.timeoutDialog = None
        if self.restoreDialog != None:
            self.restoreDialog.cleanup()
            self.restoreDialog = None
        if self.revertDialog != None:
            self.revertDialog.cleanup()
            self.revertDialog = None
        return

    def updateApiMenu(self, changeDisplaySettings):
        self.apis = []
        self.apiPipes = []
        if changeDisplaySettings:
            base.makeAllPipes()
        for pipe in base.pipeList:
            if pipe.isValid():
                self.apiPipes.append(pipe)
                self.apis.append(pipe.getInterfaceName())

        self.apiMenu['items'] = self.apis
        self.apiMenu.set(base.pipe.getInterfaceName())

    def updateWindowed(self):
        if self.fullscreen:
            self.windowedButton['indicatorValue'] = 0
            self.fullscreenButton['indicatorValue'] = 1
        else:
            self.windowedButton['indicatorValue'] = 1
            self.fullscreenButton['indicatorValue'] = 0

    def updateScreenSize(self):
        xSize, ySize = self.screenSizes[self.screenSizeIndex]
        self.screenSizeValueText['text'] = '%s x %s' % (xSize, ySize)
        if self.screenSizeIndex > 0:
            self.screenSizeLeftArrow.show()
        else:
            self.screenSizeLeftArrow.hide()
        if self.screenSizeIndex < len(self.screenSizes) - 1:
            self.screenSizeRightArrow.show()
        else:
            self.screenSizeRightArrow.hide()

    def chooseClosestScreenSize(self, currentXSize, currentYSize):
        for i in range(len(self.screenSizes)):
            xSize, ySize = self.screenSizes[i]
            if currentXSize == xSize and currentYSize == ySize:
                return i

        currentCount = currentXSize * currentYSize
        bestDiff = None
        bestI = None
        for i in range(len(self.screenSizes)):
            xSize, ySize = self.screenSizes[i]
            diff = abs(xSize * ySize - currentCount)
            if bestI == None or diff < bestDiff:
                bestI = i
                bestDiff = diff

        return bestI
        return

    def __doWindowed(self, value):
        self.fullscreen = 0
        self.updateWindowed()

    def __doFullscreen(self, value):
        self.fullscreen = 1
        self.updateWindowed()

    def __doScreenSizeLeft(self):
        if self.screenSizeIndex > 0:
            self.screenSizeIndex = self.screenSizeIndex - 1
            self.updateScreenSize()

    def __doScreenSizeRight(self):
        if self.screenSizeIndex < len(self.screenSizes) - 1:
            self.screenSizeIndex = self.screenSizeIndex + 1
            self.updateScreenSize()

    def __apply(self):
        self.cleanupDialogs()
        self.reparentTo(self.getParent(), 0)
        self.applyDialog = ToontownDialog.ToontownDialog(dialogName='DisplaySettingsApply', style=ToontownDialog.TwoChoice, text=Localizer.DisplaySettingsApplyWarning % self.ApplyTimeoutSeconds, text_wordwrap=15, fadeScreen=1, command=self.__applyDone)

    def __applyDone(self, command):
        self.applyDialog.cleanup()
        self.applyDialog = None
        self.reparentTo(self.getParent(), NO_FADE_SORT_INDEX)
        base.transitions.fadeScreen(0.5)
        if command != DIALOG_OK:
            return
        self.origPipe = base.pipe
        self.origProperties = base.win.getProperties()
        pipe = self.apiPipes[self.apiMenu.selectedIndex]
        properties = WindowProperties()
        xSize, ySize = self.screenSizes[self.screenSizeIndex]
        properties.setSize(xSize, ySize)
        properties.setFullscreen(self.fullscreen)
        if not self.resetDisplayProperties(pipe, properties):
            self.__revertBack(1)
            return
        self.reparentTo(self.getParent(), 0)
        self.timeoutDialog = ToontownDialog.ToontownDialog(dialogName='DisplaySettingsTimeout', style=ToontownDialog.TwoChoice, text=Localizer.DisplaySettingsAccept % self.ApplyTimeoutSeconds, text_wordwrap=15, fadeScreen=1, command=self.__timeoutDone)
        self.timeoutRemaining = self.ApplyTimeoutSeconds
        self.timeoutStart = None
        taskMgr.add(self.__timeoutCountdown, self.TimeoutCountdownTask)
        return

    def __timeoutCountdown(self, task):
        if self.timeoutStart == None:
            self.timeoutStart = globalClock.getRealTime()
        elapsed = int(globalClock.getFrameTime() - self.timeoutStart)
        remaining = max(self.ApplyTimeoutSeconds - elapsed, 0)
        if remaining < self.timeoutRemaining:
            self.timeoutRemaining = remaining
            self.timeoutDialog['text'] = (Localizer.DisplaySettingsAccept % remaining,)
        if remaining == 0:
            self.__timeoutDone('cancel')
            return Task.done
        return Task.cont
        return

    def __timeoutDone(self, command):
        taskMgr.remove(self.TimeoutCountdownTask)
        self.timeoutDialog.cleanup()
        self.timeoutDialog = None
        self.reparentTo(self.getParent(), NO_FADE_SORT_INDEX)
        base.transitions.fadeScreen(0.5)
        if command == DIALOG_OK:
            self.anyChanged = 1
            self.exit()
            return
        self.__revertBack(0)
        return
        return

    def __revertBack(self, reason):
        if not self.resetDisplayProperties(self.origPipe, self.origProperties):
            print "Error; couldn't restore original display settings!"
            toonbase.tcr.loginFSM.request('shutdown')
            toonbase.exitShow()
        self.reparentTo(self.getParent(), 0)
        if reason == 0:
            revertText = Localizer.DisplaySettingsRevertUser
        else:
            revertText = Localizer.DisplaySettingsRevertFailed
        self.revertDialog = ToontownDialog.ToontownDialog(dialogName='DisplaySettingsRevert', style=ToontownDialog.Acknowledge, text=revertText, text_wordwrap=15, fadeScreen=1, command=self.__revertDone)

    def __revertDone(self, command):
        self.revertDialog.cleanup()
        self.revertDialog = None
        self.reparentTo(self.getParent(), NO_FADE_SORT_INDEX)
        base.transitions.fadeScreen(0.5)
        return
        return

    def __cancel(self):
        self.exit()

    def resetDisplayProperties(self, pipe, properties):
        if base.win:
            currentProperties = base.win.getProperties()
        else:
            currentProperties = WindowProperties()
        newProperties = WindowProperties(currentProperties)
        newProperties.addProperties(properties)
        if base.pipe != pipe or currentProperties.getFullscreen() != newProperties.getFullscreen():
            base.pipe = pipe
            if not base.openMainWindow():
                return 0
            base.win.requestProperties(properties)
            NametagGlobals.setCamera(base.cam)
            base.graphicsEngine.renderFrame()
            base.graphicsEngine.renderFrame()
            if base.win.isClosed():
                self.notify.info('Window did not open, removing.')
                base.closeWindow(base.win)
                return 0
        else:
            base.win.requestProperties(properties)
        return 1