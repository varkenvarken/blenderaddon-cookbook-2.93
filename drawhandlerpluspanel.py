#  drawhandlerpluspanel.py
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
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader

from time import localtime, strftime
from math import sin,cos

bl_info = {
	"name": "Draw Handler and Panel",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202104301404),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Mesh > Draw Handler",
	"description": "Install a clock with control panel",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

running = False
handler = None
timer = None
analog = True

ticks = [(sin(6.283 * t/12.0), cos(6.283 * t/12.0)) for t in range(12)]

buf = bgl.Buffer(bgl.GL_INT, 4)  # linear array of 4 ints

def cursor_handler(context):

	global ticks
	global buf
	global analog

	bgl.glGetIntegerv(bgl.GL_VIEWPORT,buf)
	width = buf[2]

	t = localtime()
	m = t[4]
	h = (t[3]%12) + m/60.0  # fractional hours
	twopi = 6.283

	# draw text
	font_id = 0
	blf.position(font_id, width - 100, 15, 0)
	blf.size(font_id, 12, 72)  # 12pt text at 72dpi screen
	blf.draw(font_id, strftime("%H:%M:%S", t))

	if analog:
		# also see: https://blog.michelanders.nl/2019/02/working-with-new-opengl-functionality.html
		# 50% alpha, 2 pixel lines
		bgl.glEnable(bgl.GL_BLEND)
		bgl.glLineWidth(2)

		points = []
		# draw a clock in the lower right hand corner
		startx, starty = (width - 22.0,22.0)
		smallhandx, smallhandy = (startx + 9*sin(twopi * h/12),
								starty + 9*cos(twopi * h/12))
		bighandx, bighandy = (startx + 15*sin(twopi * m/60),
								starty + 15*cos(twopi * m/60))
		points.append((startx, starty))
		points.append((bighandx, bighandy))
		points.append((startx, starty))
		points.append((smallhandx, smallhandy))
		# twelve small dots
		for x,y in ticks:
			points.append((startx + 17*x, starty + 17*y))
			points.append((startx + 18*x, starty + 18*y))

		shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
		batch = batch_for_shader(shader, 'LINES', {"pos": points})
		shader.bind()
		shader.uniform_float("color", (1.0, 1.0, 1.0, 0.5))
		batch.draw(shader)
	  
		# restore opengl defaults
		bgl.glLineWidth(1)
		bgl.glDisable(bgl.GL_BLEND)


# also see http://blender.stackexchange.com/questions/30295/how-add-properties-to-operator-modal-draw

class ModalDrawHandlerOp(bpy.types.Operator):
	bl_idname = 'view3d.modaldrawhandlerop'
	bl_label = 'Show Clock'
	bl_options = {'REGISTER'}

	def modal(self, context, event):
		global running
		global width
		if not running:
			self.cancel(context)
			return {'CANCELLED'}
		if event.type == 'TIMER':
			context.area.tag_redraw()  # yes this is needed
		return {'PASS_THROUGH'}

	def cancel(self, context):
		global timer
		global handler
		wm = context.window_manager
		if timer:
			wm.event_timer_remove(timer)
			print('timer removed')
		if handler:
			bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
			handler = None
			print('handler removed')
		context.area.tag_redraw()

	def execute(self, context):
		global running
		global handler
		global timer
		if not running:
			running = True
			args = (context, )
			handler = bpy.types.SpaceView3D.draw_handler_add(cursor_handler, args, 'WINDOW', 'POST_PIXEL')
			timer = context.window_manager.event_timer_add(1.0, window=context.window)
			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {"FINISHED"}

class DrawHandlerOp(bpy.types.Operator):
	bl_idname = 'view3d.drawhandlerop'
	bl_label = 'Hide Clock'
	bl_options = {'REGISTER'}

	def execute(self, context):
		global running
		running = False
		return {"FINISHED"}

class VIEW3D_PT_clock(bpy.types.Panel):
    bl_label = "Clock"
    bl_idname = "OBJECT_PT_clock"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Clock"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, 'show_clock', text='Show clock')
        layout.prop(context.scene, 'clock_analog', text='Analog display')

def clock_check(self, context):
	if self.show_clock:
		bpy.ops.view3d.modaldrawhandlerop()
	else:
		bpy.ops.view3d.drawhandlerop()
	analog_check(self, context)

def analog_check(self, context):
	global analog
	analog = self.clock_analog

classes = [DrawHandlerOp, ModalDrawHandlerOp, VIEW3D_PT_clock]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.Scene.show_clock = bpy.props.BoolProperty(default=False, update=clock_check)
	bpy.types.Scene.clock_analog = bpy.props.BoolProperty(default=False, update=analog_check)

def unregister():
	global handler
	if handler:
		print(handler)
		bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
	# this function is marked as 'internal use' but needed to fully
	# remove a scene property. Del does NOT work
	#try:
	#	bpy.ops.wm.properties_remove(data_path="scene", property="clock_analog")
	#except Exception:
	#	print('could not remove clock_analog property')
	#try:
	#	bpy.ops.wm.properties_remove(data_path="scene", property="show_clock")
	#except Exception:
	#	print('could not remove show_clock property')
	unregister_classes()
	#del bpy.types.Scene.show_clock
	#del bpy.types.Scene.clock_analog
	for sc in bpy.data.scenes:
		sc.show_clock = False
		sc.clock_analog = False
	print('unregister done')
