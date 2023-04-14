# Bake Actions To Shapekeys

A script to automate baking actions to shape keys with corrective smoothing. Intended for use with meshes with complicated facial rigs that need to be optimized for real-time usage (i.e. Unity).


# Usage 
## Instructions
* Select mesh objects and armature object last  
* Meshes should have Armature modifier named "Armature" (without quotes)  
* Link action you want to bake in the Action Editor  
* Run script  

## Manual method 
* Select the armature and link the action you want to bake
* Select your mesh Armature modifier and Save as Shape Key
* Disable your Armature modifier
* Select the new shape key on your mesh
* Save as Shape Key on Corrective Smooth modifier
* Select your new shape key and rename to your action name
* Repeat 200 times...

# Gotchas
* Make sure all the bones affected by your actions are on visible layers
* You must have a Corrective Smooth modifier on all meshes (you can set the smoothing amount to 0.0 if you don't need it)
* Make sure your timeline is on the keyframe you want to bake
* You must be in Object mode when running the script

### Works with Blender 3.3.1

### License
GPLv3
