#  chaincurve.py
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
from mathutils import kdtree, Vector

bl_info = {
	"name": "Create a curve between selected objects",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202104301118),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Curve between objects",
	"description": """Create a curve between selected objects""",
	"category": "Experimental development"}

def object_list(objects, active=0):
	"""
	Return an approximate shortest path through objects starting at the
	active index using the nearest neighbor heuristic.
	"""

	# calculate a kd tree to quickly answer nearest neighbor queries
	kd = kdtree.KDTree(len(objects))
	for i, ob in enumerate(objects):
		kd.insert(ob.location, i)
	kd.balance()

	current = objects[active]
	chain = [current]  # we start at the chosen object
	added = {active}
	for i in range(1,len(objects)):  # we know how many objects to add
		# when looking for the nearest neighbor we start with two neigbors
		# (because we include the object itself in the search) and if
		# the other neigbors is not yet in the chain we add it, otherwise
		# we expand our search to a maximum of the total number of objects
		for n in range(2,len(objects)):
			neighbors = { index for _,index,_ in kd.find_n(current.location, n) }
			neighbors -= added
			if neighbors:  # strictly speaking we shoudl assert that len(neighbors) == 1
				chain.extend(objects[i] for i in neighbors)
				added |= neighbors
				break
		current = chain[-1]

	return chain

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

class CurveBetweenObjects(bpy.types.Operator):
	bl_idname = 'curve.curvebetweenobjects'
	bl_label = 'Curve between objects'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT'
			and len(context.selected_objects) > 1)

	def execute(self, context):
		so = context.selected_objects.copy()
		objects = object_list(so, so.index(context.active_object))

		for ob in objects:
			ob.select_set(False)

		midpoint = sum((ob.location for ob in objects),Vector()) / len(objects) # poll() guarantees we don't get a divide by zero

		curve = bpy.data.curves.new(name='Curve', type='CURVE')
		curve.dimensions = '3D'
		curve.bevel_depth = 0.01
		spline = curve.splines.new(type='BEZIER')
		spline.bezier_points.add(len(objects)-1)  # default curve has 1 point
		for ob,bp in zip(objects,spline.bezier_points):
			bp.co = ob.location - midpoint  # subtract will generate a new vector
			bp.handle_left_type = 'AUTO'
			bp.handle_right_type = 'AUTO'

		ob = bpy.data.objects.new(name='Curve',object_data=curve)
		ob.location = midpoint

		add_object(context, ob)

		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		CurveBetweenObjects.bl_idname,
		text=CurveBetweenObjects.bl_label,
		icon='PLUGIN')


classes = [CurveBetweenObjects]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_add.remove(menu_func)
	unregister_classes()
