import bpy
import bmesh
from bpy.props import BoolProperty, FloatVectorProperty, BoolVectorProperty, StringProperty

from MCExport.Toolmenu import function


class ToolsPanel(bpy.types.Panel):
    """Menu in tools region.
    
    A menu that provides buttons for adding a box and unwrapping it onto a texture.
    """
    
    bl_label = "Minecraft Tools" # Name of panel.
    bl_space_type = "VIEW_3D" # Mode when this is displayed.
    bl_region_type = "TOOLS" # Section in which panel is displayed.
    
    def draw(self, context):
        layout = self.layout
        layout.operator("button.addbox")
        layout.operator("button.unwrap")


class OBJECT_OT_addBoxButton(bpy.types.Operator):
    """Button that adds a box mesh to the scene.
    
    A button that creates a box mesh at the origin of the current scene.
    The vertices have a fixed order so it is easy to unwrap them in a texture.
    """

    bl_idname = "button.addbox"
    bl_label = "Add box"

    layers = BoolVectorProperty(
        name="Layers",
        description="Object Layers",
        size=20,
        options={'HIDDEN', 'SKIP_SAVE'},
        )

    align: StringProperty("WORLD")

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
        # Create the vertex and face arrays.
        verts_loc, faces = function.create_box(1, 1, 1)
        # Create new mesh.
        mesh = bpy.data.meshes.new("Box")
        # Create new bmesh.
        bm = bmesh.new()
        # Put vertices into bmesh.
        for v_co in verts_loc:
            bm.verts.new(v_co)
        bm.verts.ensure_lookup_table()
        # Put faces into bmesh.
        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])
        # Update the mesh.
        bm.to_mesh(mesh)
        mesh.update()
        # Add the mesh as an object into the scene with this utility module.
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)
        return{'FINISHED'}


class OBJECT_OT_unwrapButton(bpy.types.Operator):
    """
    Unwrap button that is used to unwrap the cube as done in MC.
    The button only works in edit mode and when a texture is active.
    """

    bl_idname = "button.unwrap"
    bl_label = "Unwrap"

    def execute(self, context):
        active_image = self.get_active_texture_()
        if active_image is not None and active_image.size[0] > 0 and active_image.size[1] > 0:
            function.set_uv(context.active_object, active_image.size)
        return{'FINISHED'}

    @classmethod
    def poll(cls, context):
        active_image = cls.get_active_texture_()
        return context.object and (context.object.mode == 'EDIT') and (context.object.type == 'MESH') \
            and active_image is not None and active_image.size[0] > 0 and active_image.size[1] > 0

    @classmethod
    def get_active_texture_(cls):
        active_image = None
        for area in bpy.context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                active_image = area.spaces.active.image
        return active_image
