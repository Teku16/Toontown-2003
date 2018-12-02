from DirectGui import *
import DirectNotifyGlobal, ToontownGlobals, Localizer, Task

class BankGui(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('BankGui')

    def __init__(self, doneEvent, allowWithdraw=1):
        DirectFrame.__init__(self, relief=None, geom=getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(1.33, 1, 1.1), pos=(0, 0, 0))
        self.initialiseoptions(BankGui)
        self.doneEvent = doneEvent
        self.__transactionAmount = 0
        buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
        jarGui = loader.loadModel('phase_3.5/models/gui/jar_gui')
        arrowGui = loader.loadModelOnce('phase_3/models/gui/create_a_toon_gui')
        bankModel = loader.loadModel('phase_5.5/models/estate/jellybeanBank.bam')
        bankModel.find('**/pig').setDepthWrite(1)
        bankModel.find('**/pig').setDepthTest(1)
        okImageList = (
         buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
        cancelImageList = (
         buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
        arrowImageList = (
         arrowGui.find('**/CrtATn_R_Arrow_UP'), arrowGui.find('**/CrtATn_R_Arrow_DN'), arrowGui.find('**/CrtATn_R_Arrow_RLVR'), arrowGui.find('**/CrtATn_R_Arrow_UP'))
        self.cancelButton = DirectButton(parent=self, relief=None, image=cancelImageList, pos=(-0.2, 0, -0.4), text=Localizer.BankGuiCancel, text_scale=0.06, text_pos=(0, -0.1), command=self.__cancel)
        self.okButton = DirectButton(parent=self, relief=None, image=okImageList, pos=(0.2, 0, -0.4), text=Localizer.BankGuiOk, text_scale=0.06, text_pos=(0, -0.1), command=self.__requestTransaction)
        self.jarDisplay = DirectLabel(parent=self, relief=None, pos=(-0.4, 0, 0), scale=0.8, text=str(toonbase.localToon.getMoney()), text_scale=0.2, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, -0.1, 0), image=jarGui.find('**/Jar'), text_font=ToontownGlobals.getSignFont())
        self.bankDisplay = DirectLabel(parent=self, relief=None, pos=(0.4, 0, 0), scale=1.1, text=str(toonbase.localToon.getBankMoney()), text_scale=0.2, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, -0.1, 0), geom=bankModel, geom_scale=0.08, geom_pos=(0, 10, -0.26), geom_hpr=(0, 0, 0), text_font=ToontownGlobals.getSignFont())
        self.depositArrow = DirectButton(parent=self, relief=None, image=arrowImageList, image_scale=(1, 1, 1), image3_color=Vec4(0.6, 0.6, 0.6, 0.25), pos=(0.01, 0, 0.15))
        self.withdrawArrow = DirectButton(parent=self, relief=None, image=arrowImageList, image_scale=(-1, 1, 1), image3_color=Vec4(0.6, 0.6, 0.6, 0.25), pos=(-0.01, 0, -0.15))
        self.depositArrow.bind(B1PRESS, self.__depositButtonDown)
        self.depositArrow.bind(B1RELEASE, self.__depositButtonUp)
        self.withdrawArrow.bind(B1PRESS, self.__withdrawButtonDown)
        self.withdrawArrow.bind(B1RELEASE, self.__withdrawButtonUp)
        if allowWithdraw:
            self.depositArrow.setPos(0.01, 0, 0.15)
            self.withdrawArrow.setPos(-0.01, 0, -0.15)
        else:
            self.depositArrow.setPos(0, 0, 0)
            self.withdrawArrow.hide()
        buttons.removeNode()
        jarGui.removeNode()
        arrowGui.removeNode()
        self.__updateTransaction(0)
        return

    def __cancel(self):
        messenger.send(self.doneEvent, [0])
        return

    def __requestTransaction(self):
        messenger.send(self.doneEvent, [self.__transactionAmount])
        return

    def __updateTransaction(self, amount):
        hitLimit = 0
        self.__transactionAmount += amount
        jarMoney = toonbase.localToon.getMoney()
        maxJarMoney = toonbase.localToon.getMaxMoney()
        bankMoney = toonbase.localToon.getBankMoney()
        maxBankMoney = toonbase.localToon.getMaxBankMoney()
        newJarMoney = jarMoney - self.__transactionAmount
        newBankMoney = bankMoney + self.__transactionAmount
        if newJarMoney <= 0 or newBankMoney >= maxBankMoney:
            self.depositArrow['state'] = DISABLED
            hitLimit = 1
        else:
            self.depositArrow['state'] = NORMAL
        if newBankMoney <= 0 or newJarMoney >= maxJarMoney:
            self.withdrawArrow['state'] = DISABLED
            hitLimit = 1
        else:
            self.withdrawArrow['state'] = NORMAL
        self.jarDisplay['text'] = str(newJarMoney)
        self.bankDisplay['text'] = str(newBankMoney)
        return (
         hitLimit, newJarMoney, newBankMoney, self.__transactionAmount)

    def __runCounter(self, task):
        if task.time - task.prevTime < task.delayTime:
            return Task.cont
        else:
            task.delayTime = max(0.05, task.delayTime * 0.75)
            task.prevTime = task.time
            hitLimit, jar, bank, trans = self.__updateTransaction(task.delta)
            if hitLimit:
                return Task.done
            else:
                return Task.cont

    def __depositButtonUp(self, event):
        taskMgr.remove(self.taskName('runCounter'))

    def __depositButtonDown(self, event):
        task = Task.Task(self.__runCounter)
        task.delayTime = 0.4
        task.prevTime = 0.0
        task.delta = 1
        hitLimit, jar, bank, trans = self.__updateTransaction(task.delta)
        if not hitLimit:
            taskMgr.add(task, self.taskName('runCounter'))

    def __withdrawButtonUp(self, event):
        taskMgr.remove(self.taskName('runCounter'))

    def __withdrawButtonDown(self, event):
        task = Task.Task(self.__runCounter)
        task.delayTime = 0.4
        task.prevTime = 0.0
        task.delta = -1
        hitLimit, jar, bank, trans = self.__updateTransaction(task.delta)
        if not hitLimit:
            taskMgr.add(task, self.taskName('runCounter'))