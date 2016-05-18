# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from MCExport.Exporter import function

class MinecraftCubeModelExporter(Operator, ExportHelper):
    """Export the mesh in Minecraft cube format"""
    bl_idname = "export_mesh.java"
    bl_label = "Export Minecraft cube model"
    
    # ExportHelper mixin class uses this
    filename_ext = ".java"
    
    filter_glob = StringProperty(
        default="*.java",
        options={'HIDDEN'},
        )
    
    export_animations = BoolProperty(
        name="Export animations",
        description="Set to export animation data.",
        default=False,
    )
    
    def execute(self, context):
        return function.writeData(context, self.filepath, self.export_animations)#, self.use_setting)

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(MinecraftCubeModelExporter.bl_idname, text="Minecraft cube-model format")

