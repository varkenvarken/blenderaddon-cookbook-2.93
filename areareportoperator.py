#  areareportoperator.py
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
	"name": "Area Report Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202104300925),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Mesh > Area Report",
	"description": "Show info in an area header",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	# Note: you can define your own category if you like
	"category": "Experimental development"}


class AreaReportOp(bpy.types.Operator):
	bl_idname = 'mesh.areareportop'
	bl_label = 'Area Report Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		# we need to keep a reference to the area because
		# after the forced redraw the context is changed
		area = context.area
		area.header_text_set(text="Informational message")
		area.tag_redraw()

		# if we don't cause a redraw by our actions, the
		# area header will not be shown. In that case we
		# have to force a redraw, which is not supported
		# and shows warnings on the console. see:
		# https://www.blender.org/api/blender_python_api_current/info_gotcha.html?highlight=redraw#can-i-redraw-during-the-script
		bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

		# some long running stuff here
		try:
			sleep(3)
		except Exception:
			pass
		finally:
			# pass None to restore menu. Not an empty string!
			area.header_text_set(text=None)
			area.tag_redraw()
		return {"FINISHED"}

class AreaReportModalOp(bpy.types.Operator):
	bl_idname = 'mesh.areareportmodalop'
	bl_label = 'Area Report Modal Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def modal(self, context, event):
		# note that we now set this text during every event!
		context.area.header_text_set(
			text="ESC or right mouse to exit")
		# not necessary but it doesn hurt:
		context.area.tag_redraw()

		if event.type in {'RIGHTMOUSE', 'ESC'}:
			context.area.header_text_set(text=None)
			context.area.tag_redraw()
			return {'CANCELLED'}

		print("Running modal", event.type, event.value)

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


def menu_func(self, context):
	self.layout.operator(
		AreaReportOp.bl_idname,
		text=AreaReportOp.bl_label,
		icon='PLUGIN')
	self.layout.operator(
		AreaReportModalOp.bl_idname,
		text=AreaReportModalOp.bl_label,
		icon='PLUGIN')


classes = [AreaReportOp, AreaReportModalOp]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
	unregister_classes()
