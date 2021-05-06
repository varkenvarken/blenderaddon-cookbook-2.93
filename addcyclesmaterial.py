#  addcyclesmaterial.py
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
	"name": "Add Material",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202105061320),
	"blender": (2, 92, 0),
	"location": "Node > Add > Add aterial",
	"description": "Add a basic node based material",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class AddNodeMat(bpy.types.Operator):
	bl_idname = 'node.add_material'
	bl_label = 'Add Material'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return ((context.active_object is not None )
				and (context.space_data.type == 'NODE_EDITOR')
				and (context.space_data.shader_type == 'OBJECT'))

	def execute(self, context):
		bpy.ops.object.material_slot_add()
		ob = context.active_object
		slot = ob.material_slots[ob.active_material_index]
		mat = bpy.data.materials.new('Material')
		mat.use_nodes = True
		slot.material = mat
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		AddModifier.bl_idname,
		text=AddModifier.bl_label,
		icon='PLUGIN')


def menu_func(self, context):
	self.layout.operator(
		AddNodeMat.bl_idname,
		text=AddNodeMat.bl_label,
		icon='PLUGIN')

classes = [AddNodeMat]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.NODE_MT_add.append(menu_func)


def unregister():
	bpy.types.NODE_MT_add.remove(menu_func)
	unregister_classes()
