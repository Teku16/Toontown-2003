from ShowBaseGlobal import *
from ToontownGlobals import *
from DirectGui import *
import Task

class ToontownTimer(DirectFrame):
    __module__ = __name__
    ClockImage = None

    def __init__(self):
        DirectFrame.__init__(self, relief=None, scale=0.45, image=self.getImage(), text='0', text_fg=(0, 0, 0, 1), text_font=getInterfaceFont(), text_pos=(-0.01, -0.15), text_scale=0.35)
        self.initialiseoptions(ToontownTimer)
        self.countdownTask = None
        self.currentTime = 0
        return

    def getImage(self):
        if ToontownTimer.ClockImage == None:
            model = loader.loadModel('phase_3.5/models/gui/clock_gui')
            ToontownTimer.ClockImage = model.find('**/alarm_clock')
            model.removeNode()
        return ToontownTimer.ClockImage
        return

    def posInTopRightCorner(self):
        self.setPos(1.16, 0, 0.83)
        return

    def setTime(self, time):
        if time < 0:
            time = 0
        if time > 999:
            time = 999
        if time == self.currentTime:
            return
        self.currentTime = time
        timeStr = str(time)
        timeStrLen = len(timeStr)
        self['text'] = ''
        if time <= 5:
            self['text_fg'] = Vec4(1, 0, 0, 1)
        else:
            self['text_fg'] = Vec4(0, 0, 0, 1)
        if len(timeStr) == 1:
            self['text_scale'] = 0.34
            self['text_pos'] = (-0.025, -0.125)
        else:
            if len(timeStr) == 2:
                self['text_scale'] = 0.27
                self['text_pos'] = (-0.025, -0.1)
            else:
                if len(timeStr) == 3:
                    self['text_scale'] = 0.2
                    self['text_pos'] = (-0.01, -0.08)
        self['text'] = timeStr
        return

    def _timerTask(self, task):
        countdownTime = int(task.duration - task.time)
        self.setTime(countdownTime)
        if task.time >= task.duration:
            if task.callback:
                task.callback()
            return Task.done
        else:
            return Task.cont

    def countdown(self, duration, callback=None):
        self.countdownTask = Task.Task(self._timerTask)
        self.countdownTask.duration = duration
        self.countdownTask.callback = callback
        taskMgr.remove('timerTask')
        return taskMgr.add(self.countdownTask, 'timerTask')

    def stop(self):
        if self.countdownTask:
            taskMgr.remove(self.countdownTask)

    def reset(self):
        self.stop()
        self.setTime(0)

    def destroy(self):
        self.reset()
        self.countdownTask = None
        DirectFrame.destroy(self)
        return
        return

    def cleanup(self):
        self.destroy()
        self.notify.warning('Call destroy, not cleanup')
        return