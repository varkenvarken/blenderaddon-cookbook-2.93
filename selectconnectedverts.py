#  selectconnectedverts.py
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
import bmesh

bl_info = {
	"name": "Select Connected Verts",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202105011543),
	"blender": (2, 92, 0),
	"location": "View3D > Select > Connected Verts",
	"description": "A dummy operator",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	# Note: you can define your own category if you like
	"category": "Experimental development"}


class ConnectedOp(bpy.types.Operator):
	bl_idname = 'mesh.connectedop'
	bl_label = 'Connected Verts'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH' and
				context.active_object.type == 'MESH')

	def execute(self, context):
		# selecting a mesh elements in edit mode wont work
		bpy.ops.object.mode_set(mode='OBJECT')
		mesh = context.active_object.data
		# collect a set of all indices of selected verts
		v_indices = {v.index for v in mesh.vertices if v.select}
		# select all verts that share an edge w. a selected vert
		for e in mesh.edges:
			v1,v2 = tuple(e.vertices)
			if v1 in v_indices:
				mesh.vertices[v2].select = True
			if v2 in v_indices:
				mesh.vertices[v1].select = True
		# switch back. Note: mode is NOT called EDIT_MESH
		bpy.ops.object.mode_set(mode='EDIT')
		return {"FINISHED"}

class ConnectedOpBMesh(bpy.types.Operator):
	bl_idname = 'mesh.connectedopbmesh'
	bl_label = 'Connected Verts BMesh'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH' and
				context.active_object.type == 'MESH')

	def execute(self, context):
		# no need to free or create a new bmesh object
		# because our add-on doesn't own the data
		bm = bmesh.from_edit_mesh(context.active_object.data)
		selected = [v for v in bm.verts if v.select]
		for v in selected:
			for e in v.link_edges:
				e.other_vert(v).select = True
		bm.select_flush(True)
		bmesh.update_edit_mesh(context.active_object.data)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		ConnectedOp.bl_idname,
		text=ConnectedOp.bl_label,
		icon='PLUGIN')
	self.layout.operator(
		ConnectedOpBMesh.bl_idname,
		text=ConnectedOpBMesh.bl_label,
		icon='PLUGIN')


classes = [ConnectedOp, ConnectedOpBMesh]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)
	unregister_classes()
