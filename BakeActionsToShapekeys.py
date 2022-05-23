# BakeActionsToShapekeys
# Copyright (C) 2022 VOXIE3D
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import bpy
D = bpy.data
C = bpy.context
time_start = time.time()

# 
armature = bpy.context.active_object
meshes = []
initial_selected_objects = []
#
action_name_filter = "Exp"
actions_to_bake = []

# Returns the length of a list - 1 for array indexing purposes
# Does not allow return of a negative index
def get_last_array_index(list_len=0):
	last_index = list_len - 1
	return last_index if last_index > -1 else 0

def run():
	# TODO: Operate on copy of object
	# TODO: Multiple actions
	# TODO: Support bake by keyframe (bake selected keyframe only)

	# Filter actions by name TODO: or regex
	# These are strings
	if action_name_filter != "":
		actions_to_bake = [action for action in bpy.data.actions.keys() if action_name_filter in action]
	else:
		actions_to_bake = [C.active_object.animation_data.action]
	print(f"Actions to bake: {str(actions_to_bake)}")

	C.view_layer.objects.active = armature 

	for mesh in meshes:
		C.view_layer.objects.active = mesh

		# Find armature mod
		armature_modifier = [mod for mod in C.active_object.modifiers if mod.type == 'ARMATURE']
		if armature_modifier:
			bpy.ops.object.modifier_set_active(modifier="Armature")
		else:
			#TODO: Add armature modifier if missing
			print(f"No armature modifier found, skipping {mesh.name}")

		# Add basis shape key if missing
		if C.active_object.active_shape_key == None:
			print(f'Adding basis shapekey in {mesh.name}')
			bpy.ops.object.shape_key_add(False)
		C.active_object.active_shape_key_index = 0

		# TODO: Re-set keyframe so the active frame is what is in the action
		# TODO: Find armature modifier if it doesn't exist or is named differently than "Armature"
		# Apply modifier as shapekey and rename as action name
		# If duplicate name exists, hopefully blender handles that lmao
		for action in actions_to_bake:
			action_name = action
			C.view_layer.objects.active = armature 
			C.active_object.animation_data.action = bpy.data.actions.get(action_name)

			C.view_layer.objects.active = mesh
			print(f"Baking {action_name} to shape key for mesh {C.view_layer.objects.active.name}")
			bpy.ops.object.modifier_set_active(modifier="Armature")
			bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier="Armature", report=True)
			last_shapekey_index = get_last_array_index(len(C.active_object.data.shape_keys.key_blocks.keys()))
			# If last shapekey index is 0 applying the modifier likely failed
			if last_shapekey_index > 0:
				C.active_object.active_shape_key_index = last_shapekey_index
				#TODO: Hopefully blender handles renaming shapekeys to with duplicate action name
				C.active_object.active_shape_key.name = action_name
			else:
				print("Shapekey bake failed")

		# Set active object back to armature at end for simpler workflow before multiple actions
		print("Restoring previously selected objects")
		C.view_layer.objects.selected = initial_selected_objects
		C.view_layer.objects.active = armature 

def main():
	print("***************************************")
	print("BakeShapeKeysToActions")
	can_run = True 
#	# Armature is active object
#	if armature == None or armature.type != 'ARMATURE':
#		print('Active object is not armature')
#		can_run = False
	# Meshes are selected
	initial_selected_objects = C.selected_objects
	for obj in C.selected_objects:
		if obj.type == 'ARMATURE':
			armature = obj
			print(f'Setting {obj.name} as armature object')
		if obj.type == 'MESH':
			meshes.append(obj)
			print(f'Adding {obj.name} to meshes array')
	if not meshes or not armature:
		print("No meshes added or armature not selected")
		can_run = False
	#
	if can_run:
		run()
	else:
		print('Aborting BakeActionsToShapekeys')
	print("BakeShapeKeysToActions Finished: %.4f sec" % (time.time() - time_start))
	print("***************************************")

main()