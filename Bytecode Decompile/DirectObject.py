from MessengerGlobal import *
from DirectNotifyGlobal import *
from PythonUtil import *

class DirectObject:
    __module__ = __name__

    def __initEvents(self):
        if not hasattr(self, 'events'):
            self.events = {}

    def accept(self, event, method, extraArgs=[]):
        self.__initEvents()
        self.events.setdefault(event, None)
        messenger.accept(event, self, method, extraArgs, 1)
        return

    def acceptOnce(self, event, method, extraArgs=[]):
        self.__initEvents()
        self.events.setdefault(event, None)
        messenger.accept(event, self, method, extraArgs, 0)
        return

    def _INTERNAL_acceptOnceExpired(self, event):
        if self.events.has_key(event):
            del self.events[event]

    def ignore(self, event):
        self.__initEvents()
        if self.events.has_key(event):
            del self.events[event]
        messenger.ignore(event, self)

    def ignoreAll(self):
        self.__initEvents()
        for event in self.events.keys():
            messenger.ignore(event, self)

        self.events.clear()

    def isAccepting(self, event):
        self.__initEvents()
        return self.events.has_key(event)

    def isIgnoring(self, event):
        return not self.isAccepting(event)