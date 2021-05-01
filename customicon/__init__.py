#  customicon.zip
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


# this file should not be installed as an add-on by itself!
# it is also present in customicon.zip where it is called
# __init__.py  together with directory called icons/

import bpy

bl_info = {
	"name": "Custom Icon",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202104301201),
	"blender": (2, 92, 0),
	"location": "View3D > Add > Mesh > Dummy Op",
	"description": "A dummy operator",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class DummyOp(bpy.types.Operator):
	bl_idname = 'mesh.dummyop'
	bl_label = 'Dummy Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		# do something simple but visible
		bpy.ops.mesh.primitive_cube_add(radius=self.radius)
		return {"FINISHED"}

# we can have several collections of previews/icons
preview_collections = {}

def load_icon():
	import os

	try: # if anything goes wrong, for example because we are not running 2.75+ we just ignore it
		from bpy.utils import previews
		pcoll = previews.new()

		# path to the folder where the icon is
		# the path is calculated relative to this py file inside the addon folder
		my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

		# load all previews
		icons = [entry
					for entry in os.scandir(my_icons_dir)
					if entry.is_file()
						and entry.name.endswith('.png')]
		for icon in icons:
			name = os.path.splitext(icon.name)[0]
			pcoll.load(name, icon.path, 'IMAGE')

		preview_collections['operator_icons'] = pcoll
	except Exception as e:
		print(e)
		pass


def menu_func(self, context):
	try:
		icon = preview_collections['operator_icons']['cube']
		self.layout.operator(DummyOp.bl_idname,
			text=DummyOp.bl_label, icon_value=icon.icon_id)
	except:
		self.layout.operator(DummyOp.bl_idname,
			text='Cube', icon='PLUGIN')
	try:
		icon = preview_collections['operator_icons']['box']
		self.layout.operator(DummyOp.bl_idname,
			text=DummyOp.bl_label, icon_value=icon.icon_id)
	except:
		self.layout.operator(DummyOp.bl_idname,
			text='Box', icon='PLUGIN')
	try:  # this one is not present
		icon = preview_collections['operator_icons']['crate']
		self.layout.operator(DummyOp.bl_idname,
			text=DummyOp.bl_label, icon_value=icon.icon_id)
	except:
		self.layout.operator(DummyOp.bl_idname,
			text='Crate', icon='PLUGIN')

classes = [DummyOp]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	load_icon()
	register_classes()
	bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_add.remove(menu_func)
	unregister_classes()
	try:
		for pcoll in preview_collections.values():
			bpy.utils.previews.remove(pcoll)
	except Exception as e:
		pass

