from DirectGui import *
from ToontownGlobals import *
from ToonBaseGlobal import *
from ShowBaseGlobal import *
from IntervalGlobal import *
from ClockDelta import *
import ToontownGlobals, DistributedObject, Localizer, CollisionSphere, CollisionNode, BankGui
from BankGlobals import *
import ToontownDialog

class DistributedBank(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedBank')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.bankGui = None
        self.bankDialog = None
        return

    def generate(self):
        self.bankSphereEvent = 'bankSphere'
        self.bankSphereEnterEvent = 'enter' + self.bankSphereEvent
        self.bankGuiDoneEvent = 'bankGuiDone'

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        self.accept(self.bankSphereEnterEvent, self.__handleEnterSphere)
        self.load()

    def load(self):
        bankNode = render.find('**/bank_origin')
        self.bankModel = bankNode.getParent()

    def disable(self):
        self.notify.debug('disable')
        self.ignore(self.bankSphereEnterEvent)
        self.ignore(self.bankGuiDoneEvent)
        if self.bankGui:
            self.bankGui.destroy()
            self.bankGui = None
        if self.bankDialog:
            self.bankDialog.cleanup()
            self.bankDialog = None
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        self.notify.debug('delete')
        self.bankModel.removeNode()
        DistributedObject.DistributedObject.delete(self)

    def __handleEnterSphere(self, collEntry):
        self.notify.debug('Entering Bank Sphere....')
        self.ignore(self.bankSphereEnterEvent)
        self.cr.playGame.getPlace().detectedBankCollision()
        self.sendUpdate('avatarEnter', [])

    def __handleBankDone(self, transactionAmount):
        self.sendUpdate('transferMoney', [transactionAmount])
        self.ignore(self.bankGuiDoneEvent)
        self.bankGui.destroy()
        self.bankGui = None
        return

    def freeAvatar(self):
        toonbase.localToon.posCamera(0, 0)
        toonbase.tcr.playGame.getPlace().setState('walk')
        self.accept(self.bankSphereEnterEvent, self.__handleEnterSphere)

    def setMovie(self, mode, avId, timestamp):
        timeStamp = globalClockDelta.localElapsedTime(timestamp)
        isLocalToon = avId == toonbase.localToon.doId
        self.notify.info('setMovie: %s %s %s %s' % (mode, avId, timeStamp, isLocalToon))
        if mode == BANK_MOVIE_CLEAR:
            self.notify.debug('setMovie: clear')
            return
        else:
            if mode == BANK_MOVIE_GUI:
                self.notify.debug('setMovie: gui')
                if isLocalToon:
                    self.bankGui = BankGui.BankGui(self.bankGuiDoneEvent)
                    self.accept(self.bankGuiDoneEvent, self.__handleBankDone)
                return
            else:
                if mode == BANK_MOVIE_DEPOSIT:
                    self.notify.debug('setMovie: deposit')
                    if isLocalToon:
                        self.freeAvatar()
                    return
                else:
                    if mode == BANK_MOVIE_WITHDRAW:
                        self.notify.debug('setMovie: withdraw')
                        if isLocalToon:
                            self.freeAvatar()
                        return
                    else:
                        if mode == BANK_MOVIE_NOT_OWNER:
                            self.notify.debug('setMovie: not owner')
                            if isLocalToon:
                                self.bankDialog = ToontownDialog.ToontownDialog(dialogName='BankNotOwner', style=ToontownDialog.Acknowledge, text=Localizer.DistributedBankNotOwner, text_wordwrap=15, fadeScreen=1, command=self.__clearDialog)
                            return
                        else:
                            if mode == BANK_MOVIE_NO_OWNER:
                                self.notify.debug('setMovie: no owner')
                                if isLocalToon:
                                    self.bankDialog = ToontownDialog.ToontownDialog(dialogName='BankNoOwner', style=ToontownDialog.Acknowledge, text=Localizer.DistributedBankNoOwner, text_wordwrap=15, fadeScreen=1, command=self.__clearDialog)
                                return
                            else:
                                self.notify.warning('unknown mode in setMovie: %s' % mode)

    def __clearDialog(self, event):
        self.bankDialog.cleanup()
        self.bankDialog = None
        self.freeAvatar()
        return