from ShowBaseGlobal import *
import Playground, whrandom

class DGPlayground(Playground.Playground):
    __module__ = __name__

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        self.nextBirdTime = 0
        taskMgr.add(self.__birds, 'DG-birds')

    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('DG-birds')

    def __birds(self, task):
        if task.time < self.nextBirdTime:
            return Task.cont
        randNum = whrandom.random()
        bird = int(randNum * 100) % 4 + 1
        if bird == 1:
            base.playSfx(self.loader.bird1Sound)
        else:
            if bird == 2:
                base.playSfx(self.loader.bird2Sound)
            else:
                if bird == 3:
                    base.playSfx(self.loader.bird3Sound)
                else:
                    if bird == 4:
                        base.playSfx(self.loader.bird4Sound)
        self.nextBirdTime = task.time + randNum * 20.0
        return Task.cont