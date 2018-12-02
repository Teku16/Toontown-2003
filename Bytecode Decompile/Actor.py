from PandaObject import *
import LODNode

class Actor(PandaObject, NodePath):
    __module__ = __name__
    notify = directNotify.newCategory('Actor')
    partPrefix = '__Actor_'

    def __init__(self, models=None, anims=None, other=None):
        try:
            self.Actor_initialized
            return
        except:
            self.Actor_initialized = 1
        else:
            NodePath.__init__(self)
            self.__partBundleDict = {}
            self.__animControlDict = {}
            self.__LODNode = None
            if other == None:
                self.gotName = 0
                root = ModelNode('actor')
                root.setPreserveTransform(1)
                self.assign(NodePath(root))
                self.setGeomNode(self.attachNewNode(ModelNode('actorGeom')))
                self.__hasLOD = 0
                if models:
                    if type(models) == type({}):
                        if type(models[models.keys()[0]]) == type({}):
                            self.setLODNode()
                            sortedKeys = models.keys()
                            sortedKeys.sort()
                            for lodName in sortedKeys:
                                self.addLOD(str(lodName))
                                for modelName in models[lodName].keys():
                                    self.loadModel(models[lodName][modelName], modelName, lodName)

                        if type(anims[anims.keys()[0]]) == type({}):
                            for partName in models.keys():
                                self.loadModel(models[partName], partName)

                        self.setLODNode()
                        sortedKeys = models.keys()
                        sortedKeys.sort()
                        for lodName in sortedKeys:
                            self.addLOD(str(lodName))
                            self.loadModel(models[lodName], lodName=lodName)

                    else:
                        self.loadModel(models)
                if anims:
                    if len(anims) >= 1:
                        if type(anims[anims.keys()[0]]) == type({}):
                            if type(models) == type({}):
                                if type(models[models.keys()[0]]) == type({}):
                                    sortedKeys = models.keys()
                                    sortedKeys.sort()
                                    for lodName in sortedKeys:
                                        for partName in anims.keys():
                                            self.loadAnims(anims[partName], partName, lodName)

                                for partName in anims.keys():
                                    self.loadAnims(anims[partName], partName)

                        else:
                            if type(models) == type({}):
                                sortedKeys = models.keys()
                                sortedKeys.sort()
                                for lodName in sortedKeys:
                                    self.loadAnims(anims, lodName=lodName)

                            else:
                                self.loadAnims(anims)
            otherCopy = other.copyTo(hidden)
            otherCopy.detachNode()
            self.gotName = other.gotName
            self.assign(otherCopy)
            self.setGeomNode(otherCopy.getChild(0))
            self.__copyPartBundles(other)
            self.__copyAnimControls(other)

        self.__geomNode.node().setFinal(1)
        return

    def delete(self):
        try:
            self.Actor_deleted
            return
        except:
            self.Actor_deleted = 1
            self.cleanup()

    def __cmp__(self, other):
        if self is other:
            return 0
        else:
            return 1

    def __str__(self):
        return 'Actor: partBundleDict = %s,\n animControlDict = %s' % (self.__partBundleDict, self.__animControlDict)

    def getActorInfo(self):
        lodInfo = []
        for lodName in self.__animControlDict.keys():
            partDict = self.__animControlDict[lodName]
            partInfo = []
            for partName in partDict.keys():
                partBundle = self.__partBundleDict[lodName][partName]
                animDict = partDict[partName]
                animInfo = []
                for animName in animDict.keys():
                    file = animDict[animName][0]
                    animControl = animDict[animName][1]
                    animInfo.append([animName, file, animControl])

                partInfo.append([partName, partBundle, animInfo])

            lodInfo.append([lodName, partInfo])

        return lodInfo

    def getAnimNames(self):
        animNames = []
        for lodName, lodInfo in self.getActorInfo():
            for partName, bundle, animInfo in lodInfo:
                for animName, file, animControl in animInfo:
                    if animName not in animNames:
                        animNames.append(animName)

        return animNames

    def pprint(self):
        for lodName, lodInfo in self.getActorInfo():
            print 'LOD:', lodName
            for partName, bundle, animInfo in lodInfo:
                print '  Part:', partName
                print '  Bundle:', `bundle`
                for animName, file, animControl in animInfo:
                    print '    Anim:', animName
                    print '      File:', file
                    if animControl == None:
                        print ' (not loaded)'
                    else:
                        print '      NumFrames: %d PlayRate: %0.2f' % (animControl.getNumFrames(), animControl.getPlayRate())

        return

    def cleanup(self):
        self.stop()
        del self.__partBundleDict
        del self.__animControlDict
        self.__geomNode.removeNode()
        del self.__geomNode
        if self.__LODNode:
            self.__LODNode.removeNode()
        del self.__LODNode
        self.__hasLOD = 0
        if not self.isEmpty():
            self.removeNode()

    def getAnimControlDict(self):
        return self.__animControlDict

    def getPartBundleDict(self):
        return self.__partBundleDict

    def getLODNames(self):
        lodNames = self.__partBundleDict.keys()
        lodNames.sort(lambda x, y: cmp(int(y), int(x)))
        return lodNames

    def getPartNames(self):
        return self.__partBundleDict.values()[0].keys()

    def getGeomNode(self):
        return self.__geomNode

    def setGeomNode(self, node):
        self.__geomNode = node

    def getLODNode(self):
        return self.__LODNode.node()

    def setLODNode(self, node=None):
        if node == None:
            lod = LODNode.LODNode('lod')
            self.__LODNode = self.__geomNode.attachNewNode(lod)
        else:
            self.__LODNode = self.__geomNode.attachNewNode(node)
        self.__hasLOD = 1
        self.switches = {}
        return

    def useLOD(self, lodName):
        self.resetLOD()
        sortedKeys = self.switches.keys()
        sortedKeys.sort()
        for eachLod in sortedKeys:
            index = sortedKeys.index(eachLod)
            self.__LODNode.node().setSwitch(index, 0, 10000)

        index = sortedKeys.index(lodName)
        self.__LODNode.node().setSwitch(index, 10000, 0)

    def printLOD(self):
        sortedKeys = self.switches.keys()
        sortedKeys.sort()
        for eachLod in sortedKeys:
            print 'python switches for %s: in: %d, out %d' % (eachLod, self.switches[eachLod][0], self.switches[eachLod][1])

        switchNum = self.__LODNode.node().getNumSwitches()
        for eachSwitch in range(0, switchNum):
            print 'c++ switches for %d: in: %d, out: %d' % (eachSwitch, self.__LODNode.node().getIn(eachSwitch), self.__LODNode.node().getOut(eachSwitch))

    def resetLOD(self):
        sortedKeys = self.switches.keys()
        sortedKeys.sort()
        for eachLod in sortedKeys:
            index = sortedKeys.index(eachLod)
            self.__LODNode.node().setSwitch(index, self.switches[eachLod][0], self.switches[eachLod][1])

    def addLOD(self, lodName, inDist=0, outDist=0):
        self.__LODNode.attachNewNode(str(lodName))
        self.switches[lodName] = [
         inDist, outDist]
        self.__LODNode.node().addSwitch(inDist, outDist)

    def setLOD(self, lodName, inDist=0, outDist=0):
        self.switches[lodName] = [
         inDist, outDist]
        sortedKeys = self.switches.keys()
        sortedKeys.sort()
        index = sortedKeys.index(lodName)
        self.__LODNode.node().setSwitch(index, inDist, outDist)

    def getLOD(self, lodName):
        lod = self.__LODNode.find('**/' + str(lodName))
        if lod.isEmpty():
            return None
        else:
            return lod
        return

    def hasLOD(self):
        return self.__hasLOD

    def update(self, lod=0):
        lodnames = self.getLODNames()
        if lod < len(lodnames):
            partBundles = self.__partBundleDict[lodnames[lod]].values()
            for partBundle in partBundles:
                partBundle.node().updateToNow()

        else:
            self.notify.warning('update() - no lod: %d' % lod)

    def getFrameRate(self, animName=None, partName=None):
        lodName = self.__animControlDict.keys()[0]
        controls = self.getAnimControls(animName, partName)
        if len(controls) == 0:
            return None
        return controls[0].getFrameRate()
        return

    def getBaseFrameRate(self, animName=None, partName=None):
        lodName = self.__animControlDict.keys()[0]
        controls = self.getAnimControls(animName, partName)
        if len(controls) == 0:
            return None
        return controls[0].getAnim().getBaseFrameRate()
        return

    def getPlayRate(self, animName=None, partName=None):
        lodName = self.__animControlDict.keys()[0]
        controls = self.getAnimControls(animName, partName)
        if len(controls) == 0:
            return None
        return controls[0].getPlayRate()
        return

    def setPlayRate(self, rate, animName, partName=None):
        for control in self.getAnimControls(animName, partName):
            control.setPlayRate(rate)

    def getDuration(self, animName=None, partName=None):
        lodName = self.__animControlDict.keys()[0]
        controls = self.getAnimControls(animName, partName)
        if len(controls) == 0:
            return None
        animControl = controls[0]
        return animControl.getNumFrames() / animControl.getFrameRate()
        return

    def getNumFrames(self, animName=None, partName=None):
        lodName = self.__animControlDict.keys()[0]
        controls = self.getAnimControls(animName, partName)
        if len(controls) == 0:
            return None
        return controls[0].getNumFrames()
        return

    def getCurrentAnim(self, partName=None):
        lodName, animControlDict = self.__animControlDict.items()[0]
        if partName == None:
            partName, animDict = animControlDict.items()[0]
        else:
            animDict = animControlDict.get(partName)
            if animDict == None:
                Actor.notify.warning("couldn't find part: %s" % partName)
                return None
        for animName, anim in animDict.items():
            if isinstance(anim[1], AnimControl) and anim[1].isPlaying():
                return animName

        return None
        return

    def getCurrentFrame(self, animName=None, partName=None):
        lodName, animControlDict = self.__animControlDict.items()[0]
        if partName == None:
            partName, animDict = animControlDict.items()[0]
        else:
            animDict = animControlDict.get(partName)
            if animDict == None:
                Actor.notify.warning("couldn't find part: %s" % partName)
                return None
        for animName, anim in animDict.items():
            if isinstance(anim[1], AnimControl) and anim[1].isPlaying():
                return anim[1].getFrame()

        return None
        return

    def getPart(self, partName, lodName='lodRoot'):
        if self.__partBundleDict.has_key(lodName):
            partBundleDict = self.__partBundleDict[lodName]
        else:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        if partBundleDict.has_key(partName):
            return partBundleDict[partName]
        else:
            return None
        return

    def removePart(self, partName, lodName='lodRoot'):
        if self.__partBundleDict.has_key(lodName):
            partBundleDict = self.__partBundleDict[lodName]
        else:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        if self.__animControlDict.has_key(lodName):
            animControlDict = self.__animControlDict[lodName]
        else:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        if partBundleDict.has_key(partName):
            partBundleDict[partName].removeNode()
            del partBundleDict[partName]
        if animControlDict.has_key(partName):
            del animControlDict[partName]
        return

    def hidePart(self, partName, lodName='lodRoot'):
        if self.__partBundleDict.has_key(lodName):
            partBundleDict = self.__partBundleDict[lodName]
        else:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        if partBundleDict.has_key(partName):
            partBundleDict[partName].hide()
        else:
            Actor.notify.warning('no part named %s!' % partName)
        return

    def showPart(self, partName, lodName='lodRoot'):
        if self.__partBundleDict.has_key(lodName):
            partBundleDict = self.__partBundleDict[lodName]
        else:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        if partBundleDict.has_key(partName):
            partBundleDict[partName].show()
        else:
            Actor.notify.warning('no part named %s!' % partName)
        return

    def showAllParts(self, partName, lodName='lodRoot'):
        if self.__partBundleDict.has_key(lodName):
            partBundleDict = self.__partBundleDict[lodName]
        else:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        if partBundleDict.has_key(partName):
            partBundleDict[partName].show()
            children = partBundleDict[partName].getChildren()
            numChildren = children.getNumPaths()
            for childNum in range(0, numChildren):
                children.getPath(childNum).show()

        else:
            Actor.notify.warning('no part named %s!' % partName)
        return

    def exposeJoint(self, node, partName, jointName, lodName='lodRoot'):
        if self.__partBundleDict.has_key(lodName):
            partBundleDict = self.__partBundleDict[lodName]
        else:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        if partBundleDict.has_key(partName):
            bundle = partBundleDict[partName].node().getBundle()
        else:
            Actor.notify.warning('no part named %s!' % partName)
            return None
        joint = bundle.findChild(jointName)
        if joint:
            joint.addNetTransform(node.node())
        else:
            Actor.notify.warning('no joint named %s!' % jointName)
        return

    def stopJoint(self, partName, jointName, lodName='lodRoot'):
        if self.__partBundleDict.has_key(lodName):
            partBundleDict = self.__partBundleDict[lodName]
        else:
            Actor.notify.warning('no lod named: %s' % lodName)
            return None
        if partBundleDict.has_key(partName):
            bundle = partBundleDict[partName].node().getBundle()
        else:
            Actor.notify.warning('no part named %s!' % partName)
            return None
        joint = bundle.findChild(jointName)
        if joint:
            joint.clearNetTransforms()
            joint.clearLocalTransforms()
        else:
            Actor.notify.warning('no joint named %s!' % jointName)
        return

    def instance(self, path, part, jointName, lodName='lodRoot'):
        if self.__partBundleDict.has_key(lodName):
            partBundleDict = self.__partBundleDict[lodName]
            if partBundleDict.has_key(part):
                joint = partBundleDict[part].find('**/' + jointName)
                if joint.isEmpty():
                    Actor.notify.warning('%s not found!' % jointName)
                else:
                    return path.instanceTo(joint)
            else:
                Actor.notify.warning('no part named %s!' % part)
        else:
            Actor.notify.warning('no lod named %s!' % lodName)

    def attach(self, partName, anotherPart, jointName, lodName='lodRoot'):
        if self.__partBundleDict.has_key(lodName):
            partBundleDict = self.__partBundleDict[lodName]
            if partBundleDict.has_key(partName):
                if partBundleDict.has_key(anotherPart):
                    joint = partBundleDict[anotherPart].find('**/' + jointName)
                    if joint.isEmpty():
                        Actor.notify.warning('%s not found!' % jointName)
                    else:
                        partBundleDict[partName].reparentTo(joint)
                else:
                    Actor.notify.warning('no part named %s!' % anotherPart)
            else:
                Actor.notify.warning('no part named %s!' % partName)
        else:
            Actor.notify.warning('no lod named %s!' % lodName)

    def drawInFront(self, frontPartName, backPartName, mode, root=None, lodName=None):
        if lodName != None:
            lodRoot = self.find('**/' + str(lodName))
            if root == None:
                root = lodRoot
            else:
                root = lodRoot.find('**/' + root)
        else:
            if root == None:
                root = self
        frontParts = root.findAllMatches('**/' + frontPartName)
        if mode > 0:
            numFrontParts = frontParts.getNumPaths()
            for partNum in range(0, numFrontParts):
                frontParts[partNum].setBin('fixed', mode)

            return
        if mode == -2:
            numFrontParts = frontParts.getNumPaths()
            for partNum in range(0, numFrontParts):
                frontParts[partNum].setDepthWrite(0)
                frontParts[partNum].setDepthTest(0)

        backPart = root.find('**/' + backPartName)
        if backPart.isEmpty():
            Actor.notify.warning('no part named %s!' % backPartName)
            return
        if mode == -3:
            backPart.node().setEffect(DecalEffect.make())
        else:
            backPart.reparentTo(backPart.getParent(), -1)
        frontParts.reparentTo(backPart)
        return

    def fixBounds(self, part=None):
        if part == None:
            part = self
        charNodes = part.findAllMatches('**/+Character')
        numCharNodes = charNodes.getNumPaths()
        for charNum in range(0, numCharNodes):
            charNodes.getPath(charNum).node().update()

        geomNodes = part.findAllMatches('**/+GeomNode')
        numGeomNodes = geomNodes.getNumPaths()
        for nodeNum in range(0, numGeomNodes):
            thisGeomNode = geomNodes.getPath(nodeNum)
            numGeoms = thisGeomNode.node().getNumGeoms()
            for geomNum in range(0, numGeoms):
                thisGeom = thisGeomNode.node().getGeom(geomNum)
                thisGeom.markBoundStale()
                Actor.notify.debug('fixing bounds for node %s, geom %s' % (nodeNum, geomNum))

            thisGeomNode.node().markBoundStale()

        return

    def showAllBounds(self):
        geomNodes = self.__geomNode.findAllMatches('**/+GeomNode')
        numGeomNodes = geomNodes.getNumPaths()
        for nodeNum in range(0, numGeomNodes):
            geomNodes.getPath(nodeNum).showBounds()

    def hideAllBounds(self):
        geomNodes = self.__geomNode.findAllMatches('**/+GeomNode')
        numGeomNodes = geomNodes.getNumPaths()
        for nodeNum in range(0, numGeomNodes):
            geomNodes.getPath(nodeNum).hideBounds()

    def animPanel(self):
        import TkGlobal, AnimPanel
        return AnimPanel.AnimPanel(self)

    def stop(self, animName=None, partName=None):
        for control in self.getAnimControls(animName, partName):
            control.stop()

    def play(self, animName, partName=None, fromFrame=None, toFrame=None):
        if fromFrame == None:
            for control in self.getAnimControls(animName, partName):
                control.play()

        for control in self.getAnimControls(animName, partName):
            control.play(fromFrame, toFrame)

        return

    def loop(self, animName, restart=1, partName=None, fromFrame=None, toFrame=None):
        if fromFrame == None:
            for control in self.getAnimControls(animName, partName):
                control.loop(restart)

        for control in self.getAnimControls(animName, partName):
            control.loop(restart, fromFrame, toFrame)

        return

    def pingpong(self, animName, fromFrame, toFrame, restart=1, partName=None):
        for control in self.getAnimControls(animName, partName):
            control.pingpong(restart, fromFrame, toFrame)

    def pose(self, animName, frame, partName=None, lodName=None):
        for control in self.getAnimControls(animName, partName, lodName):
            control.pose(frame)

    def enableBlend(self, blendType=PartBundle.BTNormalizedLinear, partName=None):
        for lodName, bundleDict in self.__partBundleDict.items():
            if partName == None:
                for partBundle in bundleDict.values():
                    partBundle.node().getBundle().setBlendType(blendType)

            else:
                partBundle = bundleDict.get(partName)
                if partBundle != None:
                    partBundle.node().getBundle().setBlendType(blendType)
                else:
                    Actor.notify.warning("Couldn't find part: %s" % partName)

        return

    def disableBlend(self, partName=None):
        self.enableBlend(PartBundle.BTSingle, partName)

    def setControlEffect(self, animName, effect, partName=None, lodName=None):
        for control in self.getAnimControls(animName, partName, lodName):
            control.getPart().setControlEffect(control, effect)

    def getAnimControl(self, animName, partName, lodName='lodRoot'):
        animControlDict = self.__animControlDict.get(lodName)
        animDict = animControlDict.get(partName)
        if animDict == None:
            Actor.notify.warning("couldn't find part: %s" % partName)
        else:
            anim = animDict.get(animName)
            if anim == None:
                Actor.notify.warning("couldn't find anim: %s" % animName)
            else:
                if not isinstance(anim[1], AnimControl):
                    self.__bindAnimToPart(animName, partName, lodName)
                return anim[1]
        return None
        return

    def getAnimControls(self, animName=None, partName=None, lodName=None):
        controls = []
        if lodName == None:
            animControlDictItems = self.__animControlDict.items()
        else:
            animControlDict = self.__animControlDict.get(lodName)
            if animControlDict == None:
                Actor.notify.warning("couldn't find lod: %s" % lodName)
                animControlDictItems = []
            else:
                animControlDictItems = [
                 (
                  lodName, animControlDict)]
        for lodName, animControlDict in animControlDictItems:
            if partName == None:
                animDictItems = animControlDict.items()
            else:
                animDict = animControlDict.get(partName)
                if animDict == None:
                    Actor.notify.warning("couldn't find part: %s" % partName)
                    animDictItems = []
                else:
                    animDictItems = [
                     (
                      partName, animDict)]
            if animName == None:
                for thisPart, animDict in animDictItems:
                    for anim in animDict.values():
                        if isinstance(anim[1], AnimControl) and anim[1].isPlaying():
                            controls.append(anim[1])

            for thisPart, animDict in animDictItems:
                anim = animDict.get(animName)
                if anim == None:
                    Actor.notify.warning("couldn't find anim: %s" % animName)
                else:
                    if not isinstance(anim[1], AnimControl):
                        if self.__bindAnimToPart(animName, thisPart, lodName):
                            controls.append(anim[1])
                    else:
                        controls.append(anim[1])

        return controls
        return

    def loadModel(self, modelPath, partName='modelRoot', lodName='lodRoot', copy=1):
        Actor.notify.debug('in loadModel: %s , part: %s, lod: %s, copy: %s' % (modelPath, partName, lodName, copy))
        if isinstance(modelPath, NodePath):
            if copy:
                model = modelPath.copyTo(hidden)
            else:
                model = modelPath
        else:
            if copy:
                model = loader.loadModelCopy(modelPath)
            else:
                model = loader.loadModelOnce(modelPath)
        if model == None:
            print 'model = None!!!'
        bundle = model.find('**/+PartBundleNode')
        if bundle.isEmpty():
            Actor.notify.warning('%s is not a character!' % modelPath)
        else:
            self.prepareBundle(bundle, partName, lodName)
            model.removeNode()
        return

    def prepareBundle(self, bundle, partName='modelRoot', lodName='lodRoot'):
        if not self.gotName:
            self.node().setName(bundle.node().getName())
            self.gotName = 1
        bundle.node().setName(Actor.partPrefix + partName)
        if self.__partBundleDict.has_key(lodName) == 0:
            needsDict = 1
            bundleDict = {}
        else:
            needsDict = 0
        if lodName != 'lodRoot':
            bundle.reparentTo(self.__LODNode.find('**/' + str(lodName)))
        else:
            bundle.reparentTo(self.__geomNode)
        if needsDict:
            bundleDict[partName] = bundle
            self.__partBundleDict[lodName] = bundleDict
        else:
            self.__partBundleDict[lodName][partName] = bundle

    def loadAnims(self, anims, partName='modelRoot', lodName='lodRoot'):
        Actor.notify.debug('in loadAnims: %s, part: %s, lod: %s' % (anims, partName, lodName))
        for animName in anims.keys():
            if not self.__animControlDict.has_key(lodName):
                lodDict = {}
                self.__animControlDict[lodName] = lodDict
            if not self.__animControlDict[lodName].has_key(partName):
                partDict = {}
                self.__animControlDict[lodName][partName] = partDict
            if not len(self.__animControlDict[lodName][partName].keys()):
                animDict = {}
                self.__animControlDict[lodName][partName] = animDict
            self.__animControlDict[lodName][partName][animName] = [
             anims[animName], None]

        return

    def unloadAnims(self, anims, partName='modelRoot', lodName='lodRoot'):
        Actor.notify.debug('in unloadAnims: %s, part: %s, lod: %s' % (anims, partName, lodName))
        if lodName == None:
            lodNames = self.__animControlDict.keys()
        else:
            lodNames = [
             lodName]
        if partName == None:
            if len(lodNames) > 0:
                partNames = self.__animControlDict[lodNames[0]].keys()
            else:
                partNames = []
        else:
            partNames = [
             partName]
        if anims == None:
            if len(lodNames) > 0 and len(partNames) > 0:
                anims = self.__animControlDict[lodNames[0]][partNames[0]].keys()
            else:
                anims = []
        for lodName in lodNames:
            for partName in partNames:
                for animName in anims:
                    animControlPair = self.__animControlDict[lodName][partName][animName]
                    if animControlPair[1] != None:
                        del animControlPair[1]
                        animControlPair.append(None)

        return

    def bindAnim(self, animName, partName='modelRoot', lodName='lodRoot'):
        if lodName == None:
            lodNames = self.__animControl.keys()
        else:
            lodNames = [
             lodName]
        for thisLod in lodNames:
            if partName == None:
                partNames = animControlDict[lodName].keys()
            else:
                partNames = [
                 partName]
            for thisPart in partNames:
                ac = self.__bindAnimToPart(animName, thisPart, thisLod)

        return

    def __bindAnimToPart(self, animName, partName, lodName):
        if not self.__animControlDict[lodName][partName].has_key(animName):
            Actor.notify.debug('actor has no animation %s', animName)
        if isinstance(self.__animControlDict[lodName][partName][animName][1], AnimControl):
            return None
        animPath = self.__animControlDict[lodName][partName][animName][0]
        anim = loader.loadModelOnce(animPath)
        if anim == None:
            return None
        animBundle = anim.find('**/+AnimBundleNode').node().getBundle()
        anim.removeNode()
        bundleNode = self.__partBundleDict[lodName][partName].node()
        animControl = bundleNode.getBundle().bindAnim(animBundle, -1)
        if animControl == None:
            Actor.notify.error('Null AnimControl: %s' % animName)
        else:
            self.__animControlDict[lodName][partName][animName][1] = animControl
            Actor.notify.debug('binding anim: %s to part: %s, lod: %s' % (animName, partName, lodName))
        return animControl
        return

    def __copyPartBundles(self, other):
        for lodName in other.__partBundleDict.keys():
            self.__partBundleDict[lodName] = {}
            for partName in other.__partBundleDict[lodName].keys():
                partBundle = self.find('**/' + Actor.partPrefix + partName)
                if partBundle != None:
                    self.__partBundleDict[lodName][partName] = partBundle
                else:
                    Actor.notify.error('lod: %s has no matching part: %s' % (lodName, partName))

        return

    def __copyAnimControls(self, other):
        for lodName in other.__animControlDict.keys():
            self.__animControlDict[lodName] = {}
            for partName in other.__animControlDict[lodName].keys():
                self.__animControlDict[lodName][partName] = {}
                for animName in other.__animControlDict[lodName][partName].keys():
                    self.__animControlDict[lodName][partName][animName] = [
                     other.__animControlDict[lodName][partName][animName][0], None]

        return

    def actorInterval(self, *args, **kw):
        import ActorInterval
        return ActorInterval.ActorInterval(self, *args, **kw)