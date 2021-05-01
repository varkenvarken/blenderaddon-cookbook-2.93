#  addmodifier.py
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

bl_info = {
	"name": "Add Modifier",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202104291106),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Object > Add Modifier",
	"description": "Add a modifier",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class AddModifier(bpy.types.Operator):
	bl_idname = 'mesh.addmodifier'
	bl_label = 'Add Modifier'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

#https://www.blender.org/api/blender_python_api_current/bpy.types.ObjectModifiers.html

	def execute(self, context):
		ob = context.active_object
		mod = ob.modifiers.new('NewModifier','SUBSURF')
		# all objects have a modifiers attribute, but not
		# all type of object can take modifiers, for example
		# a lamp cannot. In that case new() will return None
		if mod:
			# some properties are common to all types
			mod.show_in_editmode = True
			# others are type specific
			mod.render_levels = 2
			mod.levels = 2
		return {"FINISHED"}

def menu_func(self, context):
	self.layout.operator(
		AddModifier.bl_idname,
		text=AddModifier.bl_label,
		icon='PLUGIN')

classes = [AddModifier]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_add.remove(menu_func)
	unregister_classes()
