#  dummyoperator.py
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
	"name": "Dummy Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202104301629),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Mesh > Dummy Op",
	"description": "A dummy operator",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	# Note: you can define your own category if you like
	"category": "Experimental development"}


class DummyOp(bpy.types.Operator):
	bl_idname = 'mesh.dummyop'
	bl_label = 'Dummy Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

# no draw function, add one if needed

# the execute function is empty
	def execute(self, context):
		return {"FINISHED"}


# we do need a menu entry. Operators without it cannot be searched.
# see: https://wiki.blender.org/wiki/Reference/Release_Notes/2.90/Python_API#Compatibility

def menu_func(self, context):
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label,
		icon='PLUGIN')

classes = [DummyOp]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_add.remove(menu_func)
	unregister_classes()
