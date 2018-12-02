from libpandaexpressModules import *
from DirectNotifyGlobal import *
from PythonUtil import *
from MessengerGlobal import *
import time, fnmatch, string, signal
from bisect import bisect
exit = -1
done = 0
cont = 1
globalClock = ClockObject.getGlobalClock()

def print_exc_plus():
    import sys, traceback
    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next

    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back

    stack.reverse()
    traceback.print_exc()
    print 'Locals by frame, innermost last'
    for frame in stack:
        print
        print 'Frame %s in %s at line %s' % (frame.f_code.co_name, frame.f_code.co_filename, frame.f_lineno)
        for key, value in frame.f_locals.items():
            print '\t%20s = ' % key,
            try:
                print value
            except:
                print '<ERROR WHILE PRINTING VALUE>'


class Task:
    __module__ = __name__
    count = 0

    def __init__(self, callback, priority=0):
        self.id = Task.count
        Task.count += 1
        self.__call__ = callback
        self.__priority = priority
        self.uponDeath = None
        self.dt = 0.0
        self.maxDt = 0.0
        self.avgDt = 0.0
        self.runningTotal = 0.0
        self.pstats = None
        self.__removed = 0
        self.__onDoLaterList = 0
        return

    def setOnDoLaterList(self, status):
        self.__onDoLaterList = status

    def isOnDoLaterList(self):
        return self.__onDoLaterList

    def remove(self):
        self.__removed = 1

    def isRemoved(self):
        return self.__removed

    def getPriority(self):
        return self.__priority

    def setPriority(self, pri):
        self.__priority = pri

    def setStartTimeFrame(self, startTime, startFrame):
        self.starttime = startTime
        self.startframe = startFrame

    def setCurrentTimeFrame(self, currentTime, currentFrame):
        self.time = currentTime - self.starttime
        self.frame = currentFrame - self.startframe

    def setupPStats(self, name):
        pass

    def finishTask(self, verbose):
        if self.uponDeath:
            self.uponDeath(self)
        if verbose:
            messenger.send('TaskManager-removeTask', sentArgs=[self, self.name])

    def __repr__(self):
        if hasattr(self, 'name'):
            return 'Task id: %s, name %s' % (self.id, self.name)
        else:
            return 'Task id: %s, no name' % self.id


def pause(delayTime):

    def func(self):
        if self.time < self.delayTime:
            return cont
        else:
            return done

    task = Task(func)
    task.name = 'pause'
    task.delayTime = delayTime
    return task


def sequence(*taskList):
    return make_sequence(taskList)


def make_sequence(taskList):

    def func(self):
        frameFinished = 0
        taskDoneStatus = -1
        while not frameFinished:
            task = self.taskList[self.index]
            if self.index > self.prevIndex:
                task.setStartTimeFrame(self.time, self.frame)
            self.prevIndex = self.index
            task.setCurrentTimeFrame(self.time, self.frame)
            ret = task(task)
            if ret == cont:
                taskDoneStatus = cont
                frameFinished = 1
            else:
                if ret == done:
                    self.index = self.index + 1
                    taskDoneStatus = cont
                    frameFinished = 0
                else:
                    if ret == exit:
                        taskDoneStatus = exit
                        frameFinished = 1
            if self.index >= len(self.taskList):
                frameFinished = 1
                taskDoneStatus = done

        return taskDoneStatus

    task = Task(func)
    task.name = 'sequence'
    task.taskList = taskList
    task.prevIndex = -1
    task.index = 0
    return task


def resetSequence(task):
    task.index = 0
    task.prevIndex = -1


def loop(*taskList):
    return make_loop(taskList)


def make_loop(taskList):

    def func(self):
        frameFinished = 0
        taskDoneStatus = -1
        while not frameFinished:
            task = self.taskList[self.index]
            if self.index > self.prevIndex:
                task.setStartTimeFrame(self.time, self.frame)
            self.prevIndex = self.index
            task.setCurrentTimeFrame(self.time, self.frame)
            ret = task(task)
            if ret == cont:
                taskDoneStatus = cont
                frameFinished = 1
            else:
                if ret == done:
                    self.index = self.index + 1
                    taskDoneStatus = cont
                    frameFinished = 0
                else:
                    if ret == exit:
                        taskDoneStatus = exit
                        frameFinished = 1
            if self.index >= len(self.taskList):
                self.prevIndex = -1
                self.index = 0
                frameFinished = 1

        return taskDoneStatus

    task = Task(func)
    task.name = 'loop'
    task.taskList = taskList
    task.prevIndex = -1
    task.index = 0
    return task


class TaskPriorityList(list):
    __module__ = __name__

    def __init__(self, priority):
        self.__priority = priority
        self.__emptyIndex = 0

    def getPriority(self):
        return self.__priority

    def getEmptyIndex(self):
        return self.__emptyIndex

    def setEmptyIndex(self, index):
        self.__emptyIndex = index

    def add(self, task):
        if self.__emptyIndex >= len(self):
            self.append(task)
            self.__emptyIndex += 1
        else:
            self[self.__emptyIndex] = task
            self.__emptyIndex += 1

    def remove(self, i):
        if len(self) == 1 and i == 1:
            self[i] = None
            self.__emptyIndex = 0
        else:
            lastElement = self[self.__emptyIndex - 1]
            self[i] = lastElement
            self[self.__emptyIndex - 1] = None
            self.__emptyIndex -= 1
        return


class DoLaterList(list):
    __module__ = __name__

    def __init__(self):
        list.__init__(self)

    def add(self, task):
        lo = 0
        hi = len(self)
        while lo < hi:
            mid = (lo + hi) // 2
            if task.wakeTime < self[mid].wakeTime:
                hi = mid
            else:
                lo = mid + 1

        list.insert(self, lo, task)
        return lo


class TaskManager:
    __module__ = __name__
    notify = None

    def __init__(self):
        self.running = 0
        self.stepping = 0
        self.taskList = []
        self.pendingTaskDict = {}
        self.doLaterList = DoLaterList()
        self.currentTime, self.currentFrame = self.__getTimeFrame()
        if TaskManager.notify == None:
            TaskManager.notify = directNotify.newCategory('TaskManager')
        self.taskTimerVerbose = 0
        self.extendedExceptions = 0
        self.fKeyboardInterrupt = 0
        self.interruptCount = 0
        self.pStatsTasks = 0
        self.resumeFunc = None
        self.fVerbose = 0
        self.nameDict = {}
        self.add(self.__doLaterProcessor, 'doLaterProcessor')
        return

    def stepping(self, value):
        self.stepping = value

    def setVerbose(self, value):
        self.fVerbose = value
        messenger.send('TaskManager-setVerbose', sentArgs=[value])

    def keyboardInterruptHandler(self, signalNumber, stackFrame):
        self.fKeyboardInterrupt = 1
        self.interruptCount += 1
        if self.interruptCount == 2:
            signal.signal(signal.SIGINT, signal.default_int_handler)

    def hasTaskNamed(self, taskName):
        tasks = self.nameDict.get(taskName)
        if tasks:
            for task in tasks:
                if not task.isRemoved():
                    return 1

        return 0

    def getTasksNamed(self, taskName):
        tasks = self.nameDict.get(taskName, [])
        if tasks:
            tasks = filter(lambda task: not task.isRemoved(), tasks)
        return tasks

    def __doLaterProcessor(self, task):
        while self.doLaterList:
            dl = self.doLaterList[0]
            if dl.isRemoved():
                del self.doLaterList[0]
                dl.setOnDoLaterList(0)
                continue
            else:
                if task.time < dl.wakeTime:
                    break
                else:
                    del self.doLaterList[0]
                    dl.setStartTimeFrame(self.currentTime, self.currentFrame)
                    dl.setOnDoLaterList(0)
                    self.__addPendingTask(dl)
                    continue

        return cont

    def __spawnDoLater(self, task):
        nameList = self.nameDict.setdefault(task.name, [])
        nameList.append(task)
        currentTime = globalClock.getFrameTime()
        task.setStartTimeFrame(currentTime, self.currentFrame)
        task.wakeTime = task.starttime + task.delayTime
        task.setOnDoLaterList(1)
        index = self.doLaterList.add(task)
        if self.fVerbose:
            messenger.send('TaskManager-spawnDoLater', sentArgs=[task, task.name, task.id])
        return task

    def doLater(self, delayTime, task, taskName):
        task.delayTime = delayTime
        task.name = taskName
        return self.__spawnDoLater(task)

    def doMethodLater(self, delayTime, func, taskName):
        task = Task(func)
        return self.doLater(delayTime, task, taskName)

    def add(self, funcOrTask, name, priority=0):
        if isinstance(funcOrTask, Task):
            funcOrTask.setPriority(priority)
            return self.__spawnTaskNamed(funcOrTask, name)
        else:
            if callable(funcOrTask):
                return self.__spawnMethodNamed(funcOrTask, name, priority)
            else:
                self.notify.error('add: Tried to add a task that was not a Task or a func')

    def __spawnMethodNamed(self, func, name, priority=0):
        task = Task(func, priority)
        return self.__spawnTaskNamed(task, name)

    def __spawnTaskNamed(self, task, name):
        task.name = name
        currentTime = globalClock.getFrameTime()
        task.setStartTimeFrame(currentTime, self.currentFrame)
        nameList = self.nameDict.setdefault(name, [])
        nameList.append(task)
        self.__addPendingTask(task)
        return task

    def __addPendingTask(self, task):
        pri = task.getPriority()
        if self.pendingTaskDict.has_key(pri):
            taskPriList = self.pendingTaskDict[pri]
        else:
            taskPriList = TaskPriorityList(pri)
            self.pendingTaskDict[pri] = taskPriList
        taskPriList.add(task)

    def __addNewTask(self, task):
        taskPriority = task.getPriority()
        index = len(self.taskList) - 1
        while 1:
            if index < 0:
                newList = TaskPriorityList(taskPriority)
                newList.add(task)
                self.taskList.insert(0, newList)
                break
            taskListPriority = self.taskList[index].getPriority()
            if taskListPriority == taskPriority:
                self.taskList[index].add(task)
                break
            else:
                if taskListPriority > taskPriority:
                    index = index - 1
                else:
                    if taskListPriority < taskPriority:
                        newList = TaskPriorityList(taskPriority)
                        newList.add(task)
                        if index == len(self.taskList) - 1:
                            self.taskList.append(newList)
                        else:
                            self.taskList.insert(index + 1, newList)
                        break

        if self.fVerbose:
            messenger.send('TaskManager-spawnTask', sentArgs=[task, task.name, index])
        return task

    def remove(self, taskOrName):
        if type(taskOrName) == type(''):
            return self.__removeTasksNamed(taskOrName)
        else:
            if isinstance(taskOrName, Task):
                return self.__removeTasksEqual(taskOrName)
            else:
                self.notify.error('remove takes a string or a Task')

    def removeTasksMatching(self, taskPattern):
        num = 0
        keyList = filter(lambda key: fnmatch.fnmatchcase(key, taskPattern), self.nameDict.keys())
        for key in keyList:
            num += self.__removeTasksNamed(key)

        return num

    def __removeTasksEqual(self, task):
        if self.__removeTaskFromNameDict(task):
            task.remove()
            if task.isOnDoLaterList():
                self.doLaterList.remove(task)
            task.finishTask(self.fVerbose)
            return 1
        else:
            return 0

    def __removeTasksNamed(self, taskName):
        if not self.nameDict.has_key(taskName):
            return 0
        for task in self.nameDict[taskName]:
            task.remove()
            if task.isOnDoLaterList():
                self.doLaterList.remove(task)
            task.finishTask(self.fVerbose)

        num = len(self.nameDict[taskName])
        del self.nameDict[taskName]
        return num

    def __removeTaskFromNameDict(self, task):
        taskName = task.name
        tasksWithName = self.nameDict.get(taskName)
        if tasksWithName:
            if task in tasksWithName:
                tasksWithName.remove(task)
                if len(tasksWithName) == 0:
                    del self.nameDict[taskName]
                return 1
        return 0

    def __executeTask(self, task):
        task.setCurrentTimeFrame(self.currentTime, self.currentFrame)
        if not self.taskTimerVerbose:
            ret = task(task)
        else:
            if task.pstats:
                task.pstats.start()
            startTime = globalClock.getRealTime()
            ret = task(task)
            endTime = globalClock.getRealTime()
            if task.pstats:
                task.pstats.stop()
            dt = endTime - startTime
            task.dt = dt
            if dt > task.maxDt:
                task.maxDt = dt
            task.runningTotal = task.runningTotal + dt
            if task.frame > 0:
                task.avgDt = task.runningTotal / task.frame
            else:
                task.avgDt = 0
        return ret

    def __stepThroughList(self, taskPriList):
        i = 0
        while i < len(taskPriList):
            task = taskPriList[i]
            if task is None:
                break
            if task.isRemoved():
                task.finishTask(self.fVerbose)
                taskPriList.remove(i)
                continue
            ret = self.__executeTask(task)
            if ret == cont:
                pass
            else:
                if ret == done or ret == exit:
                    if not task.isRemoved():
                        task.remove()
                        task.finishTask(self.fVerbose)
                        self.__removeTaskFromNameDict(task)
                    else:
                        self.__removeTaskFromNameDict(task)
                    taskPriList.remove(i)
                    continue
                else:
                    raise StandardError, 'Task named %s did not return cont, exit, or done' % task.name
            i += 1

        return

    def __addPendingTasksToTaskList(self):
        for taskList in self.pendingTaskDict.values():
            for task in taskList:
                if task and not task.isRemoved():
                    self.__addNewTask(task)

        self.pendingTaskDict.clear()

    def step(self):
        self.currentTime, self.currentFrame = self.__getTimeFrame()
        self.fKeyboardInterrupt = 0
        self.interruptCount = 0
        signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        priIndex = 0
        while priIndex < len(self.taskList):
            taskPriList = self.taskList[priIndex]
            pri = taskPriList.getPriority()
            self.__stepThroughList(taskPriList)
            pendingTasks = self.pendingTaskDict.get(pri, [])
            while pendingTasks:
                del self.pendingTaskDict[pri]
                self.__stepThroughList(pendingTasks)
                for task in pendingTasks:
                    if task and not task.isRemoved():
                        self.__addNewTask(task)

                pendingTasks = self.pendingTaskDict.get(pri, [])

            self.__addPendingTasksToTaskList()
            priIndex += 1

        self.__addPendingTasksToTaskList()
        signal.signal(signal.SIGINT, signal.default_int_handler)
        if self.fKeyboardInterrupt:
            raise KeyboardInterrupt
        return

    def run(self):
        t = globalClock.getFrameTime()
        timeDelta = t - globalClock.getRealTime()
        globalClock.setRealTime(t)
        messenger.send('resetClock', [timeDelta])
        if self.resumeFunc != None:
            self.resumeFunc()
        if self.stepping:
            self.step()
        self.running = 1
        while self.running:
            try:
                self.step()
            except KeyboardInterrupt:
                self.stop()
            except:
                if self.extendedExceptions:
                    self.stop()
                    print_exc_plus()
                else:
                    raise

        return

    def stop(self):
        self.running = 0

    def replaceMethod(self, oldMethod, newFunction):
        import new
        for taskPriList in self.taskList:
            for task in taskPriList:
                if task is None:
                    break
                method = task.__call__
                if type(method) == types.MethodType:
                    function = method.im_func
                else:
                    function = method
                if function == oldMethod:
                    newMethod = new.instancemethod(newFunction, method.im_self, method.im_class)
                    task.__call__ = newMethod
                    return 1

        return 0
        return

    def __repr__(self):
        taskNameWidth = 32
        dtWidth = 10
        priorityWidth = 10
        totalDt = 0
        totalAvgDt = 0
        str = ('taskList').ljust(taskNameWidth) + ('dt(ms)').rjust(dtWidth) + ('avg').rjust(dtWidth) + ('max').rjust(dtWidth) + ('priority').rjust(priorityWidth) + '\n'
        str = str + '---------------------------------------------------------------\n'
        for taskPriList in self.taskList:
            priority = `(taskPriList.getPriority())`
            for task in taskPriList:
                if task is None:
                    break
                totalDt = totalDt + task.dt
                totalAvgDt = totalAvgDt + task.avgDt
                if task.isRemoved():
                    taskName = '(R)' + task.name
                else:
                    taskName = task.name
                if self.taskTimerVerbose:
                    import fpformat
                    str = str + (taskName.ljust(taskNameWidth) + fpformat.fix(task.dt * 1000, 2).rjust(dtWidth) + fpformat.fix(task.avgDt * 1000, 2).rjust(dtWidth) + fpformat.fix(task.maxDt * 1000, 2).rjust(dtWidth) + priority.rjust(priorityWidth) + '\n')
                else:
                    str = str + (task.name.ljust(taskNameWidth) + ('----').rjust(dtWidth) + ('----').rjust(dtWidth) + ('----').rjust(dtWidth) + priority.rjust(priorityWidth) + '\n')

        str = str + '---------------------------------------------------------------\n'
        str = str + ' pendingTasks\n'
        str = str + '---------------------------------------------------------------\n'
        for pri, taskList in self.pendingTaskDict.items():
            for task in taskList:
                remainingTime = task.starttime - self.currentTime
                if task.isRemoved():
                    taskName = '(PR)' + task.name
                else:
                    taskName = '(P)' + task.name
                if self.taskTimerVerbose:
                    import fpformat
                    str = str + ('  ' + taskName.ljust(taskNameWidth - 2) + fpformat.fix(pri, 2).rjust(dtWidth) + '\n')
                else:
                    str = str + ('  ' + taskName.ljust(taskNameWidth - 2) + ('----').rjust(dtWidth) + '\n')

        str = str + '---------------------------------------------------------------\n'
        str = str + ' doLaterList\n'
        str = str + '---------------------------------------------------------------\n'
        for task in self.doLaterList:
            remainingTime = task.wakeTime - self.currentTime
            if task.isRemoved():
                taskName = '(R)' + task.name
            else:
                taskName = task.name
            if self.taskTimerVerbose:
                import fpformat
                str = str + ('  ' + taskName.ljust(taskNameWidth - 2) + fpformat.fix(remainingTime, 2).rjust(dtWidth) + '\n')
            else:
                str = str + ('  ' + taskName.ljust(taskNameWidth - 2) + ('----').rjust(dtWidth) + '\n')

        str = str + '---------------------------------------------------------------\n'
        if self.taskTimerVerbose:
            import fpformat
            str = str + (('total').ljust(taskNameWidth) + fpformat.fix(totalDt * 1000, 2).rjust(dtWidth) + fpformat.fix(totalAvgDt * 1000, 2).rjust(dtWidth) + '\n')
        else:
            str = str + (('total').ljust(taskNameWidth) + ('----').rjust(dtWidth) + ('----').rjust(dtWidth) + '\n')
        return str
        return

    def resetStats(self):
        for task in self.taskList:
            task.dt = 0
            task.avgDt = 0
            task.maxDt = 0
            task.runningTotal = 0
            task.setStartTimeFrame(self.currentTime, self.currentFrame)

    def popupControls(self):
        import TaskManagerPanel
        return TaskManagerPanel.TaskManagerPanel(self)

    def __getTimeFrame(self):
        return (
         globalClock.getFrameTime(), globalClock.getFrameCount())