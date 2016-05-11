import bpy
import bmesh
from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty

from MinecraftExporter.Toolmenu import function

#
#    Menu in tools region
#
class ToolsPanel(bpy.types.Panel):
    bl_label = "Minecraft Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("button.addbox")
        layout.operator("button.unwrap")

#
#   Add box button that constructs a MC cube.
#
class OBJECT_OT_addBoxButton(bpy.types.Operator):
    bl_idname = "button.addbox"
    bl_label = "Add box"
    
    # generic transform props
    view_align = BoolProperty(
        name="Align to View",
        default=False,
        )
    location = FloatVectorProperty(
        name="Location",
        subtype='TRANSLATION',
        )
    rotation = FloatVectorProperty(
        name="Rotation",
        subtype='EULER',
        )

    def execute(self, context):
        verts_loc, faces = function.getBox(1,1,1)

        mesh = bpy.data.meshes.new("Box")

        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.new(v_co)

        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)
        return{'FINISHED'}

#
#   Unwrap button that is used to unwrap the cube as done in MC.
#   The button only works in edit mode and when a texture is active.
#
class OBJECT_OT_unwrapButton(bpy.types.Operator):
    bl_idname = "button.unwrap"
    bl_label = "Unwrap"
    
    @classmethod
    def poll(self, context):
        if context.object and (context.object.mode == 'EDIT') and (context.object.type == 'MESH') and (len(bpy.data.images) > 0):
            return True
    
    def execute(self, context):
        print("Unwrap "+bpy.context.object.name)
        function.setUVs(context.active_object,bpy.data.images[0].size)
        return{'FINISHED'}

