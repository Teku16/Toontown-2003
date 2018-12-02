from DirectObject import *
import types
FsmRedefine = 0
EnterFuncRedefineMap = {}
ExitFuncRedefineMap = {}

def redefineEnterFunc(oldMethod, newFunction):
    import new
    if not FsmRedefine:
        return
    for method in EnterFuncRedefineMap.keys():
        if type(method) == types.MethodType:
            function = method.im_func
        else:
            function = method
        if function == oldMethod:
            newMethod = new.instancemethod(newFunction, method.im_self, method.im_class)
            stateList = EnterFuncRedefineMap[method]
            for state in stateList:
                state.setEnterFunc(newMethod)

            return 1

    return 0


def redefineExitFunc(oldMethod, newFunction):
    import new
    if not FsmRedefine:
        return
    for method in ExitFuncRedefineMap.keys():
        if type(method) == types.MethodType:
            function = method.im_func
        else:
            function = method
        if function == oldMethod:
            newMethod = new.instancemethod(newFunction, method.im_self, method.im_class)
            stateList = ExitFuncRedefineMap[method]
            for state in stateList:
                state.setExitFunc(newMethod)

            return 1

    return 0


class State(DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('State')
    Any = 'ANY'

    def __init__(self, name, enterFunc=None, exitFunc=None, transitions=Any, inspectorPos=[]):
        self.__enterFunc = None
        self.__exitFunc = None
        self.setName(name)
        self.setEnterFunc(enterFunc)
        self.setExitFunc(exitFunc)
        self.setTransitions(transitions)
        self.setInspectorPos(inspectorPos)
        self.__FSMList = []
        return

    def getName(self):
        return self.__name

    def setName(self, stateName):
        self.__name = stateName

    def getEnterFunc(self):
        return self.__enterFunc

    def redefineFunc(self, oldMethod, newMethod, map):
        if not FsmRedefine:
            return
        if map.has_key(oldMethod):
            stateList = map[oldMethod]
            stateList.remove(self)
            if not stateList:
                del map[oldMethod]
        stateList = map.get(newMethod, [])
        stateList.append(self)
        map[newMethod] = stateList

    def setEnterFunc(self, stateEnterFunc):
        self.redefineFunc(self.__enterFunc, stateEnterFunc, EnterFuncRedefineMap)
        self.__enterFunc = stateEnterFunc

    def getExitFunc(self):
        return self.__exitFunc

    def setExitFunc(self, stateExitFunc):
        self.redefineFunc(self.__exitFunc, stateExitFunc, ExitFuncRedefineMap)
        self.__exitFunc = stateExitFunc

    def transitionsToAny(self):
        return self.__transitions is State.Any

    def getTransitions(self):
        if self.transitionsToAny():
            return []
        return self.__transitions

    def isTransitionDefined(self, otherState):
        if self.transitionsToAny():
            return 1
        if type(otherState) != type(''):
            otherState = otherState.getName()
        return otherState in self.__transitions

    def setTransitions(self, stateTransitions):
        self.__transitions = stateTransitions

    def addTransition(self, transition):
        if not self.transitionsToAny():
            self.__transitions.append(transition)
        else:
            State.notify.warning('attempted to add transition %s to state that transitions to any state')

    def getInspectorPos(self):
        return self.__inspectorPos

    def setInspectorPos(self, inspectorPos):
        self.__inspectorPos = inspectorPos

    def getChildren(self):
        return self.__FSMList

    def setChildren(self, FSMList):
        self.__FSMList = FSMList

    def addChild(self, FSM):
        self.__FSMList.append(FSM)

    def removeChild(self, FSM):
        if FSM in self.__FSMList:
            self.__FSMList.remove(FSM)

    def hasChildren(self):
        return len(self.__FSMList) > 0

    def __enterChildren(self, argList):
        for fsm in self.__FSMList:
            if fsm.getCurrentState():
                fsm.conditional_request(fsm.getInitialState().getName())
            else:
                fsm.enterInitialState()

    def __exitChildren(self, argList):
        for fsm in self.__FSMList:
            fsm.request(fsm.getFinalState().getName())

    def enter(self, argList=[]):
        self.__enterChildren(argList)
        if self.__enterFunc != None:
            apply(self.__enterFunc, argList)
        return

    def exit(self, argList=[]):
        self.__exitChildren(argList)
        if self.__exitFunc != None:
            apply(self.__exitFunc, argList)
        return

    def __str__(self):
        return 'State: name = %s, enter = %s, exit = %s, trans = %s, children = %s' % (self.__name, self.__enterFunc, self.__exitFunc, self.__transitions, self.__FSMList)