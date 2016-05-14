# MCExport
A blender plugin to create and export 3D models for Minecraft modding.

## Installation:
1. Put the MCExport folder into the addons folder of your blender script path. Then navigate to 'File > User Preferences > Add-ons' and activate the "Minecraft cube-exporter" addon.
2. To get the typical Minecraft look uncheck the option "Mipmaps" in 'File > User Preferences > System'. Do not forget to save the changes if you want them to be permanent.

## Usage:
The addon provides buttons for the following three actions:
- Add a new box mesh to the model.
- Set the UV layout of the currently active box model.
- Export the whole model as a .java class that Minecraft can use directly.

Working with this addon is quite simple and typically goes as follows:  
You start out with a blender box located at the origin.
Since the vertex order of this object is not always the same you should delete it.
(In principle the blender box works fine for exporting a model, however, the 'Unwrap' feature does only work smoothly for a fixed order of the vertices.)

It is now easy to build a box model:  
Create box objects by clicking on the 'Add box' button in the 'Misc > Minecraft Tools' tab in the toolbar in the 'View3D' blender-context.
Resize those boxes by changing the 'Dimensions' or 'Scale' variables in blender's 'Transform' tab.
**Note that the dimensions always need to be integer valued!**
This is required by Minecraft as a face with unit width and height corresponds to exactly one pixel in a texture.
You can now simply place an arbitrary number of boxs to build your model.
Note, that the origin of the box is also the rotation point of your Minecraft model.
**Forward in the Minecraft world corresponds to the -y direction in the blender world.**
The uv-layout for a Minecraft box model (in blender space) is the following:  
```
          dx     dx
       +------+------+
       |  T   |  D   |        dy
       |      |      |
+------+------+------+------+
|  L   |  F   |  R   |  B   | dz
|      |      |      |      |
+------+------+------+------+
   dy     dx     dy     dx
```
where dx, dy and dz is the box' dimension in x, y and z direction.  
Having created a texture (or part of it) in a graphics program, you can load it into blender by opening a 'UV/Image Editor' window in blender and load it as the first texture.
**Note that the texture size has to be at least 256x256 for Minecraft to be able to work with it.**
You can now go into the 'Edit' mode in the 'View3D' window and select all vertices of a box.
Clicking the 'Unwrap button' in the 'Misc > Minecraft Tools' tab in the toolbar in the 'View3D' blender-context the uv-coordinates for the active box will be set according to the layout printed above.
In the 'UV/Image Editor' window you can now set the loaded texture as the active texture for your current box.
Set the option 'Snap to pixels', select all uv-vertices and press 'G' to translate the uv-layout to the position you want it to be.
By activating the 'Viewport shading > Texture' option you can see the actual texture pinned to your model.
You can tinker with the texture and reload it until the model looks the way you want it.

When everything looks as desired, navigate to 'File > Export > Minecraft cube-model format' to export the model as a .java file.
This file can then be put into the source folder of your Minecraft mod.
(Or you want to use it to render something nice in blender :P)

Coming up:  
- Export the texture layout with lines indicating the position and size of the cubes to make it easier building a texture for your model.
- Animations: Use the action feature in blender to create named animated sequences to be exported to Minecraft.
