from ShowBaseGlobal import *
from ToontownGlobals import *
from ToontownMsgTypes import *
from DirectGui import *
from TaskManagerGlobal import *
import OnscreenText, StateData, ToontownDialog, FSM, State, DirectNotifyGlobal, Task, Localizer, TTAccount, GuiScreen, math

class FreeTimeInformScreen(StateData.StateData, GuiScreen.GuiScreen):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('FreeTimeInformScreen')

    def __init__(self, tcr, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        GuiScreen.GuiScreen.__init__(self)
        self.tcr = tcr
        self.fsm = FSM.FSM('FreeTimeInformScreen', [
         State.State('off', self.enterOff, self.exitOff, [
          'inform']),
         State.State('inform', self.enterInform, self.exitInform, [])], 'off', 'off')
        self.fsm.enterInitialState()

    def load(self):
        masterScale = 0.8
        textScale = 0.1 * masterScale
        entryScale = 0.08 * masterScale
        lineHeight = 0.21 * masterScale
        buttonScale = 2.0 * masterScale
        buttonLineHeight = 0.31 * masterScale
        background = loader.loadModel('phase_3/models/gui/login-background')
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        self.frame = DirectFrame(parent=aspect2d, relief=FLAT, image=background.find('**/free_time_expired'), image_scale=(1, 1, 1))
        self.frame.hide()
        freeTimeExpired = self.tcr.isFreeTimeExpired()
        if not freeTimeExpired:
            daysLeft, hoursLeft = self.__getTimeLeft()
            daysLeftInt = int(math.ceil(daysLeft))
            if daysLeftInt >= 2:
                notice = Localizer.FreeTimeInformScreenNDaysLeft % daysLeftInt
            else:
                if hoursLeft >= 12:
                    notice = Localizer.FreeTimeInformScreenOneDayLeft
                else:
                    if hoursLeft >= 2:
                        notice = Localizer.FreeTimeInformScreenNHoursLeft % hoursLeft
                    else:
                        if hoursLeft == 1:
                            notice = Localizer.FreeTimeInformScreenOneHourLeft
                        else:
                            notice = Localizer.FreeTimeInformScreenLessThanOneHourLeft
            freeTimeLabelPos = 0.62
            freeTimeLabelText = notice
            freeTimeLabelTextScale = 0.12
            linePos = 0.23
            self.freeButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'), guiButton.find('**/QuitBtn_UP')), image_color=(1, 1, 1, 1), text=Localizer.FreeTimeInformScreenFreePlay, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.3, 1.1, 1.1), command=self.__handlePlayFreeButton)
            linePos = -0.1
            self.sentence2Label = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, linePos), text=Localizer.FreeTimeInformScreenSecondSentence, text_scale=0.11, text_fg=(1, 1, 0, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
            joinButtonPos = -0.42
            quitButtonPos = joinButtonPos - buttonLineHeight * 1.4
        else:
            freeTimeLabelPos = 0.5
            if self.tcr.getCreditCardUpFront():
                freeTimeLabelText = Localizer.FreeTimeInformScreenExpiredCCUF
                joinButtonPos = 0.06
            else:
                freeTimeLabelText = Localizer.FreeTimeInformScreenExpired
                joinButtonPos = 0.135
            freeTimeLabelTextScale = 0.09
            if self.tcr.getCreditCardUpFront():
                quitLabelPos = -0.28
                quitLabelText = Localizer.FreeTimeInformScreenExpiredQuitCCUFText
                quitButtonPos = -0.64
            else:
                quitLabelPos = -0.27
                quitLabelText = Localizer.FreeTimeInformScreenExpiredQuitText
                quitButtonPos = -0.72
            self.freeTimeQuitLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, quitLabelPos), text=quitLabelText, text_scale=0.09, text_fg=(1, 1, 0, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        linePos = freeTimeLabelPos
        self.freeTimeLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, linePos), text=freeTimeLabelText, text_scale=freeTimeLabelTextScale, text_fg=(1, 1, 0, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        if freeTimeExpired and not self.tcr.getCreditCardUpFront():
            self.oopsLabel = DirectLabel(parent=self.freeTimeLabel, relief=None, pos=(-0.53, 0, 0), scale=1.36, text=Localizer.FreeTimeInformScreenOops, text_font=getMinnieFont(), text_scale=freeTimeLabelTextScale, text_fg=(1, 0.5, 0.1, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        linePos = joinButtonPos
        self.joinButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), text=Localizer.FreeTimeInformScreenPurchase, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.3, 1.1, 1.1), command=self.__handleJoinButton)
        linePos = quitButtonPos
        self.quitButton = DirectButton(parent=self.frame, relief=None, pos=(0, 0, linePos), scale=buttonScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image0_color=Vec4(1, 0.1, 0.1, 1), image1_color=Vec4(1, 0.1, 0.1, 1), image2_color=Vec4(1, 1, 1, 1), text=Localizer.FreeTimeInformScreenQuit, text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.3, 1.1, 1.1), command=self.__handleQuitButton)
        background.removeNode()
        guiButton.removeNode()
        return

    def unload(self):
        self.frame.destroy()
        del self.frame
        del self.fsm

    def enter(self):
        self.fsm.request('inform')

    def exit(self):
        self.fsm.requestFinalState()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterInform(self):
        self.frame.show()

    def exitInform(self):
        self.frame.hide()

    def __getTimeLeft(self):
        secsLeft = self.tcr.freeTimeLeft()
        hourSecs = 60 * 60
        daySecs = 24 * hourSecs
        return (
         float(secsLeft) / daySecs, int(secsLeft / hourSecs))

    def __handleJoinButton(self):
        messenger.send(self.doneEvent, [{'mode': 'join'}])

    def __handlePlayFreeButton(self):
        messenger.send(self.doneEvent, [{'mode': 'free'}])

    def __handleQuitButton(self):
        messenger.send(self.doneEvent, [{'mode': 'quit'}])