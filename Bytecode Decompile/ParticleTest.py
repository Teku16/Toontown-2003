from ShowBaseGlobal import *
import ParticleEffect, ParticlePanel, ForceGroup
base.enableParticles()
gravity = LinearVectorForce(Vec3(0.0, 0.0, -10.0))
fg = ForceGroup.ForceGroup()
fg.addForce(gravity)
pe = ParticleEffect.ParticleEffect('particle-fx')
pe.reparentTo(render)
pe.setPos(0.0, 5.0, 4.0)
pe.addForceGroup(fg)
pp = ParticlePanel.ParticlePanel(pe)