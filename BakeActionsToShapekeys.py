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
