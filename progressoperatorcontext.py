#  progressoperatorcontext.py
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
from time import sleep

bl_info = {
	"name": "Progress Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202105011426),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Mesh > Progress",
	"description": "An operator showing a progress bar",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

class ProgressCM:

	def __init__(self, wm=None, steps=100):
		self.running = False
		self.wm = wm
		self.steps = steps
		self.current_step = 0

	def __enter__(self):
		if self.wm:
			self.wm.progress_begin(0, self.steps)
			self.step()
			self.running = True
		return self

	def __exit__(self, *args):
		self.running = False
		if self.wm:
			self.wm.progress_end()
			self.wm = None
		else:
			print("Done.\n")

	def step(self, amount=1):
		self.current_step += amount
		self.current_step = min(self.current_step, self.steps)
		if self.wm:
			self.wm.progress_update(self.current_step)
		else:
			print("Step "
					+ str(self.current_step)
					+ "/" + str(self.steps))

class ProgressOpContext(bpy.types.Operator):
	bl_idname = 'mesh.progressopcontext'
	bl_label = 'Progress'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		with ProgressCM(wm=context.window_manager,
						steps=5) as progress:
			for i in range(5):
				progress.step(1)
				sleep(1)  # imagine we do something heavy here

		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		ProgressOpContext.bl_idname,
		text=ProgressOpContext.bl_label,
		icon='PLUGIN')

classes = [ProgressOpContext]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
	unregister_classes()
