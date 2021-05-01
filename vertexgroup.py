#  vertexgroup.py
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
from bpy.props import BoolProperty

bl_info = {
	"name": "Vertex Group",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202105011553),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Mesh > Cube with vertex group",
	"description": "Add a cube with a vertex group",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class VertexGroupOp(bpy.types.Operator):
	bl_idname = 'mesh.vertexgroupop'
	bl_label = 'Cube with vertex group'
	bl_options = {'REGISTER', 'UNDO'}

	usebmesh : BoolProperty(name='Use bmesh')

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		bpy.ops.mesh.primitive_cube_add()
		ob = context.active_object
		vg = ob.vertex_groups.new(name="Tetrahedron")
		verts = ob.data.vertices
		vg.add([v.index for v in verts
					if v.co.x * v.co.y * v.co.z > 0],
					1.0,
					'REPLACE')
		# next step could have been done in the previous
		# loop but it is separated for illustrative
		# purposes
		# you cannot check whether a vertex group contains
		# a vertex but you can check to which vertex groups
		# a vert belongs
		# NOTE: after each mode change we MUST retrieve the
		# active objects again!
		# NOTE: these mode changes are needed to update the
		# changes
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action='DESELECT')
		ob = context.active_object
		if self.usebmesh:
			# mesh must be in edit mode!
			bm = bmesh.from_edit_mesh(ob.data)
			dl = bm.verts.layers.deform.active
			for v in bm.verts:
				if vg.index in v[dl]:
					if v[dl][vg.index] >= 1.0:
						v.select = True
			bmesh.update_edit_mesh(ob.data)
		else:
			# mesh must be in object mode!
			bpy.ops.object.mode_set(mode = 'OBJECT')
			ob = context.active_object
			mesh = ob.data
			for v in mesh.vertices:
				for vge in v.groups:
					if vg.index == vge.group:
						if vge.weight >= 1.0:
							v.select = True
			bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.object.mode_set(mode = 'OBJECT')
		return {"FINISHED"}

import bpy,bmesh

def menu_func(self, context):
	self.layout.operator(
		VertexGroupOp.bl_idname,
		text=VertexGroupOp.bl_label,
		icon='PLUGIN')


classes = [VertexGroupOp]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
	unregister_classes()
