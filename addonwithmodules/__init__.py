#  addonwithmodules
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

from .helperfunctions import myfunc

bl_info = {
	"name": "Dummy Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202104291743),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Mesh > Dummy Op",
	"description": "A dummy operator that makes use of bundled modules",
	"category": "Experimental development"}


class DummyOpModule(bpy.types.Operator):
	bl_idname = 'mesh.dummyopmodule'
	bl_label = 'Dummy Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		loc = context.active_object.location
		context.active_object.location = myfunc(loc)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		DummyOpModule.bl_idname,
		text=DummyOpModule.bl_label,
		icon='PLUGIN')

classes = [DummyOpModule]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
	unregister_classes()
