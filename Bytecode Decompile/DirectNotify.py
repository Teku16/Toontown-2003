import Notifier, Logger

class DirectNotify:
    __module__ = __name__

    def __init__(self):
        self.__categories = {}
        self.logger = Logger.Logger()
        self.streamWriter = None
        return

    def __str__(self):
        return 'DirectNotify categories: %s' % self.__categories

    def getCategories(self):
        return self.__categories.keys()

    def getCategory(self, categoryName):
        return self.__categories.get(categoryName, None)
        return

    def newCategory(self, categoryName, logger=None):
        if not self.__categories.has_key(categoryName):
            self.__categories[categoryName] = Notifier.Notifier(categoryName, logger)
            self.setDconfigLevel(categoryName)
        else:
            print "Warning: DirectNotify: category '%s' already exists" % categoryName
        return self.getCategory(categoryName)

    def setDconfigLevel(self, categoryName):
        try:
            config
        except:
            return 0
        else:
            dconfigParam = 'notify-level-' + categoryName
            level = config.GetString(dconfigParam, '')
            if level:
                print 'Setting DirectNotify category: ' + categoryName + ' to severity: ' + level
                category = self.getCategory(categoryName)
                if level == 'error':
                    category.setWarning(0)
                    category.setInfo(0)
                    category.setDebug(0)
                else:
                    if level == 'warning':
                        category.setWarning(1)
                        category.setInfo(0)
                        category.setDebug(0)
                    else:
                        if level == 'info':
                            category.setWarning(1)
                            category.setInfo(1)
                            category.setDebug(0)
                        else:
                            if level == 'debug':
                                category.setWarning(1)
                                category.setInfo(1)
                                category.setDebug(1)
                            else:
                                print 'DirectNotify: unknown notify level: ' + str(level) + ' for category: ' + str(categoryName)

    def setDconfigLevels(self):
        for categoryName in self.getCategories():
            self.setDconfigLevel(categoryName)

    def popupControls(self, tl=None):
        import NotifyPanel
        NotifyPanel.NotifyPanel(self, tl)