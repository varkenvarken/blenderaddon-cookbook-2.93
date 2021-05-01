#  importfrombundledblend
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
import os

bl_info = {
	"name": "Import object from bundled .blend",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202105010955),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Mesh > Import Operator",
	"description": "A dummy operator",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

def add_object(context, ob):
	"""
	Add an object to the active view layer and make it the active object.
	"""
	scene = context.scene
	layer = context.view_layer
	layer_collection = context.layer_collection or layer.active_layer_collection
	scene_collection = layer_collection.collection
	scene_collection.objects.link(ob)
	ob.select_set(True)
	layer.objects.active = ob

class DummyOp(bpy.types.Operator):
	bl_idname = 'mesh.importop'
	bl_label = 'Import Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		blend = os.path.join(os.path.dirname(__file__), "objects.blend")
		# load a library and copy a specific object with its
		# dependencies into the current scene
		# loading a library multiple times is harmless
		with bpy.data.libraries.load(blend, link=False) as (data_from, data_to):
			data_to.objects = ['3Rings']
		# at this point bpy.data.objects is update but no
		# object links are added to the scene yet
		# note that inside the context manager data_to.objects
		# was a list of names but now we left the context it
		# is transnuted into a list of objects!
		for ob in data_to.objects:
			add_object(context, ob)
		return {"FINISHED"}

def menu_func(self, context):
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label)


classes = [DummyOp]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
	unregister_classes()
