from ToontownGlobals import *
from IntervalGlobal import *
from ClockDelta import *
import ToontownGlobals, DistributedObject, Localizer, Task, Fireworks, FireworkShows, DDHood

class DistributedFireworkShow(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedFireworkShow')
    notify.setDebug(1)

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.currentShow = None
        return

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        if self.currentShow:
            self.currentShow.pause()
            self.currentShow = None
            ivalMgr.finishIntervalsMatching('shootFirework*')
        if isinstance(toonbase.tcr.playGame.hood, DDHood.DDHood):
            toonbase.tcr.playGame.hood.whiteFogColor = Vec4(0.8, 0.8, 0.8, 1)
        if hasattr(toonbase.tcr.playGame.hood, 'loader'):
            toonbase.tcr.playGame.hood.loader.geom.clearColorScale()
        if hasattr(toonbase.tcr.playGame.hood, 'sky'):
            toonbase.tcr.playGame.hood.sky.clearColorScale()
        return

    def delete(self):
        DistributedObject.DistributedObject.delete(self)

    def startShow(self, style, timestamp):
        t = globalClockDelta.localElapsedTime(timestamp)
        self.currentShow = self.getFireworkShow(style, t)
        if self.currentShow:
            self.currentShow.play(t)
        return

    def localShootFirework(self):
        pos = toonbase.localToon.getPos(render)
        style = 1
        color = 0
        self.d_requestFirework(pos[0], pos[1], pos[2], style, color)

    def d_requestFirework(self, x, y, z, style, color):
        self.sendUpdate('requestFirework', (x, y, z, style, color))

    def shootFirework(self, x, y, z, style, color):
        amp = 5
        Fireworks.shootFirework(style, x, y, z, color, color, amp)
        return

    def getFireworkShow(self, index, t):
        show = FireworkShows.getShow(index)
        if show is None:
            self.notify.warning('could not find firework show: index' % index)
            return None
        iList = []
        dark = 0.5
        skyDark = 0.0
        currentT = 0.0

        def checkDDFog():
            if isinstance(toonbase.tcr.playGame.hood, DDHood.DDHood):
                toonbase.tcr.playGame.hood.whiteFogColor = Vec4(0.2, 0.2, 0.2, 1)
                if not toonbase.tcr.playGame.getPlace().cameraSubmerged:
                    toonbase.tcr.playGame.hood.setWhiteFog()

        def restoreDDFog():
            if isinstance(toonbase.tcr.playGame.hood, DDHood.DDHood):
                toonbase.tcr.playGame.hood.whiteFogColor = Vec4(0.8, 0.8, 0.8, 1)
                if not toonbase.tcr.playGame.getPlace().cameraSubmerged:
                    toonbase.tcr.playGame.hood.setWhiteFog()

        showMusic = loader.loadMusic('phase_4/audio/bgm/firework_music.mid')
        showMusic.setVolume(1)
        iList.extend((Func(toonbase.localToon.setSystemMessage, 0, Localizer.FireworksBeginning), Func(checkDDFog),
         Parallel(LerpColorScaleInterval(toonbase.tcr.playGame.hood.loader.geom, 2, Vec4(dark, dark, dark, 1)), LerpColorScaleInterval(toonbase.tcr.playGame.hood.sky, 2, Vec4(skyDark, skyDark, skyDark, 1))), Func(toonbase.localToon.setSystemMessage, 0, Localizer.FireworksInstructions), Wait(2), Func(toonbase.tcr.playGame.hood.loader.music.stop), Func(base.playMusic, showMusic, 0, 1, 0.8, t), Wait(1)))
        currentT = 7.0
        for effect in show:
            waitTime, style, colorIndex1, colorIndex2, amp, x, y, z = effect
            if waitTime > 0:
                currentT += waitTime
                iList.append(Wait(waitTime))
            if currentT >= t:
                iList.append(Func(Fireworks.shootFirework, style, x, y, z, colorIndex1, colorIndex2, amp))

        iList.extend((Wait(4), Func(restoreDDFog),
         Parallel(LerpColorScaleInterval(toonbase.tcr.playGame.hood.loader.geom, 2, Vec4(1, 1, 1, 1)), LerpColorScaleInterval(toonbase.tcr.playGame.hood.sky, 2, Vec4(1, 1, 1, 1))), Func(toonbase.tcr.playGame.hood.loader.geom.clearColorScale), Func(toonbase.tcr.playGame.hood.sky.clearColorScale), Func(showMusic.stop), Func(toonbase.localToon.setSystemMessage, 0, Localizer.FireworksEnding), Wait(0.5), Func(base.playMusic, toonbase.tcr.playGame.hood.loader.music, 1, 1, 0.8)))
        return Track(iList)
        return