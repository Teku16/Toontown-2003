from ParticleEffect import *
import os, DirectNotifyGlobal
notify = DirectNotifyGlobal.directNotify.newCategory('BattleParticles')
TutorialParticleEffects = (
 'gearExplosionBig.ptf', 'gearExplosionSmall.ptf', 'gearExplosion.ptf')
ParticleNames = (
 'audit-div', 'audit-five', 'audit-four', 'audit-minus', 'audit-mult', 'audit-one', 'audit-plus', 'audit-six', 'audit-three', 'audit-two', 'blah', 'brainstorm-box', 'brainstorm-env', 'brainstorm-track', 'buzzwords-crash', 'buzzwords-inc', 'buzzwords-main', 'buzzwords-over', 'buzzwords-syn', 'doubletalk-double', 'doubletalk-dup', 'doubletalk-good', 'filibuster-cut', 'filibuster-fiscal', 'filibuster-impeach', 'filibuster-inc', 'jargon-brow', 'jargon-deep', 'jargon-hoop', 'jargon-ipo', 'legalese-hc', 'legalese-qpq', 'legalese-vd', 'mumbojumbo-boiler', 'mumbojumbo-creative', 'mumbojumbo-deben', 'mumbojumbo-high', 'mumbojumbo-iron', 'poundsign', 'schmooze-genius', 'schmooze-instant', 'schmooze-master', 'schmooze-viz', 'roll-o-dex', 'rollodex-card', 'dagger', 'fire', 'snow-particle', 'raindrop', 'gear', 'checkmark', 'dollar-sign', 'spark')
particleModel = None
particleSearchPath = None

def loadParticles():
    global particleModel
    if particleModel == None:
        particleModel = loader.loadModel('phase_3.5/models/props/suit-particles')
    return


def unloadParticles():
    global particleModel
    if particleModel != None:
        particleModel.removeNode()
    del particleModel
    particleModel = None
    return


def getParticle(name):
    if name in ParticleNames:
        particle = particleModel.find('**/' + str(name))
        return particle
    else:
        notify.warning('getParticle() - no name: %s' % name)
        return None
    return


def loadParticleFile(name):
    global particleSearchPath
    if particleSearchPath == None:
        particleSearchPath = DSearchPath()
        particleSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TOONTOWN/src/battle')))
        particleSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TOONTOWN/src/safezone')))
        particleSearchPath.appendDirectory(Filename('phase_3.5/etc'))
        particleSearchPath.appendDirectory(Filename('phase_4/etc'))
        particleSearchPath.appendDirectory(Filename('phase_5/etc'))
        particleSearchPath.appendDirectory(Filename('phase_8/etc'))
    pfile = Filename(name)
    if vfs:
        found = vfs.resolveFilename(pfile, particleSearchPath)
    else:
        found = pfile.resolveFilename(particleSearchPath)
    if not found:
        notify.warning('loadParticleFile() - no path: %s' % name)
        return
    notify.debug('Loading particle file: %s' % pfile)
    effect = ParticleEffect()
    effect.loadConfig(pfile)
    return effect
    return


def createParticleEffect(name=None, file=None, numParticles=None, color=None):
    if not name:
        fileName = file + '.ptf'
        return loadParticleFile(fileName)
    if name == 'BigGearExplosion':
        return __makeBigGearExplosion(numParticles)
    else:
        if name == 'BrainStorm':
            return loadParticleFile('brainStorm.ptf')
        else:
            if name == 'BuzzWord':
                return loadParticleFile('buzzWord.ptf')
            else:
                if name == 'Calculate':
                    return loadParticleFile('calculate.ptf')
                else:
                    if name == 'DemotionFreeze':
                        return loadParticleFile('demotionFreeze.ptf')
                    else:
                        if name == 'DemotionSpray':
                            return loadParticleFile('demotionSpray.ptf')
                        else:
                            if name == 'DoubleTalkLeft':
                                return loadParticleFile('doubleTalkLeft.ptf')
                            else:
                                if name == 'DoubleTalkRight':
                                    return loadParticleFile('doubleTalkRight.ptf')
                                else:
                                    if name == 'FingerWag':
                                        return loadParticleFile('fingerwag.ptf')
                                    else:
                                        if name == 'FiredFlame':
                                            return loadParticleFile('firedFlame.ptf')
                                        else:
                                            if name == 'FreezeAssets':
                                                return loadParticleFile('freezeAssets.ptf')
                                            else:
                                                if name == 'GearExplosion':
                                                    return __makeGearExplosion(numParticles)
                                                else:
                                                    if name == 'GlowerPower':
                                                        return loadParticleFile('glowerPowerKnives.ptf')
                                                    else:
                                                        if name == 'HotAir':
                                                            return loadParticleFile('hotAirSpray.ptf')
                                                        else:
                                                            if name == 'PoundKey':
                                                                return loadParticleFile('poundkey.ptf')
                                                            else:
                                                                if name == 'ShiftSpray':
                                                                    return loadParticleFile('shiftSpray.ptf')
                                                                else:
                                                                    if name == 'ShiftLift':
                                                                        return __makeShiftLift()
                                                                    else:
                                                                        if name == 'Shred':
                                                                            return loadParticleFile('shred.ptf')
                                                                        else:
                                                                            if name == 'Smile':
                                                                                return loadParticleFile('smile.ptf')
                                                                            else:
                                                                                if name == 'SpriteFiredFlecks':
                                                                                    return loadParticleFile('spriteFiredFlecks.ptf')
                                                                                else:
                                                                                    if name == 'Synergy':
                                                                                        return loadParticleFile('synergy.ptf')
                                                                                    else:
                                                                                        if name == 'Waterfall':
                                                                                            return loadParticleFile('waterfall.ptf')
                                                                                        else:
                                                                                            if name == 'PoundKey':
                                                                                                return loadParticleFile('poundkey.ptf')
                                                                                            else:
                                                                                                if name == 'RubOut':
                                                                                                    return __makeRubOut(color)
                                                                                                else:
                                                                                                    if name == 'SplashLines':
                                                                                                        return loadParticleFile('splashlines.ptf')
                                                                                                    else:
                                                                                                        if name == 'Withdrawal':
                                                                                                            return loadParticleFile('withdrawal.ptf')
                                                                                                        else:
                                                                                                            notify.warning('createParticleEffect() - no name: %s' % name)
    return None
    return


def setEffectTexture(effect, name, color=None):
    particles = effect.getParticlesNamed('particles-1')
    np = getParticle(name)
    if color:
        particles.renderer.setColor(color)
    particles.renderer.setFromNode(np)


def __makeGearExplosion(numParticles=None):
    effect = loadParticleFile('gearExplosion.ptf')
    if numParticles:
        particles = effect.getParticlesNamed('particles-1')
        particles.setPoolSize(numParticles)
    return effect


def __makeBigGearExplosion(numParticles=None):
    effect = loadParticleFile('gearExplosionBig.ptf')
    if numParticles:
        particles = effect.getParticlesNamed('particles-1')
        particles.setPoolSize(numParticles)
    return effect


def __makeRubOut(color=None):
    effect = loadParticleFile('demotionUnFreeze.ptf')
    loadParticles()
    setEffectTexture(effect, 'snow-particle')
    particles = effect.getParticlesNamed('particles-1')
    particles.renderer.setInitialXScale(0.006)
    particles.renderer.setFinalXScale(0.0)
    particles.renderer.setInitialYScale(0.004)
    particles.renderer.setFinalYScale(0.0)
    if color:
        particles.renderer.setColor(color)
    else:
        particles.renderer.setColor(Vec4(0.54, 0.92, 0.32, 0.7))
    return effect


def __makeShiftLift():
    effect = loadParticleFile('pixieDrop.ptf')
    particles = effect.getParticlesNamed('particles-1')
    particles.renderer.setCenterColor(Vec4(1, 1, 0, 0.9))
    particles.renderer.setEdgeColor(Vec4(1, 1, 0, 0.6))
    particles.emitter.setRadius(0.01)
    effect.setHpr(0, 180, 0)
    effect.setPos(0, 0, 0)
    return effect