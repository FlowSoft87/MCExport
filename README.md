# MCExport
A blender plugin to create and export 3D models for Minecraft modding.

## Installation
1. Put the MCExport folder into the addons folder of your blender script path. Then navigate to 'File > User Preferences > Add-ons' and activate the "Minecraft cube-exporter" addon.
2. To get the typical Minecraft look uncheck the option "Mipmaps" in 'File > User Preferences > System'. Do not forget to save the changes if you want them to be permanent.

## Usage
Creating a Minecraft model goes in the following steps:
1. Place the boxes which your model consists of.
2. Wrap the boxes in a texture.
3. Export the model as a .java file that Minecraft understands.

This blender-addon provides buttons for exactly those three actions:
1. Button to add a new box mesh to the scene.
2. Button to set the UV layout of the active box model to conform to Minecraft.
3. Export menu entry to export the scene as a .java class that Minecraft can use as a model.

### Build the model
You start out with a blender cube located at the origin.
Since the vertex order of this object is not always the same you should delete it.
(In principle the blender box works fine for exporting a model, however, the 'Unwrap' feature does only work smoothly for a fixed order of the vertices.)

Create box objects by clicking on the 'Add box' button in the 'Misc > Minecraft Tools' tab in the toolbar in the 'View3D' blender-context.
Resize those boxes by changing the 'Dimensions' or 'Scale' variables in blender's 'Transform' tab.
**Note: The dimensions always need to be integer-valued!**
This is required by Minecraft as a face with unit width and height corresponds to exactly one pixel in a texture.
An arbitrary amount of boxes can be place and rotated to build up your model.
For those familiar with the way Minecraft models work: The origin of the box in blender is also the rotation point of this box in the Minecraft model.
An important note on direction: **forward in the Minecraft world corresponds to the -y direction in the blender world.**
In other words: if you want to create an entity, its front needs to look into -y direction!

Putting a texture on the model goes as follows.
The first thing to do is draw the texture in a graphics program.
The uv-layout for a Minecraft box model (in blender space) is  
```
            dx     dx
         +------+------+
         |      |      |
         |  T   |  D   |        dy
         |      |      |
+--------+------+------+-+------+
|  L     |  F   |  R     |  B   | dz
|        |      |        |      |
+--------+------+--------+------+
   dy       dx     dy       dx
```
where dx, dy and dz is the box' dimension in x, y and z direction and L, F, R, B, T and D correspond to (L)eft, (F)ront, (R)ight, (B)ack, (T)op and (D)own faces of the cube.  
Having created a texture (or part of it) in a graphics program, you can load it into blender by opening a 'UV/Image Editor' window in blender and load it as the first texture.
**Note that the texture size has to be at least 256x256 pixels for Minecraft to be able to work with it.**
You can now go into the 'Edit' mode in the 'View3D' window and select all vertices of a box (by hitting the 'A' button).
Clicking the 'Unwrap button' in the 'Misc > Minecraft Tools' tab in the toolbar in the 'View3D' blender-context the uv-coordinates for the active box will be set according to the layout printed above.
In the 'UV/Image Editor' window you can now set the loaded texture as the active texture for your current box (by clicking the loaded texture in the dropdown menu).
Set the option 'Snap to pixels' in the 'UV' menu, select all uv-vertices and press 'G' to translate the uv-layout to the position you want it to be (so it matches the position of the current cube in your texture).
By activating the 'Viewport shading > Texture' option you can see the actual texture pinned to your model.
You can tinker with the texture and reload it until the model looks the way you want it.  
**Even though blender is able to pin more than one texture layers onto a single model, only the first one will be taken into account when exporting the model later!**

When everything looks as desired, navigate to 'File > Export > Minecraft cube-model format' to export the model as a .java file.
This file can then be put into the source folder of your Minecraft mod.
(Or you use it for rendering in blender :P)

Coming up:  
- Export the texture layout with lines indicating the position and size of the cubes to make it easier building a texture for your model.
- Animations: Use the action feature in blender to create named animated sequences to be exported to Minecraft.
