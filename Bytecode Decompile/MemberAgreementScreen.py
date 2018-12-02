from DirectGui import *
from DateOfBirthEntry import *
from MultiPageTextFrame import *
from ToontownGlobals import *
import Localizer, ToontownDialog, FSM, State, TTAccount

class MemberAgreementScreen(DirectObject):
    __module__ = __name__

    def __init__(self, tcr, doneEvent):
        self.doneEvent = doneEvent
        self.tcr = tcr
        self.loginInterface = self.tcr.loginInterface
        self.legalText = Localizer.MemberAgreementScreenLegalText
        self.numPages = len(self.legalText)
        self.checkAge = config.GetBool('check-member-agreement-age', 0)
        self.fsm = FSM.FSM('MemberAgreementScreen', [
         State.State('off', self.enterOff, self.exitOff, [
          'getParents']),
         State.State('getParents', self.enterGetParents, self.exitGetParents, [
          'viewAgreement']),
         State.State('viewAgreement', self.enterViewAgreement, self.exitViewAgreement, [
          'youMustAgree']),
         State.State('youMustAgree', self.enterYouMustAgree, self.exitYouMustAgree, [
          'viewAgreement'])], 'off', 'off')
        self.fsm.enterInitialState()

    def load(self):
        guiButton = loader.loadModelOnce('phase_3/models/gui/quit_button')
        background = loader.loadModel('phase_3/models/gui/login-background')
        cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
        self.frame = DirectFrame(parent=aspect2d, relief=FLAT, image=background.find('**/member_agreement'))
        self.welcomeLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, 0.88), text=Localizer.MemberAgreementScreenWelcome, text_font=getMinnieFont(), text_scale=0.0935, text_fg=(1, 0.5, 0.1, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.onYourWayLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, 0.79), text=Localizer.MemberAgreementScreenOnYourWay, text_scale=0.0725, text_fg=(1, 1, 0, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.toontownLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, 0.67), text=Localizer.MemberAgreementScreenToontown, text_font=getMinnieFont(), text_scale=0.087, text_fg=(1, 0.5, 0.1, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        priceColor = (
         0, 0.9, 0, 1)
        if self.tcr.getCreditCardUpFront():
            priceTextScale = 0.09
            self.pricingLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, 0.558), text=Localizer.MemberAgreementScreenCCUpFrontPricing, text_scale=priceTextScale, text_fg=(1, 1, 0, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
            self.freeTrialDuration = DirectLabel(parent=self.pricingLabel, relief=None, pos=(-0.36, 0, 0), text=self.tcr.accountServerConstants.getString('freeTrialPeriodInDays'), text_scale=priceTextScale, text_fg=priceColor, text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
            priceFirstMonthPos = (
             0.92, 0, -0.18)
            pricePerMonthPos = (-0.11, 0, -0.27)
        else:
            priceTextScale = 0.1
            self.pricingLabel = DirectLabel(parent=self.frame, relief=None, pos=(0, 0, 0.558), text=Localizer.MemberAgreementScreenPricing, text_scale=priceTextScale, text_fg=(1, 1, 0, 1), text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
            priceFirstMonthPos = (
             0.52, 0, 0)
            pricePerMonthPos = (0.85, 0, -0.1)
        self.priceFirstMonth = DirectLabel(parent=self.pricingLabel, relief=None, pos=priceFirstMonthPos, text='$%s' % self.tcr.accountServerConstants.getString('priceFirstMonth'), text_scale=priceTextScale, text_fg=priceColor, text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.pricePerMonth = DirectLabel(parent=self.pricingLabel, relief=None, pos=pricePerMonthPos, text='$%s' % self.tcr.accountServerConstants.getString('pricePerMonth'), text_scale=priceTextScale, text_fg=priceColor, text_shadow=(0, 0, 0, 1), text_shadowOffset=(0.08, 0.08))
        self.dobEntry = DateOfBirthEntry(parent=self.frame, pos=(0, 0, 0.26), scale=0.095, defaultAge=0, curYear=self.tcr.dateObject.getYear())
        if not self.checkAge:
            self.dobEntry.hide()
        self.memAgreement = MultiPageTextFrame(parent=self.frame, relief=None, textList=self.legalText, hidePageNum=1, width=1.8, height=0.9, wordWrap=34, pos=(0, 0, -0.3))
        self.cogIcon = DirectLabel(parent=self.memAgreement, relief=None, pos=(-0.75, 0, 0.3), scale=0.25, image=cogIcons.find('**/LegalIcon'))
        self.agreementTitle = DirectLabel(parent=self.memAgreement, relief=None, pos=(0.0426513, 0, 0.268794), scale=0.09, text=Localizer.MemberAgreementScreenAgreementTitle, text_font=getSuitFont(), text_wordwrap=10)
        self.clickNextLabel = DirectLabel(parent=self.memAgreement, relief=None, pos=(-0.325283, 0, -0.388257), scale=0.05, text=Localizer.MemberAgreementScreenClickNext)
        self.memAgreement.setPageChangeCallback(self.__handlePageChange)
        bottomButtonZ = -0.57
        self.cancelButton = DirectButton(parent=self.memAgreement, relief=None, scale=1.1, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1, 1, 1), pos=(-0.5, 0, bottomButtonZ), text=Localizer.MemberAgreementScreenCancel, text_scale=0.06, text_pos=(0, -0.018), command=self.__handleCancel)
        self.declineButton = DirectButton(parent=self.memAgreement, relief=None, scale=1.1, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1, 1, 1), pos=(0, 0, bottomButtonZ), text=Localizer.MemberAgreementScreenDisagree, text_scale=0.06, text_pos=(0, -0.018), command=self.__handleDisagree)
        self.acceptButton = DirectButton(parent=self.memAgreement, relief=None, scale=1.1, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1, 1, 1), pos=(0.5, 0, bottomButtonZ), text=Localizer.MemberAgreementScreenAgree, text_scale=0.06, text_pos=(0, -0.018), command=self.__handleAgree)
        self.dialogDoneEvent = 'memberAgreementDialogAck'
        self.dialog = ToontownDialog.GlobalDialog(doneEvent=self.dialogDoneEvent, message='', style=ToontownDialog.Acknowledge)
        self.dialog.hide()
        self.mustAgreeDialog = DirectFrame(relief=None, pos=(0, 0.1, 0), image=getDefaultDialogGeom(), image_color=GlobalDialogColor, image_scale=(1.3, 1.0, 0.8), text=Localizer.MemberAgreementScreenYouMustAgree, text_scale=0.08, text_pos=(0.0, 0.2), text_wordwrap=15, sortOrder=NO_FADE_SORT_INDEX)
        self.mustAgreeDialog.hide()
        linePos = -0.13
        buttonImageScale = 1.1
        buttonLineHeight = 0.112
        self.mustAgreeOkButton = DirectButton(parent=self.mustAgreeDialog, relief=None, pos=(0, 0, linePos), scale=0.9, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=buttonImageScale, text=Localizer.MemberAgreementScreenYouMustAgreeOk, text_scale=0.06, text_pos=(0, -0.02), command=self.__handleMustAgreeOk)
        linePos -= buttonLineHeight
        self.mustAgreeQuitButton = DirectButton(parent=self.mustAgreeDialog, relief=None, pos=(0, 0, linePos), scale=0.9, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=buttonImageScale, image0_color=Vec4(1, 0.1, 0.1, 1), image1_color=Vec4(1, 0.1, 0.1, 1), image2_color=Vec4(1, 1, 1, 1), text=Localizer.MemberAgreementScreenYouMustAgreeQuit, text_scale=0.06, text_pos=(0, -0.02), command=self.__handleMustAgreeQuit)
        linePos -= buttonLineHeight
        self.frame.hide()
        background.removeNode()
        guiButton.removeNode()
        cogIcons.removeNode()
        return

    def unload(self):
        self.mustAgreeDialog.destroy()
        self.frame.destroy()
        self.dialog.cleanup()
        del self.frame
        del self.dialog
        del self.fsm

    def enter(self):
        self.frame.show()

        def getDOBfromEntry(self=self):
            self.dobMonth = self.dobEntry.getMonth()
            self.dobYear = self.dobEntry.getYear()
            self.dobDay = self.dobEntry.getDay()

        if self.tcr.getCreditCardUpFront():
            getDOBfromEntry()
        try:
            error = self.loginInterface.getAccountData(self.tcr.userName, self.tcr.password)
        except TTAccount.TTAccountException:
            error = 'exception raised'
        else:
            if not error:
                accountData = self.loginInterface.accountData
                if not (accountData.hasKey('dobMonth') and accountData.hasKey('dobYear') and accountData.hasKey('dobDay')):
                    error = 1
            if error:
                getDOBfromEntry()
            try:
                self.dobMonth = accountData.getInt('dobMonth')
                self.dobYear = accountData.getInt('dobYear')
                self.dobDay = accountData.getInt('dobDay')
            except ValueError:
                getDOBfromEntry()
            else:
                if self.checkAge:
                    self.dobEntry.setMonth(self.dobMonth)
                    self.dobEntry.setYear(self.dobYear)
                    self.dobEntry.setDay(self.dobDay)

        self.age = toonbase.tcr.dateObject.getAge(self.dobMonth, self.dobYear, self.dobDay)
        self.fsm.request('getParents')

    def exit(self):
        self.fsm.requestFinalState()
        self.frame.hide()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterGetParents(self):
        if self.tcr.getCreditCardUpFront() or self.age < 18:
            if self.tcr.getCreditCardUpFront():
                msg = Localizer.MemberAgreementScreenGetParentsUnconditional
            else:
                msg = Localizer.MemberAgreementScreenGetParents
            self.dialog.setMessage(msg)
            self.dialog.show()

            def handleGetParentsAck(self=self):
                self.dialog.hide()
                self.fsm.request('viewAgreement')

            self.acceptOnce(self.dialogDoneEvent, handleGetParentsAck)
        else:
            self.fsm.request('viewAgreement')

    def exitGetParents(self):
        pass

    def enterViewAgreement(self):
        self.memAgreement.acceptAgreementKeypresses()

    def exitViewAgreement(self):
        self.memAgreement.ignoreAgreementKeypresses()

    def enterYouMustAgree(self):
        base.transitions.fadeScreen(0.5)
        self.mustAgreeDialog.show()

    def __handleMustAgreeOk(self):
        self.fsm.request('viewAgreement')

    def __handleMustAgreeQuit(self):
        messenger.send(self.doneEvent, [{'mode': 'quit'}])

    def exitYouMustAgree(self):
        base.transitions.noTransitions()
        self.mustAgreeDialog.hide()

    def __handleAgree(self):
        if self.checkAge:
            age = self.dobEntry.getAge()
            if age < 18:
                self.dialog.setMessage(Localizer.MemberAgreementScreenMustBeOlder)
                self.dialog.show()

                def handleOlderAck(self=self):
                    self.dialog.hide()
                    self.fsm.request('viewAgreement')

                self.acceptOnce(self.dialogDoneEvent, handleOlderAck)
                self.memAgreement.ignoreAgreementKeypresses()
            else:
                messenger.send(self.doneEvent, [{'mode': 'agree'}])
        else:
            messenger.send(self.doneEvent, [{'mode': 'agree'}])

    def __handleDisagree(self):
        self.fsm.request('youMustAgree')

    def __handleCancel(self):
        messenger.send(self.doneEvent, [{'mode': 'cancel'}])

    def __handlePageChange(self, pageNum):
        if pageNum == 0:
            self.cogIcon.show()
            self.agreementTitle.show()
            self.clickNextLabel.show()
        else:
            self.cogIcon.hide()
            self.agreementTitle.hide()
            self.clickNextLabel.hide()