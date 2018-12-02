from PandaModules import *
from DirectNotifyGlobal import *
import Interval, ParticleEffect

class ParticleInterval(Interval.Interval):
    __module__ = __name__
    particleNum = 1
    notify = directNotify.newCategory('ParticleInterval')

    def __init__(self, particleEffect, parent, worldRelative=1, loop=0, duration=0.0, name=None):
        id = 'Particle-%d' % ParticleInterval.particleNum
        ParticleInterval.particleNum += 1
        if name == None:
            name = id
        self.particleEffect = particleEffect
        self.parent = parent
        self.worldRelative = worldRelative
        self.fLoop = loop
        Interval.Interval.__init__(self, name, duration)
        return

    def __del__(self):
        if self.particleEffect:
            self.particleEffect.cleanup()
            self.particleEffect = None
        return

    def privInitialize(self, t):
        renderParent = None
        if self.worldRelative:
            renderParent = render
        if self.particleEffect:
            self.particleEffect.start(self.parent, renderParent)
        self.state = CInterval.SStarted
        self.currT = t
        return

    def privStep(self, t):
        if self.state == CInterval.SPaused:
            self.privInitialize(t)
        else:
            self.state = CInterval.SStarted
            self.currT = t

    def privFinalize(self):
        if self.particleEffect:
            self.particleEffect.cleanup()
            self.particleEffect = None
        self.currT = self.getDuration()
        self.state = CInterval.SFinal
        return

    def privInstant(self):
        if self.particleEffect:
            self.particleEffect.cleanup()
            self.particleEffect = None
        self.currT = self.getDuration()
        self.state = CInterval.SFinal
        return

    def privInterrupt(self):
        self.particleEffect.disable()
        self.state = CInterval.SPaused