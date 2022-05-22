import bpy
from mathutils import *
D = bpy.data
C = bpy.context

armature = bpy.context.active_object
meshes = []

def run():
	print('run')

def main():
	can_run = True 

	# Make sure we can run the script
	if armature == None or armature.type != 'ARMATURE':
		print('Select the armature first')
		can_run = False
	for obj in C.selected_objects:
		if obj.type == 'MESH':
			meshes.append(obj)
			print(f'Adding {obj.name} to meshes array')
	if not meshes:
		print("No meshes added")

	if can_run:
		run()
	else:
		print('Aborting BakeActionsToShapekeys')

main()
