#  modaloperator.py
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
	"name": "Modal Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202105011334),
	"blender": (2, 92, 0),
	"location": "View3D > Object > Modal Operator",
	"description": "Example of a modal operator",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

class ModalOp(bpy.types.Operator):
	bl_idname = 'mesh.modalop'
	bl_label = 'Modal Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def modal(self, context, event):
		context.area.header_text_set(
			text="event: {e.type} {e.value} ({e.mouse_x},{e.mouse_y})".format(e=event))
		context.area.tag_redraw()

		if event.type in {'RIGHTMOUSE', 'ESC'}:
			context.area.header_text_set(text=None)
			context.area.tag_redraw()
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		# this is what makes an operator modal:
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


def menu_func(self, context):
	self.layout.operator(
		ModalOp.bl_idname,
		text=ModalOp.bl_label,
		icon='PLUGIN')


classes = [ModalOp]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	unregister_classes()
