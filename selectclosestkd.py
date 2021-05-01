#  selectclosestkd.py
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
from mathutils import kdtree

bl_info = {
	"name": "Select closest kd",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202105011541),
	"blender": (2, 92, 0),
	"location": "View3D > Select > Select closest kd",
	"description": "Select a vertex closest to any vertex of other selected mesh objects using a kd tree",
	"category": "Experimental development"}


class SelectClosestKDOp(bpy.types.Operator):
	bl_idname = 'mesh.selectclosestkdop'
	bl_label = 'Select closest kd'
	bl_options = {'REGISTER', 'UNDO'}

	# only available in edit mode with some other mesh objects selected
	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH' 
			and context.active_object.type == 'MESH'
			and any([o.type == 'MESH'
						for o in set(context.selected_objects) 
								- set([context.active_object])]))

	def execute(self, context):
		bpy.ops.object.editmode_toggle()
		obverts = context.active_object.data.vertices
		obmat = context.active_object.matrix_world

		size = len(obverts)
		kd = kdtree.KDTree(size)
		for i, v in enumerate(obverts):
			kd.insert(obmat @ v.co, i)  # store in world coords
		kd.balance()

		closest_vertex = -1
		closest_distance = 1e30  # big
		for ob in set(context.selected_objects) - set([context.active_object]):
			if ob.type == 'MESH':
				otherverts = ob.data.vertices
				obmatother = ob.matrix_world
				for v in otherverts:
					# convert to world coords
					v_world = obmatother @ v.co
					co, index, dist = kd.find(v_world)
					if dist < closest_distance:
						closest_distance = dist
						closest_vertex = index
		if closest_vertex >= 0:
			obverts[closest_vertex].select = True
		bpy.ops.object.editmode_toggle()
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		SelectClosestKDOp.bl_idname,
		text=SelectClosestKDOp.bl_label,
		icon='PLUGIN')


classes = [SelectClosestKDOp]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)
	unregister_classes()
