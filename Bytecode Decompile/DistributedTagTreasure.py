import DistributedTreasure

class DistributedTagTreasure(DistributedTreasure.DistributedTreasure):
    __module__ = __name__

    def __init__(self, cr):
        DistributedTreasure.DistributedTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/icecream'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.mp3'
        self.accept('minigameOffstage', self.handleMinigameOffstage)

    def handleEnterSphere(self, collEntry):
        if not toonbase.localToon.isIt:
            self.d_requestGrab()
        return None
        return

    def handleMinigameOffstage(self):
        self.nodePath.reparentTo(hidden)