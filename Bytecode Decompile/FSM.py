from DirectObject import *
import types

class FSM(DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('FSM')
    ALLOW = 0
    DISALLOW = 1
    DISALLOW_VERBOSE = 2
    ERROR = 3

    def __init__(self, name, states=[], initialStateName=None, finalStateName=None, onUndefTransition=DISALLOW_VERBOSE):
        self.setName(name)
        self.setStates(states)
        self.setInitialState(initialStateName)
        self.setFinalState(finalStateName)
        self.onUndefTransition = onUndefTransition
        self.inspecting = 0
        self.__currentState = None
        self.__internalStateInFlux = 0
        return

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        currentState = self.getCurrentState()
        if currentState:
            str = 'FSM ' + self.getName() + ' in state "' + currentState.getName() + '"'
        else:
            str = 'FSM ' + self.getName() + ' not in any state'
        return str

    def enterInitialState(self, argList=[]):
        if self.__currentState == self.__initialState:
            return
        self.__internalStateInFlux = 1
        self.__enter(self.__initialState, argList)

    def __str_not__(self):
        return 'FSM: name = %s \n states = %s \n initial = %s \n final = %s \n current = %s' % (self.__name, self.__states, self.__initialState, self.__finalState, self.__currentState)

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getStates(self):
        return self.__states

    def setStates(self, states):
        self.__states = states

    def addState(self, state):
        self.__states.append(state)

    def getInitialState(self):
        return self.__initialState

    def setInitialState(self, initialStateName):
        self.__initialState = self.getStateNamed(initialStateName)

    def getFinalState(self):
        return self.__finalState

    def setFinalState(self, finalStateName):
        self.__finalState = self.getStateNamed(finalStateName)

    def requestFinalState(self):
        self.request(self.__finalState.getName())

    def getCurrentState(self):
        return self.__currentState

    def getStateNamed(self, stateName):
        for state in self.__states:
            if state.getName() == stateName:
                return state

        FSM.notify.warning('[%s] : getStateNamed: %s, no such state' % (self.__name, str(stateName)))

    def __exitCurrent(self, argList):
        if FSM.notify.getDebug():
            FSM.notify.debug('[%s]: exiting %s' % (self.__name, self.__currentState.getName()))
        self.__currentState.exit(argList)
        if self.inspecting:
            messenger.send(self.getName() + '_' + self.__currentState.getName() + '_exited')
        self.__currentState = None
        return

    def __enter(self, aState, argList=[]):
        if aState in self.__states:
            if FSM.notify.getDebug():
                FSM.notify.debug('[%s]: entering %s' % (self.__name, aState.getName()))
            self.__currentState = aState
            if self.inspecting:
                messenger.send(self.getName() + '_' + aState.getName() + '_entered')
            self.__internalStateInFlux = 0
            aState.enter(argList)
        else:
            self.__internalStateInFlux = 0
            FSM.notify.error('[%s]: enter: no such state' % self.__name)

    def __transition(self, aState, enterArgList=[], exitArgList=[]):
        self.__internalStateInFlux = 1
        self.__exitCurrent(exitArgList)
        self.__enter(aState, enterArgList)

    def request(self, aStateName, enterArgList=[], exitArgList=[], force=0):
        if not self.__currentState:
            FSM.notify.warning('[%s]: request: never entered initial state' % self.__name)
            self.__currentState = self.__initialState
        if isinstance(aStateName, types.StringType):
            aState = self.getStateNamed(aStateName)
        else:
            aState = aStateName
            aStateName = aState.getName()
        if aState == None:
            FSM.notify.error('[%s]: request: %s, no such state' % (self.__name, aStateName))
        transitionDefined = self.__currentState.isTransitionDefined(aStateName)
        transitionAllowed = transitionDefined
        if self.onUndefTransition == FSM.ALLOW:
            transitionAllowed = 1
            if not transitionDefined:
                FSM.notify.warning('[%s]: performing undefined transition from %s to %s' % (self.__name, self.__currentState.getName(), aStateName))
        if transitionAllowed or force:
            self.__transition(aState, enterArgList, exitArgList)
            return 1
        else:
            if aStateName == self.__finalState.getName():
                if self.__currentState == self.__finalState:
                    if FSM.notify.getDebug():
                        FSM.notify.debug('[%s]: already in final state: %s' % (self.__name, aStateName))
                    return 1
                else:
                    if FSM.notify.getDebug():
                        FSM.notify.debug('[%s]: implicit transition to final state: %s' % (self.__name, aStateName))
                    self.__transition(aState, enterArgList, exitArgList)
                    return 1
            else:
                if aStateName == self.__currentState.getName():
                    if FSM.notify.getDebug():
                        FSM.notify.debug('[%s]: already in state %s and no self transition' % (self.__name, aStateName))
                    return 0
                else:
                    msg = '[%s]: no transition exists from %s to %s' % (self.__name, self.__currentState.getName(), aStateName)
                    if self.onUndefTransition == FSM.ERROR:
                        FSM.notify.error(msg)
                    else:
                        if self.onUndefTransition == FSM.DISALLOW_VERBOSE:
                            FSM.notify.warning(msg)
                    return 0
        return

    def forceTransition(self, aStateName, enterArgList=[], exitArgList=[]):
        self.request(aStateName, enterArgList, exitArgList, force=1)

    def conditional_request(self, aStateName, enterArgList=[], exitArgList=[]):
        if not self.__currentState:
            FSM.notify.warning('[%s]: request: never entered initial state' % self.__name)
            self.__currentState = self.__initialState
        if isinstance(aStateName, types.StringType):
            aState = self.getStateNamed(aStateName)
        else:
            aState = aStateName
            aStateName = aState.getName()
        if aState == None:
            FSM.notify.error('[%s]: request: %s, no such state' % (self.__name, aStateName))
        transitionDefined = self.__currentState.isTransitionDefined(aStateName) or aStateName in [self.__currentState.getName(), self.__finalState.getName()]
        if transitionDefined:
            return self.request(aStateName, enterArgList, exitArgList)
        else:
            FSM.notify.debug('[%s]: condition_request: %s, transition doesnt exist' % (self.__name, aStateName))
            return 0
        return

    def view(self):
        import FSMInspector
        FSMInspector.FSMInspector(self)