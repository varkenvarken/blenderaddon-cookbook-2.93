#  numpyscalecm.py
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


import bpy, bmesh
from bpy.props import FloatProperty
from mathutils import Vector
import numpy as np
from time import time

bl_info = {
	"name": "Numpy Scale",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202105011354),
	"blender": (2, 92, 0),
	"location": "View3D > Object > Numpy Scale",
	"description": "Scale around center of mass",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class RegularScaleOp(bpy.types.Operator):
	bl_idname = 'mesh.regularscaleop'
	bl_label = 'Regular Scale CM'
	bl_options = {'REGISTER', 'UNDO'}

	scale = FloatProperty(name='Scale', default=1)

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT' and
				context.active_object.type == 'MESH')

	def execute(self, context):
		# mesh must be in object mode
		ob = context.active_object
		start = time()
		me = ob.data
		count = len(me.vertices)
		# calculate center of mass
		cm = sum((v.co for v in me.vertices), Vector())
		if count > 1:
			cm /= count
		# scale the vertex coordinates
		for v in me.vertices:
			v.co = cm + (v.co - cm) * self.scale
		print("{count} verts scaled in {t:.2f} seconds".format(
					t=time()-start, count=count))
		return {"FINISHED"}

class NumpyScaleOp(bpy.types.Operator):
	bl_idname = 'mesh.numpyscaleop'
	bl_label = 'Numpy Scale CM'
	bl_options = {'REGISTER', 'UNDO'}

	scale = FloatProperty(name='Scale', default=1)

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT' and
				context.active_object.type == 'MESH')

	def execute(self, context):
		# mesh must be in object mode
		ob = context.active_object
		start = time()
		me = ob.data
		# get vertex coordinates
		count = len(me.vertices)
		shape = (count, 3)
		verts = np.empty(count*3, dtype=np.float32)
		me.vertices.foreach_get('co', verts)
		verts.shape = shape
		# calculate center of mass
		cm = np.average(verts,axis=0)
		# scale the vertex coordinates
		verts = cm + (verts - cm ) * np.float32(self.scale)
		# return coordinates, flatten the array first
		verts.shape = count*3
		me.vertices.foreach_set('co', verts)
		print("{count} verts scaled in {t:.2f} seconds".format(
					t=time()-start, count=count))
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		RegularScaleOp.bl_idname,
		text=RegularScaleOp.bl_label,
		icon='PLUGIN')
	self.layout.operator(
		NumpyScaleOp.bl_idname,
		text=NumpyScaleOp.bl_label,
		icon='PLUGIN')


classes = [NumpyScaleOp]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	unregister_classes()
