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

armature = bpy.context.active_object
meshes = []

# Returns the length of a list - 1 for array indexing purposes
# Does not allow return of a negative index
def get_last_array_index(list_len=0):
	last_index = list_len - 1
	return last_index if last_index > -1 else 0

def run():
	# TODO: Operate on copy of object
	# TODO: Multiple actions
	# TODO: Support bake by keyframe (bake selected keyframe only)

#	actions = [armature.animation_data.action]

	C.view_layer.objects.active = armature 
	active_action_name = armature.animation_data.action.name
	print(f"Baking {active_action_name} to shape key")

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
		# Apply modifier as shapekey and rename as action name
		# If duplicate name exists, hopefully blender handles that lmao
		print("Applying Armature modifier as shape key")
		C.view_layer.objects.active = mesh
		bpy.ops.object.modifier_set_active(modifier="Armature")
		bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier="Armature", report=True)
#		last_shapekey_index = get_last_array_index(C.active_object
#		C.active_object.active_shape_key_index = get_last_array_index()

def main():
	print("***************************************")
	print("BakeShapeKeysToActions")
	can_run = True 
#	# Armature is active object
#	if armature == None or armature.type != 'ARMATURE':
#		print('Active object is not armature')
#		can_run = False
	# Meshes are selected
	for obj in C.selected_objects:
		if obj.type == 'ARMATURE':
			armature = obj
			print(f'Setting {obj.name} as ')
		if obj.type == 'MESH':
			meshes.append(obj)
			print(f'Adding {obj.name} to meshes array')
	if not meshes:
		print("No meshes added")
		can_run = False
	#
	if can_run:
		run()
	else:
		print('Aborting BakeActionsToShapekeys')
	print("BakeShapeKeysToActions Finished: %.4f sec" % (time.time() - time_start))
	print("***************************************")

main()