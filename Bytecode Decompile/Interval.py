from DirectObject import *
from PandaModules import *
import Task, math

class Interval(DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('Interval')
    playbackCounter = 0

    def __init__(self, name, duration, openEnded=1):
        self.name = name
        self.duration = duration
        self.state = CInterval.SInitial
        self.currT = 0.0
        self.doneEvent = None
        self.setTHooks = []
        self.__startT = 0
        self.__startTAtStart = 1
        self.__endT = duration
        self.__endTAtEnd = 1
        self.__playRate = 1.0
        self.__doLoop = 0
        self.__loopCount = 0
        self.openEnded = openEnded
        return

    def getName(self):
        return self.name

    def getDuration(self):
        return self.duration

    def getOpenEnded(self):
        return self.openEnded

    def getState(self):
        return self.state

    def isStopped(self):
        return self.getState() == CInterval.SInitial or self.getState() == CInterval.SFinal

    def setT(self, t):
        t = min(max(t, 0.0), self.getDuration())
        state = self.getState()
        if state == CInterval.SInitial:
            self.privInitialize(t)
        else:
            if state == CInterval.SFinal:
                self.privReverseInitialize(t)
            else:
                self.privStep(t)
        self.privPostEvent()

    def getT(self):
        return self.currT

    def start(self, startT=0.0, endT=-1.0, playRate=1.0):
        self.setupPlay(startT, endT, playRate, 0)
        self.__spawnTask()

    def loop(self, startT=0.0, endT=-1.0, playRate=1.0):
        self.setupPlay(startT, endT, playRate, 1)
        self.__spawnTask()

    def pause(self):
        if self.getState() == CInterval.SStarted:
            self.privInterrupt()
        self.privPostEvent()
        self.__removeTask()
        return self.getT()

    def resume(self, t0=None):
        if t0 != None:
            self.setT(t0)
        self.setupResume()
        if not self.isPlaying():
            self.__spawnTask()
        return

    def finish(self):
        state = self.getState()
        if state == CInterval.SInitial:
            self.privInstant()
        else:
            if state != CInterval.SFinal:
                self.privFinalize()
        self.privPostEvent()
        self.__removeTask()

    def isPlaying(self):
        return taskMgr.hasTaskNamed(self.getName() + '-play')

    def setDoneEvent(self, event):
        self.doneEvent = event

    def getDoneEvent(self):
        return self.doneEvent

    def privDoEvent(self, t, event):
        if event == CInterval.ETStep:
            self.privStep(t)
        else:
            if event == CInterval.ETFinalize:
                self.privFinalize()
            else:
                if event == CInterval.ETInterrupt:
                    self.privInterrupt()
                else:
                    if event == CInterval.ETInstant:
                        self.privInstant()
                    else:
                        if event == CInterval.ETInitialize:
                            self.privInitialize(t)
                        else:
                            if event == CInterval.ETReverseFinalize:
                                self.privReverseFinalize()
                            else:
                                if event == CInterval.ETReverseInstant:
                                    self.privReverseInstant()
                                else:
                                    if event == CInterval.ETReverseInitialize:
                                        self.privReverseInitialize(t)
                                    else:
                                        self.notify.error('Invalid event type: %s' % event)

    def privInitialize(self, t):
        self.state = CInterval.SStarted
        self.privStep(t)

    def privInstant(self):
        self.state = CInterval.SStarted
        self.privStep(self.getDuration())
        self.state = CInterval.SFinal
        self.intervalDone()

    def privStep(self, t):
        self.state = CInterval.SStarted
        self.currT = t

    def privFinalize(self):
        self.privStep(self.getDuration())
        self.state = CInterval.SFinal
        self.intervalDone()

    def privReverseInitialize(self, t):
        self.state = CInterval.SStarted
        self.privStep(t)

    def privReverseInstant(self):
        self.state = CInterval.SStarted
        self.privStep(self.getDuration())
        self.state = CInterval.SInitial

    def privReverseFinalize(self):
        self.privStep(0)
        self.state = CInterval.SInitial

    def privInterrupt(self):
        self.state = CInterval.SPaused

    def intervalDone(self):
        if self.doneEvent:
            messenger.throw(self.doneEvent)

    def setupPlay(self, startT, endT, playRate, doLoop):
        duration = self.getDuration()
        if startT <= 0:
            self.__startT = 0
            self.__startTAtStart = 1
        else:
            if startT > duration:
                self.__startT = duration
                self.__startTAtStart = 0
            else:
                self.__startT = startT
                self.__startTAtStart = 0
        if endT < 0 or endT >= duration:
            self.__endT = duration
            self.__endTAtEnd = 1
        else:
            self.__endT = endT
            self.__endTAtEnd = 0
        self.__clockStart = globalClock.getFrameTime()
        self.__playRate = playRate
        self.__doLoop = doLoop
        self.__loopCount = 0

    def setupResume(self):
        now = globalClock.getFrameTime()
        if self.__playRate > 0:
            self.__clockStart = now - (self.getT() - self.__startT) / self.__playRate
        else:
            if self.__playRate < 0:
                self.__clockStart = now - (self.getT() - self.__endT) / self.__playRate
        self.__loopCount = 0

    def stepPlay(self):
        now = globalClock.getFrameTime()
        if self.__playRate >= 0:
            t = (now - self.__clockStart) * self.__playRate + self.__startT
            if self.__endTAtEnd:
                self.__endT = self.getDuration()
            if t < self.__endT:
                if self.isStopped():
                    self.privInitialize(t)
                else:
                    self.privStep(t)
            else:
                if self.__endTAtEnd:
                    if self.isStopped():
                        if self.getOpenEnded() or self.__loopCount != 0:
                            self.privInstant()
                    else:
                        self.privFinalize()
                else:
                    if self.isStopped():
                        self.privInitialize(self.__endT)
                    else:
                        self.privStep(self.__endT)
                if self.__endT == self.__startT:
                    self.__loopCount += 1
                else:
                    timePerLoop = (self.__endT - self.__startT) / self.__playRate
                    numLoops = math.floor((now - self.__clockStart) / timePerLoop)
                    self.__loopCount += numLoops
                    self.__clockStart += numLoops * timePerLoop
        return self.__loopCount == 0 or self.__doLoop

    def __repr__(self, indent=0):
        space = ''
        for l in range(indent):
            space = space + ' '

        return space + self.name + ' dur: %.2f' % self.duration

    def play(self, *args, **kw):
        self.start(*args, **kw)

    def stop(self):
        self.finish()

    def setFinalT(self):
        self.finish()

    def privPostEvent(self):
        t = self.getT()
        if hasattr(self, 'setTHooks'):
            for func in self.setTHooks:
                func(t)

    def __spawnTask(self):
        import Task
        self.__removeTask()
        taskName = self.getName() + '-play'
        task = Task.Task(self.__playTask)
        task.interval = self
        taskMgr.add(task, taskName)

    def __removeTask(self):
        taskName = self.getName() + '-play'
        oldTasks = taskMgr.getTasksNamed(taskName)
        for task in oldTasks:
            if hasattr(task, 'interval'):
                task.interval.privInterrupt()
                taskMgr.remove(task)

    def __playTask(self, task):
        import Task
        again = self.stepPlay()
        self.privPostEvent()
        if again:
            return Task.cont
        else:
            return Task.done

    def popupControls(self, tl=None):
        import TkGlobal, math
        from Tkinter import Toplevel, Frame, Button, LEFT, X
        import Pmw, EntryScale
        if tl == None:
            tl = Toplevel()
            tl.title('Interval Controls')
        outerFrame = Frame(tl)

        def entryScaleCommand(t, s=self):
            s.pause()
            s.setT(t)

        self.es = es = EntryScale.EntryScale(outerFrame, text=self.getName(), min=0, max=math.floor(self.getDuration() * 100) / 100, command=entryScaleCommand)
        es.set(self.getT(), fCommand=0)
        es.pack(expand=1, fill=X)
        bf = Frame(outerFrame)

        def toStart(s=self, es=es):
            s.pause()
            s.setT(0.0)

        def toEnd(s=self):
            s.pause()
            s.setT(s.getDuration())

        jumpToStart = Button(bf, text='<<', command=toStart)

        def doPlay(s=self, es=es):
            s.resume(es.get())

        stop = Button(bf, text='Stop', command=lambda s=self: s.pause())
        play = Button(bf, text='Play', command=doPlay)
        jumpToEnd = Button(bf, text='>>', command=toEnd)
        jumpToStart.pack(side=LEFT, expand=1, fill=X)
        play.pack(side=LEFT, expand=1, fill=X)
        stop.pack(side=LEFT, expand=1, fill=X)
        jumpToEnd.pack(side=LEFT, expand=1, fill=X)
        bf.pack(expand=1, fill=X)
        outerFrame.pack(expand=1, fill=X)

        def update(t, es=es):
            es.set(t, fCommand=0)

        if not hasattr(self, 'setTHooks'):
            self.setTHooks = []
        self.setTHooks.append(update)

        def onDestroy(e, s=self, u=update):
            if u in s.setTHooks:
                s.setTHooks.remove(u)

        tl.bind('<Destroy>', onDestroy)
        return