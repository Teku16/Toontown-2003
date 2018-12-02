from ShowBaseGlobal import *
import ToontownGlobals
from ToontownBattleGlobals import *
import DirectNotifyGlobal, string, LaffMeter, BattleBase
from DirectGui import *
import Localizer

class TownBattleToonPanel(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattleToonPanel')

    def __init__(self, id):
        gui = loader.loadModelOnce('phase_3.5/models/gui/battle_gui')
        DirectFrame.__init__(self, relief=None, image=gui.find('**/ToonBtl_Status_BG'), image_color=Vec4(0.5, 0.9, 0.5, 0.7))
        self.setScale(0.8)
        self.initialiseoptions(TownBattleToonPanel)
        self.avatar = None
        self.sosText = DirectLabel(parent=self, relief=None, pos=(0.1, 0, 0.015), text=Localizer.TownBattleToonSOS, text_scale=0.06)
        self.sosText.hide()
        self.undecidedText = DirectLabel(parent=self, relief=None, pos=(0.1, 0, 0.015), text=Localizer.TownBattleUndecided, text_scale=0.1)
        self.healthText = DirectLabel(parent=self, text='', pos=(-0.06, 0, -0.075), text_scale=0.055)
        self.hpChangeEvent = None
        self.gagNode = self.attachNewNode('gag')
        self.gagNode.setPos(0.1, 0, 0.03)
        self.hasGag = 0
        self.laffMeter = None
        self.whichText = DirectLabel(parent=self, text='', pos=(0.1, 0, -0.08), text_scale=0.05)
        self.hide()
        gui.removeNode()
        return
        return

    def setLaffMeter(self, avatar):
        self.notify.debug('setLaffMeter: new avatar %s' % avatar.doId)
        if self.avatar == avatar:
            messenger.send(self.avatar.uniqueName('hpChange'), [
             avatar.hp, avatar.maxHp])
            return None
        else:
            if self.avatar:
                self.cleanupLaffMeter()
            self.avatar = avatar
            self.laffMeter = LaffMeter.LaffMeter(avatar.style, avatar.hp, avatar.maxHp)
            self.laffMeter.setAvatar(self.avatar)
            self.laffMeter.reparentTo(self)
            self.laffMeter.setPos(-0.06, 0, 0.05)
            self.laffMeter.setScale(0.045)
            self.laffMeter.start()
            self.setHealthText(avatar.hp, avatar.maxHp)
            self.hpChangeEvent = self.avatar.uniqueName('hpChange')
            self.accept(self.hpChangeEvent, self.setHealthText)
        return None
        return

    def setHealthText(self, hp, maxHp):
        self.healthText['text'] = Localizer.TownBattleHealthText % {'hitPoints': hp, 'maxHit': maxHp}
        return

    def show(self):
        DirectFrame.show(self)
        if self.laffMeter:
            self.laffMeter.start()
        return

    def hide(self):
        DirectFrame.hide(self)
        if self.laffMeter:
            self.laffMeter.stop()
        return

    def updateLaffMeter(self, hp):
        if self.laffMeter:
            self.laffMeter.adjustFace(hp, self.avatar.maxHp)
        self.setHealthText(hp, maxHp)
        return

    def setValues(self, index, track, level=None, numTargets=None, targetIndex=None, localNum=None):
        self.notify.debug('Toon Panel setValues: index=%s track=%s level=%s numTargets=%s targetIndex=%s localNum=%s' % (index, track, level, numTargets, targetIndex, localNum))
        self.undecidedText.hide()
        self.sosText.hide()
        self.gagNode.hide()
        self.whichText.hide()
        if self.hasGag:
            self.gag.removeNode()
            self.hasGag = 0
        if track == BattleBase.NO_ATTACK or track == BattleBase.UN_ATTACK:
            self.undecidedText.show()
        else:
            if track == BattleBase.SOS:
                self.sosText.show()
            else:
                if track >= MIN_TRACK_INDEX and track <= MAX_TRACK_INDEX:
                    self.undecidedText.hide()
                    self.gagNode.show()
                    invButton = toonbase.localToon.inventory.buttonLookup(track, level)
                    self.gag = invButton.instanceUnderNode(self.gagNode, 'gag')
                    self.gag.setScale(0.8)
                    self.gag.setPos(0, 0, 0.02)
                    self.hasGag = 1
                    if numTargets is not None and targetIndex is not None and localNum is not None:
                        self.whichText.show()
                        self.whichText['text'] = self.determineWhichText(numTargets, targetIndex, localNum, index)
                else:
                    self.notify.error('Bad track value: %s' % track)
        return None
        return

    def determineWhichText(self, numTargets, targetIndex, localNum, index):
        returnStr = ''
        targetList = range(numTargets)
        targetList.reverse()
        for i in targetList:
            if targetIndex == -1:
                returnStr += 'X'
            else:
                if targetIndex == -2:
                    if i == index:
                        returnStr += '-'
                    else:
                        returnStr += 'X'
                else:
                    if targetIndex >= 0 and targetIndex <= 3:
                        if i == targetIndex:
                            returnStr += 'X'
                        else:
                            returnStr += '-'
                    else:
                        self.notify.error('Bad target index: %s' % targetIndex)

        return returnStr

    def cleanup(self):
        self.ignoreAll()
        self.cleanupLaffMeter()
        if self.hasGag:
            self.gag.removeNode()
            del self.gag
        self.gagNode.removeNode()
        del self.gagNode
        DirectFrame.destroy(self)

    def cleanupLaffMeter(self):
        self.notify.debug('Cleaning up laffmeter!')
        self.ignore(self.hpChangeEvent)
        if self.laffMeter:
            self.laffMeter.destroy()
            self.laffMeter = None
        return None
        return