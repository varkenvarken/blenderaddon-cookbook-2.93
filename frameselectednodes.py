#  frameselectednodes.py
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
from functools import lru_cache

bl_info = {
	"name": "Frame selected nodes",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 202104301650),
	"blender": (2, 92, 0),
	"location": "Node > Bundle in new frame",
	"description": "Join two selected nodes plus those in between into a frame",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

# from node wrangler
def get_nodes_links(context):
    space = context.space_data
    tree = space.node_tree
    nodes = tree.nodes
    links = tree.links
    active = nodes.active
    context_active = context.active_node
    # check if we are working on regular node tree or node group is currently edited.
    # if group is edited - active node of space_tree is the group
    # if context.active_node != space active node - it means that the group is being edited.
    # in such case we set "nodes" to be nodes of this group, "links" to be links of this group
    # if context.active_node == space.active_node it means that we are not currently editing group
    is_main_tree = True
    if active:
        is_main_tree = context_active == active
    if not is_main_tree:  # if group is currently edited
        tree = active.node_tree
        nodes = tree.nodes
        links = tree.links

    return nodes, links
# end from node wrangler

# for memoization see https://docs.python.org/3/library/functools.html#functools.lru_cache
@lru_cache()
def has_selected_child_node(node):
	"""
	Check whether any of of the descendants of a node
	(children, grandchildren, ... following output sockets)
	is selected. Invalid links (circular dependencies) are
	skipped.
	"""
	for socket in node.outputs:
		for link in socket.links:
			if link.is_valid:
				if link.to_node.select:
					return True
				elif has_selected_child_node(link.to_node):
					return True
	return False

def nodepath(node):
	"""
	return a set of nodes that contain all descendant nodes
	along any valid path to a selected descendant.
	"""
	path = set()
	queue = [node]
	while queue:
		node = queue.pop()
		for socket in node.outputs:
			for link in socket.links:
				if link.is_valid:
					node = link.to_node
					if (node.select
						or has_selected_child_node(node)):
						path.add(node)
					queue.append(node)
	return path

class FrameNodes(bpy.types.Operator):
	bl_idname = 'mode.frame_nodes'
	bl_label = 'Bundle in new frame'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return ((context.active_object is not None )
			and (context.space_data.type == 'NODE_EDITOR'))

	def execute(self, context):
		nodes, links = get_nodes_links(context)
		selected_nodes = [n for n in nodes if n.select]
		if len(selected_nodes) == 2:
			has_selected_child_node.cache_clear()
			nodelist = nodepath(selected_nodes[1])
			if len(nodelist) == 0:
				nodelist = nodepath(selected_nodes[0])
			# if we did find some path we make sure we
			# include the endpoints before we add the frame
			if len(nodelist) > 0:
				nodelist |= set(selected_nodes)
				frame = nodes.new('NodeFrame')
				for n in nodelist:
					n.parent = frame
			else:
				self.report({'WARNING'},
						'No path between selected nodes')
		else:
			self.report({'WARNING'},
						'Exactly 2 nodes should be selected')
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		FrameNodes.bl_idname,
		text=FrameNodes.bl_label,
		icon='PLUGIN')

classes = [FrameNodes]

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.NODE_MT_node.append(menu_func)


def unregister():
	bpy.types.NODE_MT_node.remove(menu_func)
	unregister_classes()

