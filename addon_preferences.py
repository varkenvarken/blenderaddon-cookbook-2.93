#  addon_preferences.py
#
#  (c) 2017 - 2021 Michel Anders
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.


import bpy
from bpy.props import StringProperty, IntProperty
from random import randint

bl_info = {
	"name": "Add particle system",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202104291115),
	"blender": (2, 92, 0),
	"location": "View3D > Object > Add particle system",
	"description": "Add a particle system with default # of particles set in add-on prefs",
	"category": "Experimental development"}

class ParticlePrefs(bpy.types.AddonPreferences):
	bl_idname = __name__  # give settings the name of the python module

	particle_count = IntProperty(
		name="Default # of particles",
		default=100, min=1, soft_max=1000)

	# unlike a Operator the draw() function of an
	# AddonPreferences derived class must be overridden to
	# produce something meaningful. Defined properties are
	# *not* drawn automatically!
	def draw(self, context):
		layout = self.layout
		layout.prop(self, "particle_count")

class AddParticlesOp2(bpy.types.Operator):
	bl_idname = 'mesh.addparticlesystem2'
	bl_label = 'Add particle system'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		prefs = context.preferences.addons[__name__].preferences

		settings = 'Particles' + str(prefs.particle_count)

		if settings not in bpy.data.particles:
			settings = bpy.data.particles.new(settings)
		else:
			settings = bpy.data.particles[settings]
		settings.count = prefs.particle_count

		ob = context.active_object
		if ob:
			# a particle system is a modifier! However, we
			# cannot alter properties of this modifier
			pm = ob.modifiers.new('Particles','PARTICLE_SYSTEM')
			if pm:  # could be None if object is Camera or something
				# some things are controlled by the system
				# for instanc the random seed
				pm.particle_system.seed = randint(0,1000000)
				# other by the settings, which is a seperate
				# object that can be shared by different
				# particle systems
				pm.particle_system.settings = settings
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		AddParticlesOp2.bl_idname,
		text=AddParticlesOp2.bl_label,
		icon='PLUGIN')


classes = [AddParticlesOp2, ParticlePrefs]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_add.remove(menu_func)
	unregister_classes()
