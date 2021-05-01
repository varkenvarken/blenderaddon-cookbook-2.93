#  addoperatortomenu.py
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
	"version": (0, 0, 202104300910),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Mesh > Dummy Op",
	"description": "A dummy operator",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class DummyOp(bpy.types.Operator):
	bl_idname = 'mesh.dummyop'
	bl_label = 'Dummy Operator'
	bl_options = {'REGISTER', 'UNDO'}

	size : bpy.props.FloatProperty(name="Size",
		default=1.0, min=0.1, max=10.0)

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		# do something simple but visible
		bpy.ops.mesh.primitive_cube_add(size=self.size)
		return {"FINISHED"}

def menu_func(self, context):
	# basic operator
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label)
	# with icon
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label,
		icon='MESH_CUBE')
	# other ui elements possible as well
	self.layout.separator()
	# can set values for properties
	# (do for all, because last value is remembered)
	op = self.layout.operator(
		DummyOp.bl_idname,
		text="Big cube",
		icon='ZOOM_IN')
	op.size = 2.0
	op = self.layout.operator(
		DummyOp.bl_idname,
		text="Little cube",
		icon='ZOOM_OUT')
	op.size = 1.0


classes = [DummyOp]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_add.remove(menu_func)
	unregister_classes()
