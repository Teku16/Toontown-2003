from ShowBaseGlobal import *
import ToontownGlobals, PandaObject, AvatarChoice, StateData, FSM, State, DownloadForceAcknowledge
from DirectGui import *
import Localizer, ToontownDialog, DirectNotifyGlobal, whrandom
MAX_AVATARS = 6
POSITIONS = (Vec3(-0.82, 0, 0.35), Vec3(0, 0, 0.35), Vec3(0.82, 0, 0.35), Vec3(-0.82, 0, -0.47), Vec3(0, 0, -0.47), Vec3(0.82, 0, -0.47))
COLORS = (
 Vec4(0.917, 0.164, 0.164, 1), Vec4(0.152, 0.75, 0.258, 1), Vec4(0.598, 0.402, 0.875, 1), Vec4(0.133, 0.59, 0.977, 1), Vec4(0.895, 0.348, 0.602, 1), Vec4(0.977, 0.816, 0.133, 1))
chooser_notify = DirectNotifyGlobal.directNotify.newCategory('AvatarChooser')

class AvatarChooser(PandaObject.PandaObject, StateData.StateData):
    __module__ = __name__

    def __init__(self, avatarList, parentFSM, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.choice = None
        self.avatarList = avatarList
        self.fsm = FSM.FSM('AvatarChooser', [
         State.State('Choose', self.enterChoose, self.exitChoose, [
          'CheckDownload']),
         State.State('CheckDownload', self.enterCheckDownload, self.exitCheckDownload, [
          'Choose'])], 'Choose', 'Choose')
        self.fsm.enterInitialState()
        self.parentFSM = parentFSM
        self.parentFSM.getCurrentState().addChild(self.fsm)
        return

    def enter(self):
        if self.isLoaded == 0:
            self.load()
        base.disableMouse()
        self.title.reparentTo(aspect2d)
        self.quitButton.show()
        if toonbase.tcr.loginInterface.supportsRelogin():
            self.logoutButton.show()
        self.pickAToonBG.reparentTo(base.camera)
        for panel in self.panelList:
            panel.show()
            self.accept(panel.doneEvent, self.__handlePanelDone)

    def exit(self):
        if self.isLoaded == 0:
            return None
        for panel in self.panelList:
            panel.hide()

        self.ignoreAll()
        self.title.reparentTo(hidden)
        self.quitButton.hide()
        self.logoutButton.hide()
        self.pickAToonBG.reparentTo(hidden)
        return

    def load(self, isPaid):
        if self.isLoaded == 1:
            return None
        self.isPaid = isPaid
        gui = loader.loadModelOnce('phase_3/models/gui/pick_a_toon_gui')
        gui2 = loader.loadModelOnce('phase_3/models/gui/quit_button')
        self.pickAToonBG = gui.find('**/av-chooser_FnlBG')
        self.pickAToonBG.reparentTo(hidden)
        self.pickAToonBG.setPos(0.0, 2.73, 0.0)
        self.pickAToonBG.setScale(1, 1, 1)
        self.title = OnscreenText(Localizer.AvatarChooserPickAToon, scale=0.125, parent=hidden, font=ToontownGlobals.getSignFont(), fg=(1, 0.9, 0.1, 1), pos=(0.0, 0.82))
        self.quitButton = DirectButton(image=(gui.find('**/QuitBtn_UP'), gui.find('**/QuitBtn_DN'), gui.find('**/QuitBtn_RLVR')), relief=None, text=Localizer.AvatarChooserQuit, text_font=ToontownGlobals.getSignFont(), text0_fg=(0.152, 0.75, 0.258, 1), text1_fg=(0.152, 0.75, 0.258, 1), text2_fg=(0.977, 0.816, 0.133, 1), text_pos=(0, -0.035), text_scale=0.1, scale=1.05, pos=(0, 0, -0.924), command=self.__handleQuit)
        self.logoutButton = DirectButton(relief=None, image=(gui2.find('**/QuitBtn_UP'), gui2.find('**/QuitBtn_DN'), gui2.find('**/QuitBtn_RLVR')), image_scale=1.15, text=Localizer.OptionsPageLogout, text_font=ToontownGlobals.getSignFont(), text0_fg=(0.152, 0.75, 0.258, 1), text1_fg=(0.152, 0.75, 0.258, 1), text2_fg=(0.977, 0.816, 0.133, 1), text_scale=0.1, text_pos=(0, -0.035), pos=(1.105, 0, -0.924), scale=0.5, command=self.__handleLogoutWithoutConfirm)
        self.logoutButton.hide()
        gui.removeNode()
        gui2.removeNode()
        self.panelList = []
        used_position_indexs = []
        for av in self.avatarList:
            panel = AvatarChoice.AvatarChoice(av, position=av.position, paid=isPaid)
            panel.setPos(POSITIONS[av.position])
            panel['image_color'] = COLORS[av.position]
            used_position_indexs.append(av.position)
            self.panelList.append(panel)

        for panelNum in range(0, MAX_AVATARS):
            if panelNum not in used_position_indexs:
                panel = AvatarChoice.AvatarChoice(position=panelNum)
                panel.setPos(POSITIONS[panelNum])
                panel['image_color'] = COLORS[panelNum]
                self.panelList.append(panel)

        if len(self.avatarList) > 0:
            self.initLookAtInfo()
        self.isLoaded = 1
        return

    def getLookAtPosition(self, toonHead, toonidx):
        lookAtChoice = whrandom.random()
        if len(self.used_panel_indexs) == 1:
            lookFwdPercent = 0.33
            lookAtOthersPercent = 0
        else:
            lookFwdPercent = 0.2
            if len(self.used_panel_indexs) == 2:
                lookAtOthersPercent = 0.4
            else:
                lookAtOthersPercent = 0.65
        lookRandomPercent = 1.0 - lookFwdPercent - lookAtOthersPercent
        if lookAtChoice < lookFwdPercent:
            self.IsLookingAt[toonidx] = 'f'
            return Vec3(0, 1.5, 0)
        else:
            if lookAtChoice < lookRandomPercent + lookFwdPercent or len(self.used_panel_indexs) == 1:
                self.IsLookingAt[toonidx] = 'r'
                return toonHead.getRandomForwardLookAtPoint()
            else:
                other_toon_idxs = []
                for i in range(len(self.IsLookingAt)):
                    if self.IsLookingAt[i] == toonidx:
                        other_toon_idxs.append(i)

                if len(other_toon_idxs) == 1:
                    IgnoreStarersPercent = 0.4
                else:
                    IgnoreStarersPercent = 0.2
                NoticeStarersPercent = 0.5
                bStareTargetTurnsToMe = 0
                if len(other_toon_idxs) == 0 or whrandom.random() < IgnoreStarersPercent:
                    other_toon_idxs = []
                    for i in self.used_panel_indexs:
                        if i != toonidx:
                            other_toon_idxs.append(i)

                    if whrandom.random() < NoticeStarersPercent:
                        bStareTargetTurnsToMe = 1
                lookingAtIdx = whrandom.choice(other_toon_idxs)
                if bStareTargetTurnsToMe:
                    self.IsLookingAt[lookingAtIdx] = toonidx
                    otherToonHead = None
                    for panel in self.panelList:
                        if panel.position == lookingAtIdx:
                            otherToonHead = panel.headModel

                    otherToonHead.doLookAroundToStareAt(otherToonHead, self.getLookAtToPosVec(lookingAtIdx, toonidx))
                self.IsLookingAt[toonidx] = lookingAtIdx
                return self.getLookAtToPosVec(toonidx, lookingAtIdx)
        return

    def getLookAtToPosVec(self, fromIdx, toIdx):
        x = -(POSITIONS[toIdx][0] - POSITIONS[fromIdx][0])
        y = POSITIONS[toIdx][1] - POSITIONS[fromIdx][1]
        z = POSITIONS[toIdx][2] - POSITIONS[fromIdx][2]
        return Vec3(x, y, z)

    def initLookAtInfo(self):
        self.used_panel_indexs = []
        for panel in self.panelList:
            if panel.dna != None:
                self.used_panel_indexs.append(panel.position)

        if len(self.used_panel_indexs) == 0:
            return
        self.IsLookingAt = []
        for i in range(MAX_AVATARS):
            self.IsLookingAt.append('f')

        for panel in self.panelList:
            if panel.dna != None:
                panel.headModel.setLookAtPositionCallbackArgs((self, panel.headModel, panel.position))

        return

    def unload(self):
        if self.isLoaded == 0:
            return None
        cleanupDialog('globalDialog')
        for panel in self.panelList:
            panel.destroy()

        del self.panelList
        self.title.removeNode()
        del self.title
        self.quitButton.destroy()
        del self.quitButton
        self.logoutButton.destroy()
        del self.logoutButton
        self.pickAToonBG.removeNode()
        del self.pickAToonBG
        del self.avatarList
        self.parentFSM.getCurrentState().removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.ignoreAll()
        self.isLoaded = 0
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        return

    def __handlePanelDone(self, panelDoneStatus, panelChoice=0):
        self.doneStatus = {}
        self.doneStatus['mode'] = panelDoneStatus
        self.choice = panelChoice
        if panelDoneStatus == 'chose':
            self.__handleChoice()
        else:
            if panelDoneStatus == 'nameIt':
                self.__handleCreate()
            else:
                if panelDoneStatus == 'delete':
                    self.__handleDelete()
                else:
                    if panelDoneStatus == 'create':
                        self.__handleCreate()

    def getChoice(self):
        return self.choice

    def __handleChoice(self):
        self.fsm.request('CheckDownload')

    def __handleCreate(self):

        def sendDoneTask(task):
            messenger.send(task.doneEvent, [task.doneStatus])
            return Task.done

        sdt = Task.Task(sendDoneTask)
        sdt.doneEvent = self.doneEvent
        sdt.doneStatus = self.doneStatus
        base.transitions.fadeOutTask(sdt)

    def __handleDelete(self):
        messenger.send(self.doneEvent, [self.doneStatus])

    def __handleQuit(self):
        cleanupDialog('globalDialog')
        self.doneStatus = {'mode': 'exit'}
        messenger.send(self.doneEvent, [self.doneStatus])

    def enterChoose(self):
        pass

    def exitChoose(self):
        pass

    def enterCheckDownload(self):
        self.accept('downloadAck-response', self.__handleDownloadAck)
        self.downloadAck = DownloadForceAcknowledge.DownloadForceAcknowledge('downloadAck-response')
        self.downloadAck.enter(4)

    def exitCheckDownload(self):
        self.downloadAck.exit()
        self.downloadAck = None
        self.ignore('downloadAck-response')
        return

    def __handleDownloadAck(self, doneStatus):

        def sendDoneTask(task):
            messenger.send(task.doneEvent, [task.doneStatus])
            return Task.done

        if doneStatus['mode'] == 'complete':
            sdt = Task.Task(sendDoneTask)
            sdt.doneEvent = self.doneEvent
            sdt.doneStatus = self.doneStatus
            base.transitions.fadeOutTask(sdt)
        else:
            self.fsm.request('Choose')

    def __handleLogoutWithoutConfirm(self):
        toonbase.tcr.loginFSM.request('login')