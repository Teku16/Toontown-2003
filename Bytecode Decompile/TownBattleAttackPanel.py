from DirectObject import *
from ShowBaseGlobal import *
import DirectNotifyGlobal, string, StateData
AttackPanelHidden = 0

def hideAttackPanel(flag):
    global AttackPanelHidden
    AttackPanelHidden = flag
    messenger.send('hide-attack-panel')


class TownBattleAttackPanel(StateData.StateData):
    __module__ = __name__

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        return

    def load(self):
        return

    def unload(self):
        return

    def enter(self):
        StateData.StateData.enter(self)
        if not AttackPanelHidden:
            toonbase.localToon.inventory.show()
        self.accept('inventory-selection', self.__handleInventory)
        self.accept('inventory-run', self.__handleRun)
        self.accept('inventory-sos', self.__handleSOS)
        self.accept('inventory-pass', self.__handlePass)
        self.accept('hide-attack-panel', self.__handleHide)
        return

    def exit(self):
        StateData.StateData.exit(self)
        self.ignore('inventory-selection')
        self.ignore('inventory-run')
        self.ignore('inventory-sos')
        self.ignore('inventory-pass')
        self.ignore('hide-attack-panel')
        toonbase.localToon.inventory.hide()
        return

    def __handleRun(self):
        doneStatus = {'mode': 'Run'}
        messenger.send(self.doneEvent, [doneStatus])
        return

    def __handleSOS(self):
        doneStatus = {'mode': 'SOS'}
        messenger.send(self.doneEvent, [doneStatus])
        return

    def __handlePass(self):
        doneStatus = {'mode': 'Pass'}
        messenger.send(self.doneEvent, [doneStatus])
        return

    def __handleInventory(self, track, level):
        if toonbase.localToon.inventory.numItem(track, level) > 0:
            doneStatus = {}
            doneStatus['mode'] = 'Inventory'
            doneStatus['track'] = track
            doneStatus['level'] = level
            messenger.send(self.doneEvent, [doneStatus])
        else:
            self.notify.error("An item we don't have: track %s level %s was selected." % [track, level])
        return

    def __handleHide(self):
        if AttackPanelHidden:
            toonbase.localToon.inventory.hide()
        else:
            toonbase.localToon.inventory.show()
        return